# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 21:03:39 2023

@author: EMINEM
"""
import threading
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

from ytmusic import YTMusicapp




import os
#from pydub import AudioSegment




from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, TCOM, TCON, TDRC, TRCK, APIC
from mutagen.easyid3 import EasyID3



class conversion:

    searched_songs = {}
    searched_albums = {}

    def __init__(self):
        self.track_num=1


    def getsong(self, index):


        return (self.song_download(index))





    async def getalbum(index,instance_searched_albums_results):
        # self.album_downloaded_songs = []
        link = 'https://music.youtube.com/playlist?list='
        count = 0
        album_detailed_info = YTMusicapp.yt.get_album(instance_searched_albums_results[index][3])
        albumID = album_detailed_info['audioPlaylistId']
        album_link = link+albumID
        songs = {}


        album =  Playlist(album_link)

        for single_song in album.videos:



            a = YTMusicapp.yt.get_song(single_song.video_id)
            title = a['videoDetails']['title']



            #songs[count] = [title,album_detailed_info['artists'][0]['name'],[2000],album_detailed_info['thumbnails'][-1]['url']],[single_song.video_id]
            songs[count] = [title,instance_searched_albums_results[index][1], album_detailed_info['artists'][0]['name'], 2000, single_song.video_id,album_detailed_info['thumbnails'][-1]['url']]
            count+=1
        return songs










    async def song_download(index,instance_song_results):



        print('Starting song download for '+instance_song_results[index][0])
        link = 'https://music.youtube.com/watch?v='+instance_song_results[index][4]




        filename = instance_song_results[index][0]+".mp3"
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
            # self.album_downloaded_songs.append(audio_file)
            conversion.song_tagging(audio_file, index,instance_song_results)
            return audio_file
        except Exception as e:
            print(f"An error occured: {e}")
            await asyncio.create_task(conversion.song_download(index,instance_song_results))





        # audio_file = database.songs_root_location+"\\"+yt.title+".mp3"








    def song_tagging(filename,index,instance_song_results):


        artwork_url = instance_song_results[index][5]
        artwork_data = requests.get(artwork_url).content

        location = filename
        mp3file = EasyID3(location)
        mp3file["albumartist"] = instance_song_results[index][2]
        mp3file["artist"] = instance_song_results[index][2]
        mp3file["album"] = instance_song_results[index][1]
        mp3file["title"] = instance_song_results[index][0]
        mp3file["website"] = 't.me/mchoga'
        # mp3file["tracknumber"] = str(self.track_num)
        mp3file.save()
        # self.track_num+=1

        audio = ID3(filename)
        audio.save(v2_version=3)
        print('adding album art')

        audio = ID3(filename)
        with urllib.request.urlopen(artwork_url) as albumart:
            audio["APIC"] = APIC(
                encoding=3, mime="image/jpeg", type=3, desc="Cover", data=albumart.read()
            )
        audio.save(v2_version=3)






