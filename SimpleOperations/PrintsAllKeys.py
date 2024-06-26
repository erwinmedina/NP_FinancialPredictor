import os
import pymongo
from dotenv import load_dotenv

# ************************************************************************************** #
# This was a test script, ensuring the database was connected and we could retrieve data #
# ************************************************************************************** #

load_dotenv("./.env")
mongo_uri = os.environ.get("MONGODB_URI")
print(mongo_uri)

# MongoDB connection
client = pymongo.MongoClient(mongo_uri)
db = client.get_database("nonprofit")
collection = db.get_collection("organization")

# Retrieve one document from the collection
organization = collection.find_one()

# Print keys for the "organization" field
print("Keys for 'organization' field:")
for word in organization["organization"].keys():
    print(word)

# Print keys for the "filings_with_data" field
print("\nKeys for 'filings_with_data' field:")

for word in organization["filings_with_data"][0].keys():
    print(word)
