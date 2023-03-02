# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 17:18:10 2023

@author: EMINEM
"""
import requests
from pytube import YouTube
from ytmusicapi.parsers import browsing
from ytmusicapi import YTMusic
import os
import database



#header = "D:\\ShadyBot\\ytmusic\\header.json"
header = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'header.json')

#song - https://music.youtube.com/watch?v=ZB0eUo6rtM0
#album - https://music.youtube.com/playlist?list=


yt = YTMusic(header)


class YTmusicappclass():
    


        

    def song_search(song_name):
        songs = {}
        count = 0
        print("Searching for song... "+song_name)
        results = yt.search(song_name, filter="songs")
        
        for x in results[0:3]:

            
            #title - artistName  - album  - year - videoID  - thumbnail
            songs[count] = [x['title'], x['album']['name'], x['artists'][0]['name'], x['year'], x['videoId'], x['thumbnails'][-1]['url']]

            albumid = x['album']['id']
            album = yt.get_album(albumid)
            songs[count][5] = album['thumbnails'][-1]['url']












            count += 1
            

        database.songs_searched_results = songs
       
       
    def album_search(album_name):
        count = 0
        albums = {}
        print("Searching for album... "+album_name)
        results = yt.search(album_name, filter="albums")


        for x in results[0:3]:
            albums[count] = [x['artists'][0]['name'], x['title'], x['year'], x['browseId'], x['thumbnails'][-1]['url']]
            count += 1

        database.albums_searched_results = albums




