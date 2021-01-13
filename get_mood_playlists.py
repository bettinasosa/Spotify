from pprint import pprint
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy
import spotipy.util as util
from dotenv import load_dotenv
import csv
import pandas as pd

load_dotenv()
client_credentials_manager = SpotifyClientCredentials()

# A dictionary of playlists and their spotify ID. Selected by popularity and genre. This will conform our database.

playlists = {'happy': ['37i9dQZF1DX2FsCLsHeMrM', '1EBXLInFVBEEr8pi2upj3a',
                       '3UY9GMgt4123xs7PzdFhIL', '3sxujeqA2ns5ef1jmda5WR', '37i9dQZF1DWXqpDKK4ed9O',
                       '37i9dQZF1DXc3KygMa1OE7', '37i9dQZF1DX8FwnYE6PRvL', '0u64r7ofIxyNBsvfXnVl9R'],
             'study': ['1qS8XvaEn0brfJyNjsBOdP', '37i9dQZF1DWSw8liJZcPOI', '37i9dQZF1DX9sIqqvKsjG8',
                       '37i9dQZF1DX8NTLI2TtZa6', '37i9dQZF1DX8Uebhn9wzrS', '37i9dQZF1DX692WcMwL2yW',
                       '37i9dQZF1DXd5zUwdn6lPb', '5zX5kOmh7ib6Xy52GxHhBL'],
             'energetic': ['4v5d07rx6XmeZ0bqFcWv2l', '37i9dQZF1DXdxcBWuJkbcy', '37i9dQZF1DX76Wlfdnj7AP',
                           '37i9dQZF1DWUVpAXiEPK8P', '37i9dQZF1DXaXB8fQg7xif',
                           '37i9dQZF1DX8a1tdzq5tbM', '37i9dQZF1DX5Ozry5U6G0d'],
             'chill': ['6tsMG3CI6cwpQZPjIvRaEk', '2GfLRoD5RzuU3qGBJwI5TT', '37i9dQZF1DWWQRwui0ExPn',
                       '37i9dQZF1DX4WYpdgoIcn6', '7ozIozDp260fjNOZy1yzRG'
                       ]
             }

scope = 'playlist-read-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
trackLists = []
tracks_with_features = []
for genre in playlists:
    sp = spotipy.Spotify(
        client_credentials_manager=client_credentials_manager)
    genre = str(genre)
    print(genre)
    for pl_id in playlists[str(genre)]:
        # print(pl_id)
        offset = 0
        response = sp.playlist_items(pl_id,
                                     offset=offset,
                                     fields='items.track.id,items.track.name',
                                     additional_types=['track'])

        for i, item in enumerate(response['items']):
            trackLists.append(
                dict(track=item['track'], mood=genre))

for song in trackLists:
    track_id = song['track']['id']
    # print(track_id)
    if track_id != None:
        sp = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager)
        meta = sp.track(track_id)
        features = sp.audio_features(track_id)

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
            mood=song['mood']))
    else:
        pass

csv_columns = ['name', 'album', 'artist', 'id', 'release_date', 'popularity', 'length', 'danceability', 'acousticness', 'energy', 'instrumentalness',
               'liveness', 'valence', 'loudness', 'speechiness', 'tempo', 'key', 'time_signature', 'mood']
csv_file = "moods1.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in tracks_with_features:
            writer.writerow(data)

    dat = pd.read_csv("moods1.csv")
    dat.drop_duplicates(subset="name", keep=False)
    dat.to_csv('moods.csv')
except IOError:
    print("I/O error")

""" 'energetic': ['37i9dQZF1DXdxcBWuJkbcy', '37i9dQZF1DX76Wlfdnj7AP',
                           '37i9dQZF1DWUVpAXiEPK8P', '37i9dQZF1DXaXB8fQg7xif',
                           '37i9dQZF1DX8a1tdzq5tbM', '37i9dQZF1DX5Ozry5U6G0d'
                           ],
             'chill': ['6tsMG3CI6cwpQZPjIvRaEk', '2GfLRoD5RzuU3qGBJwI5TT', '37i9dQZF1DWWQRwui0ExPn'
                       ],
             'happy': ['37i9dQZF1DX2FsCLsHeMrM' '1EBXLInFVBEEr8pi2upj3a',
                       '3UY9GMgt4123xs7PzdFhIL', '3sxujeqA2ns5ef1jmda5WR', '37i9dQZF1DWXqpDKK4ed9O',
                       '37i9dQZF1DXc3KygMa1OE7', '37i9dQZF1DX8FwnYE6PRvL'
                       ],
             'study': ['1qS8XvaEn0brfJyNjsBOdP', '37i9dQZF1DWSw8liJZcPOI', '37i9dQZF1DX9sIqqvKsjG8',
                       '37i9dQZF1DX8NTLI2TtZa6', '37i9dQZF1DX8Uebhn9wzrS', '37i9dQZF1DX692WcMwL2yW',
                       '37i9dQZF1DXd5zUwdn6lPb'
                       ] """
