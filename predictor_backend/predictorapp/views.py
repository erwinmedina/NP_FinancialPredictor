import os
import pymongo
import json
import matplotlib
from dotenv import load_dotenv
from django.shortcuts import render
matplotlib.use('Agg')
from django.http import HttpResponse
from .predictor import predict_total_expenses, predict_total_revenue

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
        plot_image_expenses = predict_total_expenses(ein)
        plot_image_revenue = predict_total_revenue(ein)

        # Convert filings_with_data to JSON
        filings_with_data_json = json.dumps(organization.get('filings_with_data', []))
        return render(request, 'organization_detail.html', {
            'organization': organization, 
            'filings_with_data_json': filings_with_data_json,
            'plot_image_expenses': plot_image_expenses,
            'plot_image_revenue': plot_image_revenue
            })
    else:
        return render(request, 'home.html')

# Handles the random generator.
def random_organization(request):
    random_organization = collection.aggregate([{ '$sample': { 'size': 1 }}])
    organization = next(random_organization, None)
    plot_image_expenses = predict_total_expenses(organization["organization"]["ein"])
    plot_image_revenue = predict_total_revenue(organization["organization"]["ein"])
    if organization:
        filings_with_data_json = json.dumps(organization.get('filings_with_data', []))
        return render(request, 'organization_detail.html', {
            'organization': organization, 
            'filings_with_data_json': filings_with_data_json,
            'plot_image_expenses': plot_image_expenses,
            'plot_image_revenue': plot_image_revenue
            })
    else:
        return render(request, 'home.html')