# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 21:03:39 2023

@author: EMINEM
"""
import asyncio
import inspect
import urllib
from datetime import time

import requests
from ytmusicapi import YTMusic

import database
from ytmusic import YTMusicapp
#import youtube_dl
from pytube import YouTube
from moviepy.editor import *
from pytube import Playlist
import telegram.ext
from telegram.ext import CallbackQueryHandler, ApplicationBuilder, CommandHandler, filters
from telegram.ext import Updater
from telegram import *
from ytmusic import YTMusicapp



import os
#from pydub import AudioSegment




from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, TCOM, TCON, TDRC, TRCK, APIC
from mutagen.easyid3 import EasyID3



class conversion:
    track_num = 1
    searched_songs = {}



    def __init__(self,update,context,application,music_type):


        self.application = application
        self.music_type = music_type
        self.context = context
        self.update = update
        print('__init__')




        # asyncio.create_task(self.inLineKeyboardFeedback())

        # self.application.add_handler(telegram.ext.CommandHandler('filters', inLineKeyboardFeedback))
        self.application.add_handler(CallbackQueryHandler(self.song_callback, pattern='first_song'))
        self.application.add_handler(CallbackQueryHandler(self.song_callback, pattern='second_song'))
        self.application.add_handler(CallbackQueryHandler(self.song_callback, pattern='third_song'))
        # self.application.add_handler(CallbackQueryHandler(album_callback, pattern='first_album'))
        # self.application.add_handler(CallbackQueryHandler(album_callback, pattern='second_album'))
        # self.application.add_handler(CallbackQueryHandler(album_callback, pattern='third_album'))


    async def inLineKeyboardFeedback(self):
        global searched_songs







        if self.music_type == "song":

            mhinduro = ""
            # music.YTmusicappclass.song_search(update.message.text)
            # searched_songs_results = database.songs_searched_results
            self.searched_songs_results = await asyncio.create_task(YTMusicapp.YTmusicappclass.song_search(self.update.message.text))
            searched_songs = self.searched_songs_results

            for x in self.searched_songs_results:
                mhinduro += str(x + 1) + '. ' + self.searched_songs_results[x][2] + " - " + self.searched_songs_results[x][
                    0] + "\n"

            buttons = [[InlineKeyboardButton("1", callback_data="first_song", )],
                       [InlineKeyboardButton("2", callback_data="second_song")],
                       [InlineKeyboardButton("3", callback_data="third_song")]]

            await self.context.bot.send_message(chat_id=self.update.effective_chat.id,
                                           reply_markup=InlineKeyboardMarkup(buttons),
                                           text=mhinduro)

    async def song_callback(self,update, context):
        global searched_songs
        self.searched_songs_results = searched_songs
        print("Processing...")
        chat_id = update.effective_chat.id
        query = update.callback_query
        path = None
        print(self.searched_songs_results)


        if query.data == "first_song":
            path = await asyncio.create_task(self.getsong(0))


            song = open(path, "rb")
            await context.bot.send_document(chat_id, song)
            await context.bot.send_message(chat_id, "I provided song: " + self.searched_songs_results[0][0])
            song.close()

        elif query.data == "second_song":
            path  = await asyncio.create_task(self.getsong(1))


            song = open(path, "rb")
            await context.bot.send_document(chat_id, song)
            await context.bot.send_message(1591024405, "I provided song: " + self.searched_songs_results[1][0])
            song.close()
        elif query.data == "third_song":
            path = await asyncio.create_task(self.getsong(2))


            song = open(path, "rb")
            context.bot.send_document(chat_id, song)
            context.bot.send_message(1591024405, "I provided song: " + self.searched_songs_results[2][0])
            song.close()

        while True:
            print('Damn man')
            try:
                os.remove(path)
                print(f"Song successfully deleted: ")
                break
            except OSError as e:
                if e.errno != 32:  # skip if error is not related to file lock
                    raise
                print("Waiting to delete song")
                time.sleep(0.1)  # wait for 100ms before trying again

    # elif reply == "album":
    #
    #     mhinduro = ""
    #     database.track_num = 1
    #     music.YTmusicappclass.album_search(update.message.text)
    #     reply = "album_search_results"
    #     searched_albums_results = database.albums_searched_results
    #
    #     for x in searched_albums_results:
    #         mhinduro += str(x + 1) + '. ' + searched_albums_results[x][0] + " - " + searched_albums_results[x][
    #             1] + "\n"
    #
    #     buttons = [[InlineKeyboardButton("1", callback_data="first_album")],
    #                [InlineKeyboardButton("2", callback_data="second_album")],
    #                [InlineKeyboardButton("3", callback_data="third_album")]]
    #     context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons),
    #                              text=mhinduro)

    def getsong(self, index):

        return (self.song_download(index))





    def getalbum(index):
        link = 'https://music.youtube.com/playlist?list='
        count = 0
        album_detailed_info =YTMusicapp.yt.get_album(database.albums_searched_results[index][3])
        albumID = album_detailed_info['audioPlaylistId']
        album_link = link+albumID
        songs = {}


        album =  Playlist(album_link)

        for single_song in album.videos:



            a =YTMusicapp.yt.get_song(single_song.video_id)
            title = a['videoDetails']['title']



            #songs[count] = [title,album_detailed_info['artists'][0]['name'],[2000],album_detailed_info['thumbnails'][-1]['url']],[single_song.video_id]
            songs[count] = [title,database.albums_searched_results[index][1], album_detailed_info['artists'][0]['name'], 2000, single_song.video_id,album_detailed_info['thumbnails'][-1]['url']]
            count+=1
        database.songs_searched_results = songs
        # for num in songs:
        #     conversion.song_download(num)










    async def song_download(self,index):

        print(self.searched_songs_results)

        print('Starting song download for '+self.searched_songs_results[index][0])
        link = 'https://music.youtube.com/watch?v='+self.searched_songs_results[index][4]



        #song_info = youtube_dl.YoutubeDL().extract_info(url=link, download=False)
        #filename = f"{song_info['title']}.mp3"
        filename = self.searched_songs_results[index][0]+".mp3"
        try:
            yt = YouTube(link)
            yt.title = "".join([c for c in yt.title if c not in ['/', '\\', '|', '?', '*', ':', '>', '<', '"']])

            video = yt.streams.filter(only_audio=True).first()

            vid_file = video.download(output_path=database.songs_root_location)

            base = os.path.splitext(vid_file)[0]
            audio_file = base + ".mp3"

            mp4_no_frame = AudioFileClip(vid_file)

            mp4_no_frame.write_audiofile(audio_file, logger=None)
            mp4_no_frame.close()

            os.remove(vid_file)
            os.replace(audio_file, database.songs_root_location + "/" + yt.title + ".mp3")
            # os.replace(audio_file, database.songs_root_location+"\\"+yt.title+".mp3")
            audio_file = database.songs_root_location + "/" + yt.title + ".mp3"
            # database.album_downloaded_songs.append(audio_file)
            self.song_tagging(audio_file, index)
            return audio_file
        except Exception as e:
            print(f"An error occured: {e}")
            self.song_download(index)



        # audio_file = database.songs_root_location+"\\"+yt.title+".mp3"








    def song_tagging(self,filename,index):


        artwork_url = self.searched_songs_results[index][5]
        artwork_data = requests.get(artwork_url).content

        location = filename
        mp3file = EasyID3(location)
        mp3file["albumartist"] = self.searched_songs_results[index][2]
        mp3file["artist"] = self.searched_songs_results[index][2]
        mp3file["album"] = self.searched_songs_results[index][1]
        mp3file["title"] = self.searched_songs_results[index][0]
        mp3file["website"] = 't.me/mchoga'
        mp3file["tracknumber"] = str(self.track_num)
        mp3file.save()
        self.track_num+=1

        audio = ID3(filename)
        audio.save(v2_version=3)
        print('adding album art')

        audio = ID3(filename)
        with urllib.request.urlopen(artwork_url) as albumart:
            audio["APIC"] = APIC(
                encoding=3, mime="image/jpeg", type=3, desc="Cover", data=albumart.read()
            )
        audio.save(v2_version=3)






