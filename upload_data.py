#!/usr/bin/env python
# coding: utf-8

import time
from pymongo import MongoClient
import requests
import pandas as pd
from pprint import pprint
import csv
import os
import json
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
from datetime import datetime
from ml import predict_mood

load_dotenv()

client_credentials_manager = SpotifyClientCredentials()

scope = 'user-top-read'

client = MongoClient(
    "mongodb+srv://gorgodar:gorgodar@cluster0.z77hp.mongodb.net/Spotify?retryWrites=true&w=majority")
db = client.Spotify

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
sp_range = ['short_term']
results = sp.current_user_top_tracks(time_range=sp_range, limit=20)
trackList = []
for i, item in enumerate(results['items']):
    trackList.append(
        dict(name=item['name'], id=item['id'],
             artist=item['artists'][0]['name']))
# print(i, item['name'], '//', item['artists'][0]['name'], '//', item['id'])
# return trackList

tracks_with_features = []
data = []
for i in trackList:
    track_id = i['id']
    sp = spotipy.Spotify(
        client_credentials_manager=client_credentials_manager)
    features = sp.audio_features(track_id)
    f = features[0]
    m = predict_mood(track_id)
    tracks_with_features.append(dict(
        name=i['name'],
        artist=i['artist'],
        id=i['id'],
        danceability=f['danceability'],
        energy=f['energy'],
        loudness=f['loudness'],
        speechiness=f['speechiness'],
        acousticness=f['acousticness'],
        tempo=f['tempo'],
        liveness=f['liveness'],
        valence=f['valence'],
        mood=m
    ))

data.append(dict(tracks=tracks_with_features,
                 time=datetime.now()))
db.Spotify.insert_many(data)
print(tracks_with_features[0])
pprint(tracks_with_features)
