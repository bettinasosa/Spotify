import csv
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
import signal
from datetime import datetime
import spi
import spidev
import time
import sys
from mfrc522 import SimpleMFRC522
from mfrc522 import MFRC522
import gpio as GPIO
import os
import time
import numpy as np
import random

load_dotenv()

client_credentials_manager = SpotifyClientCredentials()


tag_mapping = {
    "[136, 4, 194, 26, 84]": 'energetic',     # mp black running leggings
    '[136, 4, 162, 26, 52]': 'energetic',     # mp king blue running leggings
    '[136, 4, 161, 26, 55]': 'energetic',     # Nike long-sleeve running fleece
    '[136, 4, 156, 26, 10]': 'energetic',     # mp dark blue running leggings
    '[136, 4, 123, 26, 237]': 'study',         # Nike white sweatpant
    '[136, 4, 252, 26, 106]': 'happy',        # cream sweater
    '[136, 4, 2, 26, 148]': 'happy',          # ando blue sweater
    '[136, 4, 219, 26, 77]': 'chill',         # b&w xmas sweater
    '[136, 4, 251, 26, 109]': 'happy',        # black gold sweater
    '[136, 4, 1, 26, 151]': 'chill',          # Grey cardigan
    '[136, 4, 28, 26, 138]': 'happy',         # black velvet trousers
    '[136, 4, 36, 25, 177]': 'happy',         # black trouser
    '[136, 4, 27, 26, 141]': 'happy',         # wide-leg jeans
    '[136, 4, 35, 26, 181]': 'energetic',     # red black legging (party ones)
    '[136, 4, 34, 26, 180]': 'chill',          # camel wide-leg trouser
    '[136, 4, 37, 25, 176]': 'study',         # lightining white t-shirt
    # moon dark blue long sleeve tshirt
    '[136, 4, 9, 25, 156]': 'chill',
    '[136, 4, 43, 25, 190]': 'chill',         # black no sleeve turtleneck
    '[136, 4, 44, 25, 185]': 'happy',         # blue crop top long sleeve
    '[136, 4, 3, 25, 150]': 'study',          # white crop top long sleeve
    '[136, 4, 228, 25, 113]': 'happy',        # brown no sleeve turtleneck
    '[136, 4, 4, 25, 145]': 'happy',          # grey crop top
    '[136, 4, 10, 25, 159]': 'study',          # grey long-sleeve p&b
    '[136, 4, 227, 25, 118]': 'happy',        # green and blue overshirt
    '[136, 4, 233, 25, 124]': 'happy',        # black and white overshirt
    '[136, 4, 130, 25, 23]': 'happy',         # black boots
    '[136, 4, 169, 25, 60]': 'energetic',     # nike air force1 pixle
    '[136, 4, 162, 25, 55]': 'energetic',     # nike react running
    '[136, 4, 163, 25, 54]': 'energetic',     # Black ysl high-heels
    '[136, 4, 168, 25, 61]': 'energetic',     # ash black going out high-heels
    '[136, 4, 234, 25, 127]': 'study',         # long pleated dark blue skirt
    '[136, 4, 195, 25, 86]': 'energetic',     # black long skirt with side slit
    # mid-length black skirt neoprene
    '[136, 4, 201, 25, 92]': 'studyy',
    '[136, 4, 196, 25, 81]': 'study',          # camel skort
    # shoulder-pad ceam crop top/sweater
    '[136, 4, 202, 25, 95]': 'energectic',
    '[136, 4, 105, 27, 254]': 'happy',        # stars black plumeti top
    '[136, 4, 99, 27, 244]': 'energetic',     # black lace crop top
    '[136, 4, 138, 27, 29]': 'energetic',     # kiss kimono
    '[136, 4, 132, 27, 19]': 'study',          # kimono
    '[136, 4, 137, 27, 30]': 'happy',         # black with white dots dress
    '[136, 4, 225, 26, 119]': 'energetic',    # black vs tshirt (running)
    '[136, 4, 220, 26, 74]': 'energetic',     # breast cancer tshirt (running)
    '[136, 4, 226, 26, 116]': 'energetic',    # grey crew neck sweatshirt
    '[136, 4, 187, 26, 45]': 'energetic',     # thrasher pink crew sweatshirt
    '[136, 4, 188, 26, 42]': 'energetic',     # NB running lighweight jacket
    '[136, 4, 100, 27, 243]': 'study',         # best ever fluffy slippers
    # black stars long-sleeve semi shirt
    '[136, 4, 106, 27, 253]': 'happy',
    '[136, 4, 130, 26, 20]': 'energetic',         # black leather jacket
    '[136, 4, 124, 26, 234]': 'energetic',    # black leather blazer
    '[136, 4, 129, 26, 23]': 'happy',         # black leather moto jacket
    '[136, 4, 163, 27, 52]': 'happy',         # black leather trousers
    '[136, 4, 170, 27, 61]': 'happy',         # black fur coat
    '[136, 4, 164, 27, 51]': 'energetic',     # burgundy velvet dress
    '[136, 4, 171, 27, 60]': 'energetic',     # black nike crop top
    '[136, 4, 131, 27, 20]': 'energetic',     # mp white crop top
    '[136, 4, 235, 27, 124]': 'energetic',    # boxing shorts
    '[136, 4, 196, 27, 83]': 'energetic',     # running shorts
    '[136, 4, 202, 27, 9]': 'energetic',      # dark blue nike running leg
    '[136, 4, 197, 27, 82]': 'energetic',     # blue fleece
    '[136, 4, 203, 27, 92]': 'energetic'      # running tshirt
}


while True:
    try:
        load_dotenv()

        client_credentials_manager = SpotifyClientCredentials()
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

        # Get the UID of the card
        (status, uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:
            # print(data)
            trackLists = []
            df_study = []
            df_chill = []
            df_happy = []
            df_energetic = []
            with open('moods1.csv') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[18] == 'chill':
                        df_chill.append(row)
                    if row[18] == 'study':
                        df_study.append(row)
                    if row[18] == 'happy':
                        df_happy.append(row)
                    if row[18] == 'energetic':
                        df_energetic.append(row)
                        # print(df_study)
            #df = np.recfromcsv('data_moods.csv')
            # print(df)
            uid = ''.join(str(uid))
            ids = tag_mapping[uid]
            sp = spotipy.Spotify(
                client_credentials_manager=client_credentials_manager)

            if ids == 'chill':
                t = random.choice(df_chill)
                track = []
                track.append(t[3])

            if ids == 'study':
                t = random.choice(df_study)
                track = []
                print(track)
                track.append(t[3])
                print(track)

            if ids == 'energetic':
                t = random.choice(df_energetic)
                track = []
                track.append(t[3])

            if ids == 'happy':
                t = random.choice(df_happy)
                track = []
                track.append(t[3
                               ])

            print(track)
            recommend = sp.recommendations(
                seed_tracks=track, limit=20)
            # pprint(recommend)
            for i, tracks in enumerate(recommend['tracks']):
                trackLists.append(tracks['uri'])
            scope = "user-read-playback-state,user-modify-playback-state"
            sp = spotipy.Spotify(
                client_credentials_manager=SpotifyOAuth(scope=scope))
            sp.start_playback(uris=trackLists)
    except KeyboardInterrupt:
        # quit
        sys.exit()
