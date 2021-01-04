# Shows the top tracks for a user

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

scope = 'user-top-read'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

ranges = ['short_term', 'medium_term', 'long_term']

for sp_range in ranges:
    print("range:", sp_range)
    results = sp.current_user_top_tracks(time_range=sp_range, limit=20)
    trackList = []
    for i, item in enumerate(results['items']):
        print(i, item['name'], '//', item['artists']
              [0]['name'], '//', item['id'])
        trackList.append(
            dict(name=item['name'], id=item['id'], artist=item['artists'][0]['name']))

print(trackList)
