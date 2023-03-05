# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 21:03:39 2023

@author: EMINEM
"""
import inspect
import urllib

import requests
from ytmusicapi import YTMusic

import database
from ytmusic import YTMusicapp
#import youtube_dl
from pytube import YouTube
from moviepy.editor import *
from pytube import Playlist



import os
#from pydub import AudioSegment




from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, TCOM, TCON, TDRC, TRCK, APIC
from mutagen.easyid3 import EasyID3



class conversion:



    def getsong(self,index):

        return (conversion.song_download(index))



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










    def song_download(index):



        print('Starting song download for '+database.songs_searched_results[index][0])
        # link = 'https://music.youtube.com/watch?v='+database.songs_searched_results[index][4]
        link = 'https://music.youtube.com/watch?v=abc'


        #song_info = youtube_dl.YoutubeDL().extract_info(url=link, download=False)
        #filename = f"{song_info['title']}.mp3"
        filename = database.songs_searched_results[index][0]+".mp3"
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
        except Exception as e:
            print(f"An error occured: {e}")

        audio_file = database.songs_root_location+"/"+yt.title+".mp3"
        # audio_file = database.songs_root_location+"\\"+yt.title+".mp3"

        database.album_downloaded_songs.append(audio_file)
        conversion().song_tagging(audio_file,index)
        return audio_file






    def song_tagging(self,filename,index):

            artwork_url = database.songs_searched_results[index][5]
            artwork_data = requests.get(artwork_url).content

            location = filename
            mp3file = EasyID3(location)
            mp3file["albumartist"] = database.songs_searched_results[index][2]
            mp3file["artist"] = database.songs_searched_results[index][2]
            mp3file["album"] = database.songs_searched_results[index][1]
            mp3file["title"] = database.songs_searched_results[index][0]
            mp3file["website"] = 't.me/mchoga'
            mp3file["tracknumber"] = str(database.track_num)
            mp3file.save()
            database.track_num+=1

            audio = ID3(filename)
            audio.save(v2_version=3)
            print('adding album art')

            audio = ID3(filename)
            with urllib.request.urlopen(artwork_url) as albumart:
                audio["APIC"] = APIC(
                    encoding=3, mime="image/jpeg", type=3, desc="Cover", data=albumart.read()
                )
            audio.save(v2_version=3)








