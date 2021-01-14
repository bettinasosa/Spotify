from pprint import pprint
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy
import spotipy.util as util
from dotenv import load_dotenv
import csv
import pandas as pd
import time
import sys
import pymongo
import os
from pymongo import MongoClient
from ml import predict_mood

# this script periodically adds the new songs I am listening.
# In this way when the ml algorithm will become more and more informed as time goes by.

while True:
    try:
        load_dotenv()
        client_credentials_manager = SpotifyClientCredentials()

        # music played in the last hour, as script will run every hour
        millis = int(round(time.time() * 1000 - 3600000))

        # specifying necessary authentications and scope
        client_credentials_manager = SpotifyClientCredentials()
        scope = 'user-read-recently-played'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

        # mongo client and database I am sending the document to
        password = os.getenv("password")
        client = MongoClient(
            "mongodb+srv://gorgodar:{0}@cluster0.z77hp.mongodb.net/activity?retryWrites=true&w=majority".format(password))
        db = client.Spotify

        # getting recently played songs maximum 20 (normally I don't play more that 16 songs in an hour)
        results = sp.current_user_recently_played(limit=20, after=millis)
        trackList = []
        trackLists = []
        for i, item in enumerate(results['items']):
            trackLists.append(
                dict(name=item['track']))

        tracks_with_features = []
        for song in trackLists:
            track_id = song['name']['id']
            # Getting the mood
            sp = spotipy.Spotify(
                client_credentials_manager=client_credentials_manager)
            meta = sp.track(track_id)
            features = sp.audio_features(track_id)
            )
                tracks_with_features.append(dict(
                    name=meta['name'],
                    album=meta['album']['name'],
                    artist=meta['album']['artists'][0]['name'],
                    release_date=meta['album']['release_date'],
                    length=meta['duration_ms'],
                    popularity=meta['popularity'],
                    id=meta['id'],
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
                    time_signature=features[0]['time_signature'],
                    mood=predict_mood(track_id))

        csv_columns = ['name', 'album', 'artist', 'id', 'release_date', 'popularity', 'length', 'danceability', 'acousticness', 'energy', 'instrumentalness',
                       'liveness', 'valence', 'loudness', 'speechiness', 'tempo', 'key', 'time_signature', 'mood']
        csv_file = "moods.csv"
        try:
            # using 'a' will append new elements to the file instead of overwriting it
            with open(csv_file, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                for data in tracks_with_features:
                    writer.writerow(data)
        except IOError:
            print("I/O error")
        time.sleep(3600)
    except KeyboardInterrupt:
        # quit
        sys.exit()
