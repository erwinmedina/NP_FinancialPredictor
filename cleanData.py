import os
import pymongo
from dotenv import load_dotenv

load_dotenv("./.env")
mongo_uri = os.environ.get("MONGODB_URI")
print(mongo_uri)

client = pymongo.MongoClient(mongo_uri)
db = client.get_database("nonprofit")
collection = db.get_collection("organization_10k")

# # Simply removes the three objects listed below.
# update_operation = {
#     "$unset": {
#         "filings_without_data": "",
#         "data_source": "",
#         "api_version": ""
#     }
# }
# collection.update_many({}, update_operation)

# -------------------------------------------- #
# Deletes extra keys from organization object. #
# -------------------------------------------- #
keys_to_delete = [
    "subsection_code",
    "affiliation_code",
    "classification_codes",
    "ruling_date",
    "deductibility_code",
    "foundation_code",
    "activity_codes",
    "filing_requirement_code",
    "pf_filing_requirement_code",
    "accounting_period",
    "sort_name",
    "created_at",
    "updated_at",
    "data_source",
    "have_extracts",
    "have_pdfs",
    "latest_object_id"
]

count = 0
for document in collection.find():
    count += 1
    organization = document["organization"]
    for key in keys_to_delete:
        organization.pop(key, None)
    print(count)
    collection.update_one({"_id": document["_id"]},{"$set": {"organization": organization}})

print("Deleted keys from organization. woot")

# -------------------------------------------------------------------- #
# Deletes extra keys from the organization["filings_with_data"] object #
# -------------------------------------------------------------------- #

keys_to_delete = [
    "tax_prd",
    "formtype",
    "pdf_url",
    "updated",
    "pct_compnsatncurrofcr",
    "tax_pd",
    "subseccd",
    "unrelbusinccd",
    "initiationfees",
    "grsrcptspublicuse",
    "grsincmembers",
    "grsincother",
    "txexmptbndsproceeds",
    "grsalesecur",
    "grsalesothr",
    "cstbasisecur",
    "cstbasisothr",
    "netgnls",
    "grsincfndrsng",
    "lessdirfndrsng",
    "netincfndrsng",
    "grsincgaming",
    "lessdirgaming",
    "netincgaming",
    "grsalesinvent",
    "lesscstofgoods",
    "netincsales",
    "miscrevtot11e",
    "profndraising",
    "txexmptbndsend",
    "secrdmrtgsend",
    "unsecurednotesend",
    "retainedearnend",
    "totnetassetend",
    "nonpfrea",
    "gftgrntsrcvd170",
    "txrevnuelevied170",
    "srvcsval170",
    "grsinc170",
    "grsrcptsrelated170",
    "totgftgrntrcvd509",
    "grsrcptsadmissn509",
    "txrevnuelevied509",
    "srvcsval509",
    "subtotsuppinc509",
    "totsupp509"
]

count = 0
for document in collection.find():
    count += 1
    for filing in document["filings_with_data"]:
        for key in keys_to_delete:
            filing.pop(key, None)
    print(count)
    collection.update_one({"_id": document["_id"]}, {"$set": {"filings_with_data": document["filings_with_data"]}})

print("deleted the extra keys from filings_with_data. Woot")