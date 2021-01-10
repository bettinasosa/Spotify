from pprint import pprint
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy
import spotipy.util as util
from dotenv import load_dotenv
import csv

load_dotenv()
client_credentials_manager = SpotifyClientCredentials()

# A dictionary of playlists and their spotify ID. Selected by popularity and genre. This will conform our database.

playlists = {'romantic': ['37i9dQZF1DX50QitC6Oqtn', '37i9dQZF1DWXqpDKK4ed9O',
                          '37i9dQZF1DX09mi3a4Zmox', '37i9dQZF1DXc3KygMa1OE7',
                          '37i9dQZF1DWYMvTygsLWlG', '37i9dQZF1DWUoGbRYcteyC',
                          '37i9dQZF1DX5IDTimEWoTd'
                          ],
             'energetic': ['37i9dQZF1DXdxcBWuJkbcy', '37i9dQZF1DX76Wlfdnj7AP',
                           '37i9dQZF1DWUVpAXiEPK8P', '37i9dQZF1DXaXB8fQg7xif',
                           '37i9dQZF1DX8a1tdzq5tbM', '37i9dQZF1DX8FwnYE6PRvL',
                           '37i9dQZF1DX5Ozry5U6G0d'
                           ],
             'chill': ['37i9dQZF1DX4WYpdgoIcn6', '37i9dQZF1DWTwnEm1IYyoj',
                       '37i9dQZF1DWWQRwui0ExPn', '37i9dQZF1DX6VdMW310YC7',
                       '37i9dQZF1DX504r1DvyvxG', '37i9dQZF1DX2TRYkJECvfC',
                       '37i9dQZF1DX0SM0LYsmbMT'
                       ],
             'cheerful': ['37i9dQZF1DXdPec7aLTmlC', '37i9dQZF1DX3rxVfibe1L0',
                          '37i9dQZF1DX7KNKjOK0o75', '37i9dQZF1DWSf2RDTDayIx',
                          '37i9dQZF1DX9XIFQuFvzM4', '37i9dQZF1DXca8AyWK6Y7g'
                          ],
             'sad': ['7i9dQZF1DX4yeSNLFx6qI', '37i9dQZF1DXbrUpGvoi3TS',
                     '37i9dQZF1DWX83CujKHHOn', '37i9dQZF1DX3YSRoSdA634',
                     '37i9dQZF1DWVxpHBekDUXK', '37i9dQZF1DWZrc3lwvImLj'
                     ]
             }

scope = 'playlist-read-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
trackLists = []
trackList = []

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
            dict(track=item['track']))
    tracks_with_features = []
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
                mood=genre))
            # print(tracks_with_features[0])
        else:
            pass

csv_columns = ['name', 'album', 'artist', 'id', 'release_date', 'popularity', 'length', 'danceability', 'acousticness', 'energy', 'instrumentalness',
               'liveness', 'valence', 'loudness', 'speechiness', 'tempo', 'key', 'time_signature', 'genre']
csv_file = "moods_dataset.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in tracks_with_features:
            writer.writerow(data)
except IOError:
    print("I/O error")


""" # Ignore this (for me to know which playlist is which)
# Romance genre
romantic1 = '37i9dQZF1DX50QitC6Oqtn'  # love pop
romantic2 = '37i9dQZF1DWXqpDKK4ed9O'  # 90s love songs
romantic3 = '37i9dQZF1DX09mi3a4Zmox'  # baladas romanticas
romantic4 = '37i9dQZF1DXc3KygMa1OE7'  # 80s love songs (my favourite :)
romantic5 = '37i9dQZF1DWYMvTygsLWlG'  # Love ballas
romantic6 = '37i9dQZF1DWUoGbRYcteyC'  # Amor Amor (some spanish music too)
romantic7 = '37i9dQZF1DX5IDTimEWoTd'  # Warm fuzzy feeling

# energetic genre
energetic1 = '37i9dQZF1DXdxcBWuJkbcy'  # Motivation mix
energetic2 = '37i9dQZF1DX76Wlfdnj7AP'  # Beast Mode
energetic3 = '37i9dQZF1DWUVpAXiEPK8P'  # power workout
energetic4 = '37i9dQZF1DXaXB8fQg7xif'  # dance party
energetic5 = '37i9dQZF1DX8a1tdzq5tbM'  # Dance classics
energetic6 = '37i9dQZF1DX8FwnYE6PRvL'  # Rock party (good good)
energetic7 = '37i9dQZF1DX5Ozry5U6G0d'  # Summer party

# chill genre
chill1 = '37i9dQZF1DX4WYpdgoIcn6'  # chill hits
chill2 = '37i9dQZF1DWTwnEm1IYyoj'  # soft pop hits
chill3 = '37i9dQZF1DWWQRwui0ExPn'  # Lo-Fi hits
chill4 = '37i9dQZF1DX6VdMW310YC7'  # chill tracks
chill5 = '37i9dQZF1DX504r1DvyvxG'  # classic acoustics
chill6 = '37i9dQZF1DX2TRYkJECvfC'  # deep house relax
chill7 = '37i9dQZF1DX0SM0LYsmbMT'  # jazz vibes (the best one of this section)

# cheerful genre
cheerful1 = '37i9dQZF1DXdPec7aLTmlC'  # happy hits
cheerful2 = '37i9dQZF1DX3rxVfibe1L0'  # mood booster
cheerful3 = '37i9dQZF1DX7KNKjOK0o75'  # Have a great day!
cheerful4 = '37i9dQZF1DWSf2RDTDayIx'  # happy beats
cheerful5 = '37i9dQZF1DX9XIFQuFvzM4'  # feelin' good
cheerful6 = '37i9dQZF1DXca8AyWK6Y7g'  # Young and free

# sad genre
sad1 = '7i9dQZF1DX4yeSNLFx6qI'  # sin ti (brekup)
sad2 = '37i9dQZF1DXbrUpGvoi3TS'  # Broken Heart
sad3 = '37i9dQZF1DWX83CujKHHOn'  # alone again
sad4 = '37i9dQZF1DX3YSRoSdA634'  # life sucks (yeez)
sad5 = '37i9dQZF1DWVxpHBekDUXK'  # coping with loss
sad6 = '37i9dQZF1DWZrc3lwvImLj'  # melancholy instrumental """
