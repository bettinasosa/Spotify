#!/usr/bin/env python3
# coding: utf-8


from spotify_client import *

client_id = 'b9bca1427f084b93be082e6755acbeab'
client_secret = '2398177c2eae4536976c36e94ad1fb00'

spotify = SpotifyAPI(client_id, client_secret)
spotify.search({"track": "Time"}, search_type="track")
print(spotify.personalisation(_id='tracks'))
