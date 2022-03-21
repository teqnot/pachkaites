# "Pachkaites" Newspaper Telegram Bot
###### A Telegram bot that performs all the communication with readers/writers of the ['Pachkaites'](https://t.me/pachkaites) newspaper

## Basic Concept and Some Background
In our school in 10th grade we have an obligatory project that we are supposed to prepare throughout the year. I entered a team of enthusiasts, that were going to make a whole platform via a Telegram channel for students to publish their poems, different texts and etc. They needed a way of getting those files comfortably, and, what's more important, anonymously. I was given a task to come up a solution for this problem. And that's how this project was born.
So, basically what happens is:
User enters the **/themes** command that returns the list of previously announced themes in form of the inline buttons. User then proceeds to choose the theme by pressing a button. Then he sends a file, that will be saved in a chosen directory on a Google Disk, to which all the members of the team have access.    
The active usage period fell on 20/21 school year, in which we managed to publish two full articles with the help of this bot, that are available in the previously managed Telegram channel.
Bot works on a remote ruvds.com server with the help of webhooks configured through the cherrypy library. 

## Basic Functions
**/start** - obviously, a command for starting the conversation
**/help** - command that returns all the other possible commands for the bot
**/about** - command that returns all the possible file formats for further saving

## File Saving 
**/themes** - command that returns the list of all the announced themes. 
> This command gets the list of all available themes from the **themes_list.txt** file, located in the **themes** directory. This way the returned buttons list can be dinamically changed without editing the code itself.

After receiving the name of a chosen theme bot waits for the user to send a document or a photo of his choice. Then, judging by file type (document/photo), name of the directory and the document/photo itself are passed to the designated function connected to the Google Drive API: **handle_docs** for all the documents and **handle_photos** for all the photos. 
Either function then checks if the directory already exists in the Google Drive. In this case the sent file will be just simply saved there. If there's no such directory, one will be created, and only then the file will be saved. 
After successful process of saving the document/photo bot will send a message informating the user about it.

## PachkaitesAPI
This a program working with the bot, reporting every time a file was sent. This happens via **FlaskMail** library and the requests, sent to the ip-adress the program is hosted on, everytime a file is received

## Miscellaneous Stuff
**/feedback** - command that allows the user to leave some feedback about the work of the newspaper/photo
**/channel** - command that allows the user to leave their Telegram channel
As it can be known, the Instagram was basically banned in Russia. Because of that a lot of people made a decision about moving their lifestyle to the Telegram channels. This command was implemented only about 2 weeks ago to help all of the "Pachkaites" users to collect a reliable database of their channels, that were later published in the main newspaper channel



