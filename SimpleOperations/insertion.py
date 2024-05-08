import os
import pymongo
import json
from dotenv import load_dotenv

# ******************************************************************* #
# This script inserts all of our json organizations into the database #
# ******************************************************************* #

load_dotenv("./.env")
mongo_uri = os.environ.get("MONGODB_URI")
print(mongo_uri)

client = pymongo.MongoClient(mongo_uri)
db = client.get_database("nonprofit")
collection = db.get_collection("organization_10k")

count = 1
with open("nonprofit_data_10k.json", "r") as file:
    nonprofit = json.load(file)
results = []

for org in nonprofit:
    count = count + 1
    collection.insert_one(org)
    print(count)