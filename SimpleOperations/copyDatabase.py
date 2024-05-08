import os
import pymongo
from dotenv import load_dotenv

# ------------------------------------------------------------------------------------------------------- #
# This simply duplicated the database; ensuring if we destroyed the data, we would have an untouched copy #
# ------------------------------------------------------------------------------------------------------- #

load_dotenv("./.env")
mongo_uri = os.environ.get("MONGODB_URI")
print(mongo_uri)

client = pymongo.MongoClient(mongo_uri)
db = client.get_database("nonprofit")
existing_collection = db.get_collection("organization_10k")
new_collection = db.get_collection("organization_10k_original")
new_collection.insert_many(existing_collection.find())
print("New collection has been created.")