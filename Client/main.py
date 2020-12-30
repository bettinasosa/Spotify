#!/usr/bin/env python3
# coding: utf-8


from spotify_client import *
from dotenv import load_dotenv

load_dotenv()

spotify = SpotifyAPI(client_id, client_secret)
spotify.search({"track": "Time"}, search_type="track")
print(spotify.personalisation(_id='tracks'))
