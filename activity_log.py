from pprint import pprint
from pymongo import MongoClient
import pymongo
from dotenv import load_dotenv
import os
import time
from datetime import datetime
import sys

while True:
    try:

        # music played in the last hour, as script will run every hour
        millis = int(round(time.time() * 1000 - 3600000))

        # loading client credentials
        load_dotenv()

        # mongo client and database I am sending the document to
        password = os.getenv("password")
        client = MongoClient(
            "mongodb+srv://gorgodar:{0}@cluster0.z77hp.mongodb.net/activity?retryWrites=true&w=majority".format(password))
        db = client.Spotify

        # Note: Python 2.x users should use raw_input, the equivalent of 3.x's input
        mood = str(input("Please enter the activity: "))
        data = []

        data.append(dict(activity=mood,
                         time=datetime.now()))
        db.activity.insert_many(data)
        time.sleep(100)
    except KeyboardInterrupt:
        # quit
        sys.exit()
