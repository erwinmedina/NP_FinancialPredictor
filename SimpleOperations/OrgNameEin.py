import os
import pymongo
from dotenv import load_dotenv

# *************************************************************** #
# Created a new database that only contains EIN and Company Name. #
# *************************************************************** #

load_dotenv("./.env")
mongo_uri = os.environ.get("MONGODB_URI")
print(mongo_uri)

client = pymongo.MongoClient(mongo_uri)
db = client.get_database("nonprofit")
collection = db.get_collection("organization_10k")
collection2 = db.get_collection("OrgNameEin")
document = collection.find({})

count = 0

for document in collection.find():
    count += 1
    orgName = document["organization"].get("name")
    orgEin = document["organization"].get("ein")
    collection2.insert_one({
        "name": orgName,
        "ein": orgEin
    })
    print(count)
