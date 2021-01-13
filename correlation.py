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
import time
import pandas
import numpy as np

# loading client credentials
load_dotenv()

# mongo client and database I am sending the document to
password = os.getenv("password")
client = MongoClient(
    "mongodb+srv://gorgodar:{0}@cluster0.z77hp.mongodb.net/activity?retryWrites=true&w=majority".format(password))
db = client.Spotify
collection = db["activity"]

start_time = time.time()

cursor = collection.find()

mongo_docs = list(cursor)

docs = pandas.DataFrame(columns=[])
for num, doc in enumerate(mongo_docs):
    doc["_id"] = str(doc["_id"])
    doc_id = doc["_id"]

    series_obj = pandas.Series(doc, name=doc_id)
    docs = docs.append(series_obj)

# print(docs)

start = (docs.iloc[1]['time'])  # gives the time for the first entry
# gives the time for the last entry
end = (docs.iloc[len(mongo_docs)-1]['time'])
# print(end)
bins = np.arange(start, end, 3600000000)
print(bins)
category = []
for n in bins:
    category.append(n)
del category[-1]  # there needs to be one less category than no. of bins
# print(category)

docs['TimeBin'] = pandas.cut(docs["time"], bins, labels=category)
print(docs)
