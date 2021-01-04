# shows audio analysis for the given track

from __future__ import print_function    # (at top of module)
from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
import time
import sys

from dotenv import load_dotenv

load_dotenv()


client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

if len(sys.argv) > 1:
    tid = sys.argv[1]
else:
    tid = 'spotify:track:7tqhbajSfrz2F7E1Z75ASX'

start = time.time()
#analysis = sp.audio_analysis(tid)
analysis = sp.audio_features(tid)
delta = time.time() - start
print(json.dumps(analysis, indent=4))
print("analysis retrieved in %.2f seconds" % (delta,))
