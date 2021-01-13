#!/usr/bin/env python 3.7.4
# coding: utf-8

import time
from pymongo import MongoClient
from pprint import pprint
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
from datetime import datetime
import pymongo

# loading client credentials
load_dotenv()

# specifying necessary authentications and scope
client_credentials_manager = SpotifyClientCredentials()
scope = 'user-top-read'

# mongo client and database I am sending the document to
password = os.getenv("password", "")
client = MongoClient(
    "mongodb+srv://gorgodar:{0}@cluster0.z77hp.mongodb.net/Spotify?retryWrites=true&w=majority".format(password))
db = client.Spotify

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
sp_range = ['short_term']
results = sp.current_user_top_tracks(time_range=sp_range, limit=20)
trackList = []
for i, item in enumerate(results['items']):
    trackList.append(item['id'])
# print(i, item['name'], '//', item['artists'][0]['name'], '//', item['id'])

# getting my top played tracked in the past few days
tracks_with_features = []
data = []
for i in trackList:
    sp = spotipy.Spotify(
        client_credentials_manager=client_credentials_manager)
    meta = sp.track(i)
    features = sp.audio_features(i)

    tracks_with_features.append(dict(
        name=meta['name'],
        album=meta['album']['name'],
        artist=meta['album']['artists'][0]['name'],
        release_date=meta['album']['release_date'],
        length=meta['duration_ms'],
        popularity=meta['popularity'],
        ids=meta['id'],
        acousticness=features[0]['acousticness'],
        danceability=features[0]['danceability'],
        energy=features[0]['energy'],
        instrumentalness=features[0]['instrumentalness'],
        liveness=features[0]['liveness'],
        valence=features[0]['valence'],
        loudness=features[0]['loudness'],
        speechiness=features[0]['speechiness'],
        tempo=features[0]['tempo'],
        key=features[0]['key'],
        time_signature=features[0]['time_signature']))

""" data.append(dict(tracks=tracks_with_features,
                 time=datetime.now()))
db.Spotify.insert_many(data) """
pprint(tracks_with_features[0])
# pprint(tracks_with_features)
