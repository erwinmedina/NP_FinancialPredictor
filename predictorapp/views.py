import os
import pymongo
import json
import matplotlib
from dotenv import load_dotenv
from django.shortcuts import render
from .predictor import predict_total_expenses, predict_total_revenue
from .compare import compare_revenue, compare_expense
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

        # Handles the json expenses image #
        response_expenses = predict_total_expenses(ein)
        data_expenses = json.loads(response_expenses.content.decode('utf-8'))
        plot_image_expenses = data_expenses.get('plot_image_expense')

        # Handles the json revenue image #
        response_revenue = predict_total_revenue(ein)
        data_revenue = json.loads(response_revenue.content.decode('utf-8'))  
        plot_image_revenue = data_revenue.get('plot_image_revenue')

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

    # Handles the json expenses image #
    response_expenses = predict_total_expenses(organization["organization"]["ein"])
    data_expenses = json.loads(response_expenses.content.decode('utf-8'))
    plot_image_expenses = data_expenses.get('plot_image_expense')

    # Handles the json revenue image #
    response_revenue = predict_total_revenue(organization["organization"]["ein"])
    data_revenue = json.loads(response_revenue.content.decode('utf-8'))  
    plot_image_revenue = data_revenue.get('plot_image_revenue')

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
    
# Handles the comparison graphs
def comparison_charts(request):

    # Handles the json expenses image #
    response_compare_expenses = compare_expense()
    data_compare_expenses = json.loads(response_compare_expenses.content.decode('utf-8'))
    plot_image_comparison_expense = data_compare_expenses.get('plot_image_compare_expense')

    # Handles the json revenue image #
    response_compare_revenue = compare_revenue()
    data_compare_revenue = json.loads(response_compare_revenue.content.decode('utf-8'))  
    plot_image_comparison_revenue = data_compare_revenue.get('plot_image_compare_revenue')

    return render(request, "comparison.html", {
        'plot_image_comparison_revenue': plot_image_comparison_revenue,
        'plot_image_comparison_expense': plot_image_comparison_expense
    })