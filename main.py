import asyncio
import threading
import time

import telegram.ext
from telegram.ext import CallbackQueryHandler, ApplicationBuilder, CommandHandler, filters
from telegram.ext import Updater
from  Feedback import Feedback

from youtube_dll.song_conversion import conversion
from ytmusic import YTMusicapp
import database
from telegram import *
from youtube_dll import song_conversion
import os


# useful code
# update.message.reply_text(update.message.text)
# context.bot.send_message(chat_id=update.effective_chat.id,text="Whatsapp")



reply = ""
bot_users={}

database.songs_root_location = os.path.join(os.path.dirname(os.path.abspath(__file__))) + "/Songs"
# database.songs_root_location = os.path.join(os.path.dirname(os.path.abspath(__file__))) + "\\Songs"
music = YTMusicapp
my_chat_ID =  1591024405

#music.YTmusicappclass.song_search("eminem")




async def start(update, context):


    await update.message.reply_text("Hello "+update.effective_chat.first_name+"!"+". My name is Morris, How can i help you today")


async def song(update, context):

    bot_users[update.message.from_user.id] = 'song'
    await update.message.reply_text("Enter name of the song")

async def album(update, context):
    bot_users[update.message.from_user.id] = 'album'
    await update.message.reply_text("Enter name of the Album")
    


async def help(update,context):

    await update.message.reply_text("Choose any of the commands availavble to search and download a song or album")

async def handle_message(update, context):



    if bot_users[update.message.from_user.id] == 'song':
        a = Feedback(update, context, application, "song")


        # asyncio.create_task(a.inLineKeyboardFeedback())



        # x = conversion(update,context,application,"song")
        # context.application.create_task(x.Feedback())

        # context.application.create_task(Feedback(update,context,application,"song"))

    elif bot_users[update.message.from_user.id] == 'album':
        a = Feedback(update, context, application, "album")



        asyncio.create_task(a.inLineKeyboardFeedback())


        # context.application.create_task(Feedback(update,context,application,"album"))


    else:
        await update.message.reply_text("Invalid Command: Please choose a valid command")




Token = '6199155011:AAFTpM4CN17p7fRZ4Y9n0vqHMEi2_vVYQCM'


application = ApplicationBuilder().token(Token).build()
# start_handler = CommandHandler('start', start)
# application.add_handler(start_handler)




application.add_handler(telegram.ext.CommandHandler('album', album,block=False))
# application.add_handler(telegram.ext.CommandHandler('song',dang))
application.add_handler(telegram.ext.CommandHandler('song', song,block=False))
application.add_handler(telegram.ext.CommandHandler('start', start,block=False))
application.add_handler(telegram.ext.CommandHandler('help', help,block=False))
application.add_handler(telegram.ext.MessageHandler(filters.TEXT & (~filters.COMMAND),handle_message,block=False))
application.run_polling()



