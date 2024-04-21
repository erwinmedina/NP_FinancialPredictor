import os
import pymongo
import json
import matplotlib
from dotenv import load_dotenv
from django.shortcuts import render
matplotlib.use('Agg')

# Handles reading from the DB
load_dotenv("./.env")
mongo_uri = os.environ.get("MONGODB_URI")
client = pymongo.MongoClient(mongo_uri)
db = client.get_database("nonprofit")
collection = db.get_collection('organization_10k')

# Handles the home.html request
def home(request):
    return render(request, "home.html")

# Handles the organization page.
def organization_detail(request):
    ein = int(request.GET.get('ein'))
    if ein:
        organization = collection.find_one({'organization.ein': ein})

        # Convert filings_with_data to JSON
        filings_with_data_json = json.dumps(organization.get('filings_with_data', []))
        return render(request, 'organization_detail.html', {'organization': organization, 'filings_with_data_json': filings_with_data_json})
    else:
        return render(request, 'home.html')

# Handles the random generator.
def random_organization(request):
    random_organization = collection.aggregate([{ '$sample': { 'size': 1 }}])
    organization = next(random_organization, None)
    if organization:
        filings_with_data_json = json.dumps(organization.get('filings_with_data', []))
        return render(request, 'organization_detail.html', {'organization': organization, 'filings_with_data_json': filings_with_data_json})
    else:
        return render(request, 'home.html')
