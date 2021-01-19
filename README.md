# Spotify

This project intends to collect user data based on their Spotify listening trends and their clothing style. The of this project is a 'personalised jukebox', in other words a smart device that will create a 20 song playlist according to your clothing and mood.

File structure: 

- upload_uid.py   This script is intended for collecting the users clothing trends
- add_data.py     This script sends data to mongodb on the hour with the data on recently played songs by the user and the song analasys.
- ml.py           This script analyses the user data been collected and predict the user moood. It was used to set a certain mood to different pieces of clothing from the music data.
- recommend.py    This script is triggered when a clothing tag is scanned. Depending on the items' mood it will find a seed song from the analysed data and create a playlist of 20 songs available at any device with spotify.
