#!/usr/bin/env python
# coding: utf-8


from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.utils import np_utils
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from spotipy import SpotifyClientCredentials, util
import spotipy
from dotenv import load_dotenv
load_dotenv()


# loading the updated csv file
df = pd.read_csv("moods1.csv")

# structuring the file properly
col_features = df.columns[6:-3]
X = MinMaxScaler().fit_transform(df[col_features])
X2 = np.array(df[col_features])
Y = df['mood']


# Encode the categories
encoder = LabelEncoder()
encoder.fit(Y)
encoded_y = encoder.transform(Y)

# dividning the data into train and test
X_train, X_test, Y_train, Y_test = train_test_split(
    X, encoded_y, test_size=0.2, random_state=0)

target = pd.DataFrame({'mood': df['mood'].tolist(
), 'encode': encoded_y}).drop_duplicates().sort_values(['encode'], ascending=True)
#print('X_train: {}, Y_train: {}'.format(len(X_train), len(Y_train)))
#print('X_test: {}, Y_test: {}'.format(len(X_test), len(Y_test)))

# the model function to predict the mood. Random forest classifier was chosen over other as it had the highest accuracy.


def predict_mood(id_song):
    clf = RandomForestClassifier(n_estimators=100, criterion='gini')
    clf.fit(X2, encoded_y)

    # Obtain the features of the song
    preds = get_songs_features(id_song)
    # Pre-process the features to input the Model
    preds_features = np.array(preds[0][6:-2]).reshape(-1, 1).T

    # Predict the features of the song
    results = clf.predict(preds_features)

    mood = np.array(target['mood'][target['encode'] == int(results)])
    name_song = preds[0][0]
    artist = preds[0][2]

    return print(f"{name_song} by {artist} is a {mood[0].upper()} song")
    # mood[0].upper()
    # print("{0} by {1} is a {2} song".format(name_song, artist, mood[0].upper()))
    # print(f"{name_song} by {artist} is a {mood[0].upper()} song")


def get_songs_features(id_songs):
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    meta = sp.track(id_songs)
    features = sp.audio_features(id_songs)

    # meta
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']
    ids = meta['id']

    # features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    valence = features[0]['valence']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    key = features[0]['key']
    time_signature = features[0]['time_signature']

    track = [name, album, artist, ids, release_date, popularity, length, danceability, acousticness,
             energy, instrumentalness, liveness, valence, loudness, speechiness, tempo, key, time_signature]
    columns = ['name', 'album', 'artist', 'id', 'release_date', 'popularity', 'length', 'danceability', 'acousticness', 'energy', 'instrumentalness',
               'liveness', 'valence', 'loudness', 'speechiness', 'tempo', 'key', 'time_signature']
    return track, columns


# predict_mood('2AkcjsKlRbIBYGAgpQVFii')
