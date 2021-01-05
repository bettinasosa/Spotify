import csv
import os
import json
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import time
from IPython.core.display import clear_output
from dotenv import load_dotenv
load_dotenv()

client_credentials_manager = SpotifyClientCredentials()

scope = 'user-top-read'
scope1 = 'playlist-read-private'


def get_playlists():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    results = sp.user_playlists('bettsr12', limit=20)
    playList = []
    for i, item in enumerate(results['items']):
        playList.append(
            dict(name=item["name"], id=item['id']))
        #print(i, item['name'], '//', item['id'])
    return playList


x = get_playlists()
x
