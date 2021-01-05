from pprint import pprint
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy
from dotenv import load_dotenv

load_dotenv()

client_credentials_manager = SpotifyClientCredentials()

scope = 'playlist-read-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
search_str = 'Muse'
result = sp.search(search_str)
pprint(result)

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
    while True:
        response = sp.playlist_items(pl_id,
                                     offset=offset,
                                     fields='items.track.id,items.track.name,total',
                                     additional_types=['track'])

        for i, item in enumerate(response['items']):
            trackList.append(
                dict(track=item['track']))
        print(trackList)

        if len(response['items']) == 0:
            break

    # pprint(trackList)
    offset = offset + len(response['items'])
