import telebot, cherrypy, config, os, json, random, requests
from time import strftime
from telebot import types
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.http import MediaFileUpload

KEYBOARD = types.InlineKeyboardMarkup()
KEYBOARD1 = types.InlineKeyboardMarkup()
ANSWERS = config.saveAnswers

# If modifying these scopes, delete the file token.json.
SCOPES = 'xxxx'

themes_list = []
press_check = 0
press_checks = 0
feedback_check = False

FOLDER_DICT = {}
#FOLDER_CHECK = 0
FOLDERS_NAME_LIST = []

WEBHOOK_HOST = 'xxx.xxx.xxx.xxx' #$Host IP-adress
WEBHOOK_PORT = xxxx  # 443, 80, 88 or 8443 (port must be open on the server!)
WEBHOOK_LISTEN = 'xxx.xxx.xxx.xxx'  # On some servers you will be forced to use the same IP as in HOST

# SSL certificate
WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Certificate path
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Private key path

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (config.token)

bot = telebot.TeleBot(config.token)

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            with open('logs.txt', 'w') as logs_file:
                logs_file.write(str(cherrypy.request.body.read(length).decode("utf-8")))
            return ''
        else:
            raise cherrypy.HTTPError(403)

def main():
    global drive

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
        
    drive = build('drive', 'v3', http=creds.authorize(Http()))

# /start command
@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Наш Инстаграм: @pachkaites", url = "https://www.instagram.com/pachkaites/?hl=ru")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, '''Привет! Я бот газеты «Пачкайтесь». 
Мы хотим обеспечить возможность анонимно опубликовать свое творчество. 
Сюда ты можешь отправить файлы со своими текстами, фотографиями, рисунками, набросками и всем, чем хочешь. 
Если ты здесь впервые, ты можешь написать */help* для просмотра доступных команд.''', reply_markup = keyboard, parse_mode='Markdown')
    
# /help command
@bot.message_handler(commands=['help'])
def process_command_help(message):
    bot.send_message(message.chat.id, '''Список доступных команд: 
1. */start* – начало общения с ботом 
2. */themes* – список тем ближайших выпусков
3. */about* - форматы
4. */feedback* - возможность оставить обратную связь
5. */channel* - возможность оставить свой канал''', parse_mode='Markdown')

# /about command (usable formats)
@bot.message_handler(commands=['about'])
def process_command_about(message):
    bot.send_message(message.chat.id, '''Список доступных форматов:
*.docx*, *.doc*, *.odt*, *.jpeg*''', parse_mode='Markdown')

# temporary channel option
@bot.message_handler(commands=['channel'])
def process_command_channel(message):
    answer = bot.send_message(message.chat.id, '''В связи с недавней блокировкой Инстаграма и повсеместным переходом в телеграм каналы, для того чтобы не потеряться, вы может скинуть сюда канал в котором вы обитаете. После, собранная база будет выложена в канале.\n
На твое усмотрение оставить своё имя, но, очевидно, подпишутся на твой канал только те, кто поймут, что он именно твой.''')
    bot.register_next_step_handler(message = answer, callback = saveChnl)

def saveChnl(message):
    msg = message.text
    with open("channels/channels.txt", 'a') as channel_file:
        channel_file.write("[" + str(msg) + "]" + "\n")
        bot.send_message(message.chat.id, "Спасибо, что помогаете не теряться!")

# feedback option
@bot.message_handler(commands=['feedback'])
def feedback(message):
    answer = bot.send_message(message.chat.id, "Здесь вы может высказать обратную связь по поводу газеты, просто отправив сообщение боту:")
    bot.register_next_step_handler(message = answer, callback = saveFdbck)

def saveFdbck(message):
    msg = message.text
    with open("feedback/feedback.txt", 'a') as feedback_file:
        feedback_file.write(f"[{message.from_user.id}; {message.from_user.username}; {message.from_user.first_name} {message.from_user.last_name}]" + "\n" + "[" + str(msg) + "]" + "\n")
        bot.send_message(message.chat.id, "Спасибо за фидбек!")

# buttons themselves
@bot.message_handler(commands=['themes'])
def process_command_themes(message):
    global themes_list, press_check, themes_dict

    keyboard = types.InlineKeyboardMarkup()
    
    with open('themes/themes_list.txt', 'r') as f:
        themes_dict = json.load(f)

    if press_check < 1:
        for key in themes_dict:
            themes_list.append(key)

    
    for smthn in themes_dict:
        inline_btn = types.InlineKeyboardButton(smthn, callback_data = 'btn'+ str(themes_dict[smthn]['number']))
        keyboard.add(inline_btn)
        press_check += 1
        
    bot.reply_to(message, "Список доступных тем:", reply_markup = keyboard)

# button press check and answer
@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('btn'))
def process_callback_button1(callback_query: types.CallbackQuery):
    global themes_list, name, theme_number, themes_dict, folders_check
    
    for key1 in themes_dict:

        code = callback_query.data[-1]
        
        if code.isdigit():
            code = int(code)
        if code == int(themes_dict[key1]["number"]):
            bot.send_message(callback_query.from_user.id, 'Выбранная тема - ' + str(key1))
            bot.send_message(callback_query.from_user.id, 'Теперь вам необходимо отправить ваш текст/фото (список форматов доступен с помощью /about).')
            name = str(key1)

# document and photo saver
@bot.message_handler(content_types=["document"])
def handle_docs(message):
    global name
    theme_name = name
    try:
        time = strftime("%Y-%m-%d %H:%M:%S")

        file_name = message.document.file_name
        file_info = bot.get_file(message.document.file_id)
        src = "received/" + file_name;

        file_ext = src.split('.')[-1]
        downloaded_file = bot.download_file(file_info.file_path)
            
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        page_token = None

        while True:
            response = drive.files().list(q = "mimeType = 'application/vnd.google-apps.folder'", spaces = 'drive', fields = 'nextPageToken, files(id, name)', pageToken = page_token).execute()
            for file in response.get('files', []):
                folder_id = str(file.get('id'))
                folder_name = str(file.get('name'))
                FOLDER_DICT.update({folder_name: folder_id})
                FOLDERS_NAME_LIST.append(folder_name)

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                      break
        
        if theme_name not in FOLDERS_NAME_LIST:
            file_metadata = {'name': str(theme_name), 'mimeType': 'application/vnd.google-apps.folder'}
            file = drive.files().create(body=file_metadata, fields='id').execute()
            folder_id = str(file.get('id'))
            FOLDER_DICT.update({theme_name: folder_id})
            FOLDERS_NAME_LIST.append(theme_name)

            file_metadata = {'name': str(message.document.file_name), 'parents': [folder_id]}

            media = MediaFileUpload('received/' + message.document.file_name, mimetype= 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', resumable = True)

            file = drive.files().create(body=file_metadata, media_body=media, fields='id').execute()
                      
        elif theme_name in FOLDERS_NAME_LIST:
            file_metadata = {'name': str(message.document.file_name), 'parents': [FOLDER_DICT[theme_name]]}

            media = MediaFileUpload('received/' + message.document.file_name, mimetype= 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', resumable = True)

            file = drive.files().create(body=file_metadata, media_body=media, fields='id').execute()
    
        bot.reply_to(message, random.choice(ANSWERS))

        FOLDER_DICT.clear()
        FOLDERS_NAME_LIST.clear()

        response = requests.post('http://127.0.0.1:5000/auth',
                                 json={'docName': file_name, 'date': time, 'docFolder': folder_name})

    except Exception as e:
        bot.reply_to(message, e)
        bot.send_message(message.chat.id, 'Please report the problem: *@teqnot*', parse_mode='Markdown')

# saving photos
@bot.message_handler(content_types = ['photo'])
def handle_photos(message):
    global name
    theme_name = name

    try:
        time = strftime("%Y-%m-%d %H:%M:%S")

        file_name = message.document.file_name
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = "received/" + message.photo[0].file_id;

        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        page_token = None

        while True:
            response = drive.files().list(q="mimeType = 'application/vnd.google-apps.folder'", spaces='drive', fields='nextPageToken, files(id, name)', pageToken=page_token).execute()

            for file in response.get('files', []):
                folder_id = str(file.get('id'))
                folder_name = str(file.get('name'))
                FOLDER_DICT.update({folder_name: folder_id})
                FOLDERS_NAME_LIST.append(folder_name)

            page_token = response.get('nextPageToken', None)

            if page_token is None:
                break

        if theme_name not in FOLDERS_NAME_LIST:
            file_metadata = {'name': str(theme_name), 'mimeType': 'application/vnd.google-apps.folder'}
            file = drive.files().create(body=file_metadata, fields='id').execute()
            folder_id = str(file.get('id'))
            FOLDER_DICT.update({theme_name: folder_id})
            FOLDERS_NAME_LIST.append(theme_name)

            file_metadata = {'name': str(message.photo[0].file_id), 'parents': [folder_id]}

            media = MediaFileUpload('received/' + message.photo[0].file_id, mimetype= 'image/jpeg', resumable=True)

            file = drive.files().create(body=file_metadata, media_body=media, fields='id').execute()

        elif theme_name in FOLDERS_NAME_LIST:
            file_metadata = {'name': str(message.photo[0].file_id), 'parents': [FOLDER_DICT[theme_name]]}

            media = MediaFileUpload('received/' + message.photo[0].file_id, mimetype= 'image/jpeg', resumable=True)

            file = drive.files().create(body=file_metadata, media_body=media, fields='id').execute()

        bot.reply_to(message, 'Фото сохранено!')

        response = requests.post('http://127.0.0.1:5000/auth',
                                 json={'docName': file_name, 'date': time, 'docFolder': folder_name})

        FOLDER_DICT.clear()
        FOLDERS_NAME_LIST.clear()

    except Exception as e:
        bot.reply_to(message, e)
        bot.send_message(message.chat.id, 'Please report the problem: *@teqnot*', parse_mode='Markdown')

if __name__ == '__main__':
    main()

bot.remove_webhook()

bot.set_webhook(url = WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, certificate = open(WEBHOOK_SSL_CERT, 'r'))

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
