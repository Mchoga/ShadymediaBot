import asyncio
import threading
import time

import telegram.ext
from telegram.ext import CallbackQueryHandler, ApplicationBuilder, CommandHandler, filters
from telegram.ext import Updater

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
      context.application.create_task(conversion(update,context,application,"song").inLineKeyboardFeedback())

    elif bot_users[update.message.from_user.id] == 'album':
        context.application.create_task(conversion(update,context,application,"album").inLineKeyboardFeedback())



    else:
        await update.message.reply_text("Invalid Command: Please choose a valid command")




Token = '6199155011:AAFTpM4CN17p7fRZ4Y9n0vqHMEi2_vVYQCM'
# Token = '5865766343:AAECVqR7cMD2HNoJPGuOwQW4kXWtN45v1EE'
#print(bot.get_me())
# updater = telegram.ext.Updater(Token, use_context=True)

application = ApplicationBuilder().token(Token).build()
# start_handler = CommandHandler('start', start)
# application.add_handler(start_handler)




application.add_handler(telegram.ext.CommandHandler('album', album))
# application.add_handler(telegram.ext.CommandHandler('song',dang))
application.add_handler(telegram.ext.CommandHandler('song', song))
application.add_handler(telegram.ext.CommandHandler('start', start))
application.add_handler(telegram.ext.CommandHandler('help', help))
application.add_handler(telegram.ext.MessageHandler(filters.TEXT & (~filters.COMMAND),handle_message))



# application.add_handler(CallbackQueryHandler(song_callback, pattern='first_song'))
# application.add_handler(CallbackQueryHandler(song_callback, pattern='second_song'))
# application.add_handler(CallbackQueryHandler(song_callback, pattern='third_song'))
# application.add_handler(CallbackQueryHandler(album_callback, pattern='first_album'))
# application.add_handler(CallbackQueryHandler(album_callback, pattern='second_album'))
# application.add_handler(CallbackQueryHandler(album_callback, pattern='third_album'))





# disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
application.run_polling()



