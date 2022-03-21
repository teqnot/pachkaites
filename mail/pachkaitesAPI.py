from flask import Flask, request, render_template, Response
from flask_mail import Mail, Message
import json

app = Flask(__name__)
mail= Mail(app)

app.config['MAIL_SERVER']='smtp.mail.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '########'
app.config['MAIL_PASSWORD'] = '########'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route("/")
def index():
   return 'Hello user!'

@app.route('/auth', methods=['POST'])
def result():
   data = request.json
   docName = data['docName']
   date = data['date']
   folder = data['docFolder']

   msg = Message('Hello', sender = '#######', recipients = ['########'])
   msg.body = f'New file: "{docName}" in {folder}. \n{date}'
   mail.send(msg)

   return Response(status=200)

if __name__ == '__main__':
   app.run()