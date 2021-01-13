#!/usr/bin/venv python 3.8.0
# coding: utf-8

import signal
from datetime import datetime
import spi
import spidev
import time
import sys
from mfrc522 import SimpleMFRC522
from mfrc522 import MFRC522
import gpio as GPIO
from dotenv import load_dotenv
import os
import time
from pymongo import MongoClient
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv


while True:
    try:
        # loading client credentials
        load_dotenv()

        # mongo client and database I am sending the document to
        password = os.getenv("password")
        client = MongoClient(
            "mongodb+srv://gorgodar:{0}@cluster0.z77hp.mongodb.net/UID?retryWrites=true&w=majority".format(password))
        db = client.Spotify

        # Creating a list to contain the document
        data = []

        # Disable warnings
        GPIO.setwarnings(False)

        # read with MFRC522 on GPIO
        # define variables
        global value_rfid_2, reply_rfid_2, tag, refTime

        # assign values
        refTime = datetime.now()

        # Create an object of the class MFRC522
        MIFAREReader = MFRC522()
        easy = SimpleMFRC522()

        # Scan for cards
        (status, TagType) = MIFAREReader.MFRC522_Request(
            MIFAREReader.PICC_REQIDL)

        # If a card is found
        # if status == MIFAREReader.MI_OK:
        # print("Card detected")

        # Get the UID of the card
        (status, uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:
            text = []
            text_read = ''
            for block_num in easy.BLOCK_ADDRS:
                block = easy.READER.MFRC522_Read(block_num)
            if block:
                text += block
            if text:
                text_read = ''.join(chr(i) for i in text)
                print(text_read)
            data.append(dict(uid=uid, text=text, time=datetime.now()))
            # print(data)

            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)

            # insert document in database
            db.UID.insert_many(data)

            time.sleep(5)

        GPIO.cleanup()      # Clear input buffer
    except KeyboardInterrupt:
        # quit
        sys.exit()
