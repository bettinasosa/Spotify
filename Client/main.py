#!/usr/bin/env python3
# coding: utf-8


from spotify_client import *
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

spotify = SpotifyAPI(client_id, client_secret)
spotify.search({"track": "Time"}, search_type="track")
print(spotify.personalisation(_id='tracks'))
