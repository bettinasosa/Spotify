import pprint
import getopt
import sys
import csv
import json
import pandas as pd
from pymongo import MongoClient
import pymongo
from dotenv import load_dotenv
import os

# loading client credentials
load_dotenv()

# mongo client and database I am sending the document to
password = os.getenv("password")

# CSV to JSON Conversion
csvfile = open('moods1.csv', 'r')
reader = csv.DictReader(csvfile)
client = MongoClient(
    "mongodb+srv://gorgodar:{0}@cluster0.z77hp.mongodb.net/tracks?retryWrites=true&w=majority".format(password))
db = client.Spotify
header = ['name', 'album', 'artist', 'id', 'release_date', 'popularity', 'length', 'danceability', 'acousticness', 'energy', 'instrumentalness',
          'liveness', 'valence', 'loudness', 'speechiness', 'tempo', 'key', 'time_signature', 'mood']

for each in reader:
    row = {}
    for field in header:
        data = []
        row[field] = each[field]
    data.append(row)
    print(data)
    db.tracks.insert_many(data)


""" import tkinter as tk
from tkinter import simpledialog

ROOT = tk.Tk()

ROOT.withdraw()
# the input dialog
USER_INP = simpledialog.askstring(title="Test",
                                  prompt="What's your Name?:")

# check it out
print("Hello", USER_INP)
 """
