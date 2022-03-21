# "Pachkaites" Newspaper Telegram Bot
###### A Telegram bot that performs all the communication with readers/writers of the ['Pachkaites'] (https://t.me/pachkaites) newspaper

## Basic Concept and Some Background

In our school in 10th grade we have an obligatory project that we are supposed to prepare throughout the year. I entered a team of enthusiasts, that were going to make a whole platform via a Telegram channel for students to publish their poems, different texts and etc. They needed a way of getting those files comfortably, and, what's more important, anonymously. I was given a task to come up a solution for this problem. And that's how this project was born.
So, basically what happens is:
User enters the **/themes** command that returns the list of previously announced themes in form of the inline buttons. User then proceeds to choose the theme by pressing a button. Then he sends a file, that will be saved in a chosen directory on a Google Disk, to which all the members of the team have access.    
The active usage period fell on 20/21 school year, in which we managed to publish two full articles with the help of this bot, that are available in the previously managed Telegram channel.

## Basic Functions

**/start** - obviously, a command for starting the conversation
**/help** - command that returns all the other possible commands for the bot
**/about** - command that returns all the possible file formats for further saving

## File Saving 

**/themes** - command that returns the list of all the announced themes. 

> This command gets the list of all available themes from the **themes_list.txt** file, located in the **themes** directory. This way the returned buttons list can be dinamically changed without editing the code itself.

After receiving the name of a chosen theme bot waits for the user to send either a file or a photo. Then the 
