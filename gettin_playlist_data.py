from pprint import pprint
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy
from dotenv import load_dotenv
import csv

load_dotenv()

client_credentials_manager = SpotifyClientCredentials()

scope = 'playlist-read-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_playlists(limit=50)
playList = []
for i, item in enumerate(results['items']):
    playList.append(
        dict(name=item['name'], id=item['id']))

trackList = []
trackLists = []
for playlist in playList:
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    pl_id = playlist['id']
    offset = 0
    response = sp.playlist_items(pl_id,
                                 offset=offset,
                                 fields='items.track.id,items.track.name',
                                 additional_types=['track'])
    for i, item in enumerate(response['items']):
        trackLists.append(
            dict(track=item['track']))
    # pprint(trackLists)
for song in trackLists:
    tracks = song['track']['name']
    track_id = song['track']['id']
    trackList.append(
        dict(name=tracks, id=track_id))
# pprint(trackList)

tracks_with_features = []
for i in trackList:
    track_id = i['id']
    if track_id != None:
        # print(track_id)
        sp = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager)
        features = sp.audio_features(track_id)
        f = features[0]
        tracks_with_features.append(dict(
            name=i['name'],
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
        # print(tracks_with_features[0])
    else:
        pass

csv_columns = ['name', 'id', 'danceability',
               'energy', 'loudness', 'speechiness', 'acousticness', 'tempo', 'liveness', 'valence']
csv_file = "emotion_data.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in tracks_with_features:
            writer.writerow(data)
except IOError:
    print("I/O error")
