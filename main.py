import time

import telegram.ext
from telegram.ext import CallbackQueryHandler

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
searched_songs_results = {}
searched_albums_results = {}
database.songs_root_location = os.path.join(os.path.dirname(os.path.abspath(__file__))) + "/Songs"
# database.songs_root_location = os.path.join(os.path.dirname(os.path.abspath(__file__))) + "\\Songs"
music = YTMusicapp
my_chat_ID =  1591024405

#music.YTmusicappclass.song_search("eminem")




def start(update, context):

    update.message.reply_text("Hello "+update.effective_chat.first_name+"!"+". My name is Morris, How can i help you today")


def song(update, context):
        global reply
        reply = "song"
        update.message.reply_text("Enter name of the song")





def album(update, context):
    global reply
    reply="album"
    
    update.message.reply_text("Enter name of the Album")
    


def help(update,context):
    update.message.reply_text("Choose any of the commands availavble to search and download a song or album")
    


def handle_message(update, context):
    global reply
    global searched_songs_results
    global searched_albums_results



    if reply == "song":
        database.track_num = 1
        mhinduro = ""
        music.YTmusicappclass.song_search(update.message.text)
        reply = "song_search_results"
        searched_songs_results = database.songs_searched_results


        for x in searched_songs_results:
            mhinduro += str(x+1) +'. ' + searched_songs_results[x][2] + " - " + searched_songs_results[x][0] + "\n"

        buttons = [[InlineKeyboardButton("1", callback_data="first_song",)],
                   [InlineKeyboardButton("2", callback_data="second_song")],
                   [InlineKeyboardButton("3", callback_data="third_song")]]
        context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons),
                                 text=mhinduro)
        #

        
        
        

    elif reply=="album":

        mhinduro = ""
        database.track_num = 1
        music.YTmusicappclass.album_search(update.message.text)
        reply = "album_search_results"
        searched_albums_results = database.albums_searched_results



        for x in searched_albums_results:
            mhinduro += str(x+1) +'. '+searched_albums_results[x][0] + " - " + searched_albums_results[x][1] + "\n"

        buttons = [[InlineKeyboardButton("1", callback_data="first_album")],
                   [InlineKeyboardButton("2", callback_data="second_album")],
                   [InlineKeyboardButton("3", callback_data="third_album")]]
        context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons),
                                 text=mhinduro)

        



    else:
        update.message.reply_text("Invalid Command: Please choose a valid command")

    
    
def song_callback(update, context):
    print("Processing...")
    chat_id = update.effective_chat.id
    query = update.callback_query
    path=None



    if query.data =="first_song":


        path = song_conversion.conversion().getsong(0)


        song = open(path,"rb")
        context.bot.send_document(chat_id, song)
        context.bot.send_message(my_chat_ID, "I provided song: " + database.songs_searched_results[0][0])
        song.close()
        database.album_downloaded_songs.clear()




    elif query.data =="second_song":
        path = song_conversion.conversion().getsong(1)

        song = open(path, "rb")
        context.bot.send_document(chat_id, song)
        context.bot.send_message(my_chat_ID, "I provided song: " + database.songs_searched_results[1][0])
        song.close()
    elif query.data == "third_song":
        path = song_conversion.conversion().getsong(2)

        song = open(path, "rb")
        context.bot.send_document(chat_id, song)
        context.bot.send_message(my_chat_ID, "I provided song: " + database.songs_searched_results[2][0])
        song.close()

    while True:
        try:
            os.remove(path)
            print(f"Song successfully deleted: ")
            break
        except OSError as e:
            if e.errno != 32:  # skip if error is not related to file lock
                raise
            print("Waiting to delete song")
            time.sleep(0.1)  # wait for 100ms before trying again


def album_callback(update, context):
    global my_chat_ID
    # Code to handle when the album button is pressed
    chat_id = update.effective_chat.id
    query = update.callback_query
    path = None
    print("Album downloading...")
    songs = database.album_downloaded_songs
    count = 0;


    if query.data =="first_album":

        song_conversion.conversion.getalbum(0)



    

        for number in database.songs_searched_results:
            conversion.song_download(number)
            path =database.album_downloaded_songs[count]
            song = open(path, "rb")
            context.bot.send_document(chat_id, song)


            song.close()
            count+=1

        context.bot.send_message(my_chat_ID, "I provided album: " + database.albums_searched_results[0][1])


        for path in database.album_downloaded_songs:
            while True:
                try:
                    os.remove(path)
                    print(f"Song successfully deleted: ")
                    break
                except OSError as e:
                    if e.errno != 32:  # skip if error is not related to file lock
                        raise
                    print("Waiting to delete song")
                    time.sleep(0.1)  # wait for 100ms before trying again
        database.album_downloaded_songs.clear()




    elif query.data =="second_album":
        song_conversion.conversion.getalbum(1)

       

        for number in database.songs_searched_results:
            conversion.song_download(number)
            path =database.album_downloaded_songs[count]
            song = open(path, "rb")
            context.bot.send_document(chat_id, song)
            song.close()
            count+=1
        context.bot.send_message(my_chat_ID, "I provided album: " + database.albums_searched_results[1][1])


        for path in database.album_downloaded_songs:
            while True:
                try:
                    os.remove(path)
                    print(f"Song successfully deleted: ")
                    break
                except OSError as e:
                    if e.errno != 32:  # skip if error is not related to file lock
                        raise
                    print("Waiting to delete song")
                    time.sleep(0.1)  # wait for 100ms before trying again
        database.album_downloaded_songs.clear()


    elif query.data == "third_album":
        song_conversion.conversion.getalbum(2)

        # for path in database.album_downloaded_songs:
        #     song = open(path, "rb")
        #     context.bot.send_document(chat_id, song)
        #     song.close()

        for number in database.songs_searched_results:
            conversion.song_download(number)
            path =database.album_downloaded_songs[count]
            song = open(path, "rb")
            context.bot.send_document(chat_id, song)
            song.close()
            count+=1
        context.bot.send_message(my_chat_ID, "I provided album: " + database.albums_searched_results[2][1])
        for path in database.album_downloaded_songs:
            while True:
                try:
                    os.remove(path)
                    print(f"Song successfully deleted: ")
                    break
                except OSError as e:
                    if e.errno != 32:  # skip if error is not related to file lock
                        raise
                    print("Waiting to delete song")
                    time.sleep(0.1)  # wait for 100ms before trying again

        database.album_downloaded_songs.clear()
        update.message.reply_text("**Enjoy** 😉")




    



Token = '6199155011:AAH8rBy3Ozypmbvzp5dOeYZE3fu-n4hCJqM'
#print(bot.get_me())
updater = telegram.ext.Updater(Token, use_context=True)
disp = updater.dispatcher





disp.add_handler(telegram.ext.CommandHandler('album', album))
disp.add_handler(telegram.ext.CommandHandler('song', song))
disp.add_handler(telegram.ext.CommandHandler('start', start))
disp.add_handler(telegram.ext.CommandHandler('help', help))


disp.add_handler(CallbackQueryHandler(song_callback, pattern='first_song'))
disp.add_handler(CallbackQueryHandler(song_callback, pattern='second_song'))
disp.add_handler(CallbackQueryHandler(song_callback, pattern='third_song'))
disp.add_handler(CallbackQueryHandler(album_callback, pattern='first_album'))
disp.add_handler(CallbackQueryHandler(album_callback, pattern='second_album'))
disp.add_handler(CallbackQueryHandler(album_callback, pattern='third_album'))



disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
updater.start_polling()
updater.idle()


