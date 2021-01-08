
#!/usr/bin/env python 3.7.4
# coding: utf-8

from pprint import pprint
from pymongo import MongoClient
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
import os
import time
from datetime import datetime


# music played in the last hour, as script will run every hour
millis = int(round(time.time() * 1000 - 3600000))

# loading client credentials
load_dotenv()

# specifying necessary authentications and scope
client_credentials_manager = SpotifyClientCredentials()
scope = 'user-read-recently-played'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# mongo client and database I am sending the document to
password = os.getenv("password", "")
client = MongoClient(
    "mongodb+srv://gorgodar:{0}@cluster0.z77hp.mongodb.net/Spotify?retryWrites=true & w=majority".format(password))
db = client.Spotify

# getting recently played songs maximum 20 (normally I don't play more that 16 songs in an hour)
results = sp.current_user_recently_played(limit=20, after=millis)
trackList = []
trackLists = []
for i, item in enumerate(results['items']):
    trackLists.append(
        dict(name=item['track']))

# pprint(trackLists[0])

# Getting all the track features
tracks_with_features = []
data = []
for song in trackLists:
    track_id = song['name']['id']
    #name = song['name']['name']
    sp = spotipy.Spotify(
        client_credentials_manager=client_credentials_manager)
    meta = sp.track(track_id)
    features = sp.audio_features(track_id)
    # pprint(name)

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

# putting the data in the correct format to send to mongo
data.append(dict(tracks=tracks_with_features,
                 time=datetime.now()))
db.Spotify.insert_many(data)

# pprint(name)
