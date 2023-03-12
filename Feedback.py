import asyncio
import os
from datetime import time

from youtube_dll.song_conversion import conversion
from ytmusic import YTMusicapp
import telegram.ext
from telegram.ext import CallbackQueryHandler, ApplicationBuilder, CommandHandler, filters
from telegram.ext import Updater
from telegram import *
class Feedback:

    user_instances = {}





    def __init__(self,update,context,application,music_type):
        Feedback.user_instances[update.message.from_user.id] = self







        self.album_downloaded_songs = []
        self.searched_albums_results = {} #Object renewed when called
        self.searched_songs_results = {}

        self.application = application
        self.music_type = music_type
        self.context = context
        self.update = update
        instance = self

        self.application.add_handler(CallbackQueryHandler(self.song_callback, pattern='first_song',block=False))
        self.application.add_handler(CallbackQueryHandler(self.song_callback, pattern='second_song',block=False))
        self.application.add_handler(CallbackQueryHandler(self.song_callback, pattern='third_song',block=False))
        self.application.add_handler(CallbackQueryHandler(self.album_callback, pattern='first_album', block=False))
        self.application.add_handler(CallbackQueryHandler(self.album_callback, pattern='second_album',block=False))
        self.application.add_handler(CallbackQueryHandler(self.album_callback, pattern='third_album',block=False))

    async def inLineKeyboardFeedback(self):




        if self.music_type == "song":

            mhinduro = ""

            self.searched_songs_results = YTMusicapp.YTmusicappclass.song_search(self.update.message.text) #Changes new object


            for x in self.searched_songs_results:
                mhinduro += str(x + 1) + '. ' + self.searched_songs_results[x][2] + " - " + self.searched_songs_results[x][
                    0] + "\n"

            buttons = [[InlineKeyboardButton("1", callback_data="first_song", )],
                       [InlineKeyboardButton("2", callback_data="second_song")],
                       [InlineKeyboardButton("3", callback_data="third_song")]]


            await self.context.bot.send_message(chat_id=self.update.effective_chat.id,
                                                reply_markup=InlineKeyboardMarkup(buttons),
                                                text=mhinduro)

        elif self.music_type == "album":


            mhinduro = ""
            self.searched_albums_results = YTMusicapp.YTmusicappclass.album_search(self.update.message.text)








            for x in self.searched_albums_results:
                mhinduro += str(x+1) +'. '+self.searched_albums_results[x][0] + " - " + self.searched_albums_results[x][1] + "\n"

            buttons = [[InlineKeyboardButton("1", callback_data="first_album")],
                       [InlineKeyboardButton("2", callback_data="second_album")],
                       [InlineKeyboardButton("3", callback_data="third_album")]]
            await self.context.bot.send_message(chat_id=self.update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons),
                                     text=mhinduro)




    async def song_callback(self,update, context):

        instance_song_results = Feedback.user_instances[update.callback_query.from_user.id].searched_songs_results
        print("Processing...")
        chat_id = update.effective_chat.id
        query = update.callback_query
        path = None




        if query.data == "first_song":
            path = await asyncio.create_task(conversion.getsong(0,instance_song_results))

            while True:
                try:
                    song = open(path, "rb")
                    break
                except TypeError as e:
                    print("An error Occured " + e)



            await context.bot.send_document(chat_id, song)
            await context.bot.send_message(chat_id, "I provided song: " + instance_song_results[0][0])
            song.close()

        elif query.data == "second_song":
            path  = await asyncio.create_task(conversion.getsong(1,instance_song_results))

            while True:
                try:
                    song = open(path, "rb")
                    break
                except TypeError as e:
                    print("An error Occured " + e)

            await context.bot.send_document(chat_id, song)
            await context.bot.send_message(1591024405, "I provided song: " + instance_song_results[1][0])
            song.close()

        elif query.data == "third_song":
            path = await asyncio.create_task(conversion.getsong(2,instance_song_results))

            while True:
                try:
                    song = open(path, "rb")
                    break
                except TypeError as e:
                    print("An error Occured " + e)


            await context.bot.send_document(chat_id, song)
            await context.bot.send_message(1591024405, "I provided song: " + instance_song_results[2][0])
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

    async def album_callback(self,update, context):
        final_album = []

        albums = Feedback.user_instances[update.callback_query.from_user.id].searched_albums_results

        # Code to handle when the album button is pressed
        chat_id = update.effective_chat.id
        query = update.callback_query
        path = None
        print("Album downloading...")
        songs = albums
        count = 0;

        if query.data == "first_album":

            instance_song_results = await asyncio.create_task(conversion.getalbum(0,albums))

            for number in instance_song_results:
                track = await asyncio.create_task(conversion.song_download(number,instance_song_results))
                final_album.append(track)


                # path = self.album_downloaded_songs[count]
                path = track

                while True:
                    try:
                        song = open(path, "rb")
                        break
                    except TypeError as e:
                        print("An error Occured " + e)

                await context.bot.send_document(chat_id, song)

                song.close()
                count += 1

            await context.bot.send_message(1591024405, "I provided album: " + albums[0][1])

            for path in final_album:
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





        elif query.data == "second_album":
            instance_song_results = await asyncio.create_task(conversion.getalbum(1,albums))

            for number in instance_song_results:
                track = await asyncio.create_task(conversion.song_download(number, instance_song_results))
                final_album.append(track)
                path = track

                while True:
                    try:
                        song = open(path, "rb")
                        break
                    except TypeError as e:
                        print("An error Occured " + e)


                await context.bot.send_document(chat_id, song)
                song.close()
                count += 1
            await context.bot.send_message(1591024405, "I provided album: " + albums[1][1])

            for path in final_album:
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



        elif query.data == "third_album":
            instance_song_results = await asyncio.create_task(conversion.getalbum(2,albums))


            for number in instance_song_results:
                track = await asyncio.create_task(conversion.song_download(number,instance_song_results))
                final_album.append(track)
                path = track

                while True:
                    try:
                        song = open(path, "rb")
                        break
                    except TypeError as e:
                        print("An error Occured " + e)

                await context.bot.send_document(chat_id, song)
                song.close()
                count += 1
            await context.bot.send_message(1591024405, "I provided album: " + albums[2][1])
            for path in final_album:
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



        await context.bot.send_message(chat_id, "**Enjoy** 😉")






