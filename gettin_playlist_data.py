from pprint import pprint
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy
from dotenv import load_dotenv

load_dotenv()

client_credentials_manager = SpotifyClientCredentials()

scope = 'playlist-read-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_playlists(limit=50)
playList = []
for i, item in enumerate(results['items']):
    playList.append(
        dict(name=item['name'], id=item['id']))


for playlist in playList:
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    pl_id = playlist['id']
    offset = 0
    trackList = []
    response = sp.playlist_items(pl_id,
                                 offset=offset,
                                 fields='items.track.id,items.track.name',
                                 additional_types=['track'])

trackList = []
for i in response['items']:
    tracks = i['track']['name']
    track_id = i['track']['id']
    trackList.append(
        dict(name=tracks, id=track_id))
    print(trackList)

""" for item in response:
        print(item)
        for t, track in enumerate(item['track']):
            trackList.append(
                dict(name=item['name'], id=item['id']))

        pprint(trackList)
    offset = offset + len(response['items'])
 """
