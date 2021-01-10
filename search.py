# shows artist info for a URN or URL

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
import pprint

from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
#result = sp.search(search_str)
result = sp.recommendations(seed_tracks='tracks')
pprint.pprint(result)
