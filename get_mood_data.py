import csv
import os
import json
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
load_dotenv()

client_credentials_manager = SpotifyClientCredentials()

scope = 'user-top-read'


# def get_top_tracks(scope, sp):
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
for i in trackList:
    track_id = i['id']
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    features = sp.audio_features(track_id)
    f = features[0]
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
        valence=f['valence']
    ))
print(tracks_with_features[0])

csv_columns = ['name', 'artist', 'id', 'danceability',
               'energy', 'loudness', 'speechiness', 'acousticness', 'tempo', 'liveness', 'valence']
csv_file = "Mood_data.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in tracks_with_features:
            writer.writerow(data)
except IOError:
    print("I/O error")
