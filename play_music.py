import pandas as pd
import csv
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

client_credentials_manager = SpotifyClientCredentials()


tag_mapping = {
    "136, 4, 194, 26, 84": 'energetic',     # mp black running leggings
    '136, 4, 162, 26, 52': 'energetic',     # mp king blue running leggings
    '136, 4, 161, 26, 55': 'energetic',     # Nike long-sleeve running fleece
    '136, 4, 156, 26, 10': 'energetic',     # mp dark blue running leggings
    '136, 4, 123, 26, 237': 'calm',         # Nike white sweatpant
    '136, 4, 252, 26, 106': 'happy',        # cream sweater
    '136, 4, 2, 26, 148': 'happy',          # ando blue sweater
    '136, 4, 219, 26, 77': 'happy',         # b&w xmas sweater
    '136, 4, 251, 26, 109': 'happy',        # black gold sweater
    '136, 4, 1, 26, 151': 'happy',          # Grey cardigan
    '136, 4, 28, 26, 138': 'happy',         # black velvet trusers
    '136, 4, 36, 25, 177': 'happy',         # black trouser
    '136, 4, 27, 26, 141': 'happy',         # wide-leg jeans
    '136, 4, 35, 26, 181': 'energetic',     # red black legging (party ones)
    '136, 4, 34, 26, 180': 'calm',          # camel wide-leg trouser
    '136, 4, 37, 25, 176': 'happy',         # lightining white t-shirt
    '136, 4, 9, 25, 156': 'happy',          # moon dark blue long sleeve tshirt
    '136, 4, 43, 25, 190': 'happy',         # black no sleeve turtleneck
    '136, 4, 44, 25, 185': 'happy',         # blue crop top long sleeve
    '136, 4, 3, 25, 150': 'happy',          # white crop top long sleeve
    '136, 4, 228, 25, 113': 'happy',        # brown no sleeve turtleneck
    '136, 4, 4, 25, 145': 'happy',          # grey crop top
    '136, 4, 10, 25, 159': 'calm',          # grey long-sleeve p&b
    '136, 4, 227, 25, 118': 'happy',        # green and blue overshirt
    '136, 4, 233, 25, 124': 'happy',        # black and white overshirt
    '136, 4, 130, 25, 23': 'happy',         # black boots
    '136, 4, 169, 25, 60': 'energetic',     # nike air force1 pixle
    '136, 4, 162, 25, 55': 'energetic',     # nike react running
    '136, 4, 163, 25, 54': 'energetic',     # Black ysl high-heels
    '136, 4, 168, 25, 61': 'energetic',     # ash black going out high-heels
    '136, 4, 234, 25, 127': 'calm',         # long pleated dark blue skirt
    '136, 4, 195, 25, 86': 'energetic',     # black long skirt with side slit
    '136, 4, 201, 25, 92': 'calm',          # mid-length black skirt neoprene
    '136, 4, 196, 25, 81': 'calm',          # camel skort
    '136, 4, 202, 25, 95': 'energectic',    # shoulder-pad ceam crop top/sweater
    '136, 4, 105, 27, 254': 'happy',        # stars black plumeti top
    '136, 4, 99, 27, 244': 'energetic',     # black lace crop top
    '136, 4, 138, 27, 29': 'energetic',     # kiss kimono
    '136, 4, 132, 27, 19': 'calm',          # kimono
    '136, 4, 137, 27, 30': 'happy',         # black with white dots dress
    '136, 4, 225, 26, 119': 'energetic',    # black vs tshirt (running)
    '136, 4, 220, 26, 74': 'energetic',     # breast cancer tshirt (running)
    '136, 4, 226, 26, 116': 'energetic',    # grey crew neck sweatshirt
    '136, 4, 187, 26, 45': 'energetic',     # thrasher pink crew sweatshirt
    '136, 4, 188, 26, 42': 'energetic',     # NB running lighweight jacket
    '136, 4, 100, 27, 243': 'calm',         # best ever fluffy slippers
    '136, 4, 106, 27, 253': 'happy',        # black stars long-sleeve semi shirt
    '136, 4, 130, 26, 20': 'happy',         # black leather jacket
    '136, 4, 124, 26, 234': 'energetic',    # black leather blazer
    '136, 4, 129, 26, 23': 'happy',         # black leather moto jacket
    '136, 4, 163, 27, 52': 'happy',         # black leather trousers
    '136, 4, 170, 27, 61': 'happy',         # black fur coat
    '136, 4, 164, 27, 51': 'energetic',     # burgundy velvet dress
    '136, 4, 171, 27, 60': 'energetic',     # black nike crop top
    '136, 4, 131, 27, 20': 'energetic',     # mp white crop top
    '136, 4, 235, 27, 124': 'energetic',    # boxing shorts
    '136, 4, 196, 27, 83': 'energetic',     # running shorts
    '136, 4, 202, 27, 9': 'energetic',      # dark blue nike running leg
    '136, 4, 197, 27, 82': 'energetic',     # blue fleece
    '136, 4, 203, 27, 92': 'energetic'      # running tshirt
}

""" with open('data_moods.csv')as f:
    df = csv.reader(f)
    print(df)
 """
trackLists = []
df = pd.read_csv("data_moods.csv")
# mood_c = tag_type[uid]

# uids = ''.join(uid)
ids = 'Calm'  # tag_mapping[uids]

if ids == 'Sad':
    df_sad = df[df['mood'] == 'Sad']
    df_sad.sample()


if ids == 'Calm':
    sp = spotipy.Spotify(
        client_credentials_manager=client_credentials_manager)
    df_calm = df[df['mood'] == 'Calm']
    t = df_calm.sample()
    track = t['id'].tolist()

if ids == 'Energetic':
    df_energetic = df[df['mood'] == 'Energetic']
    t = df_energetic.sample()

if ids == 'Happy':
    df_happy = df[df['mood'] == 'Happy']
    t = df_happy.sample()

recommend = sp.recommendations(
    seed_tracks=track, limit=1)
# pprint(recommend)
for i, tracks in enumerate(recommend['tracks']):
    trackLists.append(tracks['uri'])
scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))
sp.start_playback(uris=trackLists)
