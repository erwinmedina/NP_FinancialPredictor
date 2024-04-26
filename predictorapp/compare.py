import pandas as pd
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import pymongo
import io
import base64
from django.http import JsonResponse

# --------------------------------------------- #
# THIS HANDLES THE COMPARISON CHART FOR REVENUE #
# --------------------------------------------- #
def compare_revenue():

    # Handles reading from the DB
    load_dotenv("./.env")
    mongo_uri = os.environ.get("MONGODB_URI")
    client = pymongo.MongoClient(mongo_uri)
    db = client.get_database("nonprofit")
    collection = db.get_collection('organization')

    # Extract revenue_amount and state for each organization
    revenue_data = []
    data = collection.find({})
    for entry in data:
        state = entry["organization"]["state"]
        revenue_amount = entry["organization"]["revenue_amount"]
        revenue_data.append({"State": state, "Revenue Amount": revenue_amount})

    # Convert data to DataFrame
    df_revenue = pd.DataFrame(revenue_data)

    # Calculate average revenue_amount per state
    df_average_revenue = df_revenue.groupby('State').mean().reset_index()
    print(df_average_revenue.to_string())

    # GDP per capita data with state abbreviations
    gdp_per_capita = {
        'State': ['NY', 'VA', 'NC', 'MA', 'NH', 'TN', 'AK', 'PA', 'MI', 'CT', 'IA', 'MO', 'CA', 'KS', 'NM', 'ND', 
                'SD', 'AZ', 'WA', 'WI', 'FL', 'WY', 'OH', 'ME', 'DE', 'OR', 'MT', 'NJ', 'RI', 'KY', 'MD', 'UT', 
                'AL', 'IL', 'GA', 'SC', 'CO', 'LA', 'ID', 'MN', 'OK', 'WV', 'TX', 'IN', 'AR', 'NE', 'NV', 'MS', 
                'HI', 'VT', 'DC'],
        'GDP per Capita': [73531, 55929, 47778, 72635, 55744, 47695, 70936, 55602, 46858, 67784,
                            54101, 46064, 67698, 52297, 44187, 67308, 51997, 43096, 67242, 51575,
                            43052, 66413, 51456, 42356, 66023, 50996, 42173, 62263, 50827, 41659,
                            60886, 49740, 40279, 59980, 49663, 39883, 59057, 49606, 39843, 59057,
                            48954, 39495, 58417, 48738, 38467, 58141, 48189, 34029, 56880, 47921,
                            176534]  # GDP per capita in dollars
    }

    # Convert GDP per capita data to DataFrame
    df_gdp_per_capita = pd.DataFrame(gdp_per_capita)

    # Merge DataFrames on 'State'
    df_merged = pd.merge(df_average_revenue, df_gdp_per_capita, left_on='State', right_on='State')

    # Normalize average revenue with GDP per capita
    df_merged['Normalized Revenue'] = df_merged['Revenue Amount'] / df_merged['GDP per Capita']

    # Plotting
    plt.figure(figsize=(12, 8))
    plt.bar(df_merged['State'], df_merged['Normalized Revenue'], color='skyblue')
    plt.xlabel('State')
    plt.ylabel('Normalized Revenue')
    plt.title('Normalized Revenue by State')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.grid(True)

    # Save the plot to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Encode the plot image as a base64 string
    plot_image_compare_revenue = base64.b64encode(buffer.getvalue()).decode()

    return JsonResponse({'plot_image_compare_revenue': plot_image_compare_revenue})


# ---------------------------------------------- #
# THIS HANDLES THE COMPARISON CHART FOR EXPENSES #
# ---------------------------------------------- #
def compare_expense():
   # Handles reading from the DB
    load_dotenv("./.env")
    mongo_uri = os.environ.get("MONGODB_URI")
    client = pymongo.MongoClient(mongo_uri)
    db = client.get_database("nonprofit")
    collection = db.get_collection('organization')

    expense_data = []
    expense_amount = []
    data = collection.find({})
    counter = 0

    # Iterate over each organization
    for organization in data:
        # Extract organization information
        org_state = organization['organization']['state']        

        # Extract totfuncexpns for each filing and calculate average
        totfuncexpns_list = []
        for filing in organization['filings_with_data']:
            totfuncexpns_list.append(filing['totfuncexpns'])
        
        # Calculate average totfuncexpns
        average_totfuncexpns = sum(totfuncexpns_list) / len(totfuncexpns_list) if totfuncexpns_list else 0
        expense_amount.append(average_totfuncexpns)

        expense_data.append({"State": org_state, "Expense Amount": expense_amount[counter]})
        counter += 1

    # Convert data to DataFrame
    df_expense = pd.DataFrame(expense_data)

    # Calculate average revenue_amount per state
    df_average_expense = df_expense.groupby('State').mean().reset_index()

    # GDP per capita data with state abbreviations
    gdp_per_capita = {
        'State': ['NY', 'VA', 'NC', 'MA', 'NH', 'TN', 'AK', 'PA', 'MI', 'CT', 'IA', 'MO', 'CA', 'KS', 'NM', 'ND', 
                'SD', 'AZ', 'WA', 'WI', 'FL', 'WY', 'OH', 'ME', 'DE', 'OR', 'MT', 'NJ', 'RI', 'KY', 'MD', 'UT', 
                'AL', 'IL', 'GA', 'SC', 'CO', 'LA', 'ID', 'MN', 'OK', 'WV', 'TX', 'IN', 'AR', 'NE', 'NV', 'MS', 
                'HI', 'VT', 'DC'],
        'GDP per Capita': [73531, 55929, 47778, 72635, 55744, 47695, 70936, 55602, 46858, 67784,
                            54101, 46064, 67698, 52297, 44187, 67308, 51997, 43096, 67242, 51575,
                            43052, 66413, 51456, 42356, 66023, 50996, 42173, 62263, 50827, 41659,
                            60886, 49740, 40279, 59980, 49663, 39883, 59057, 49606, 39843, 59057,
                            48954, 39495, 58417, 48738, 38467, 58141, 48189, 34029, 56880, 47921,
                            176534]  # GDP per capita in dollars
    }

    # Convert GDP per capita data to DataFrame
    df_gdp_per_capita = pd.DataFrame(gdp_per_capita)

    # Merge DataFrames on 'State'
    df_merged = pd.merge(df_average_expense, df_gdp_per_capita, left_on='State', right_on='State')

    # Normalize average revenue with GDP per capita
    df_merged['Normalized Expense'] = df_merged['Expense Amount'] / df_merged['GDP per Capita']

    # Plotting
    plt.figure(figsize=(12, 8))
    plt.bar(df_merged['State'], df_merged['Normalized Expense'], color='skyblue')
    plt.xlabel('State')
    plt.ylabel('Normalized Expenses')
    plt.title('Normalized Expenses by State')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.grid(True)

    # Save the plot to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Encode the plot image as a base64 string
    plot_image_compare_expense = base64.b64encode(buffer.getvalue()).decode()

    return JsonResponse({'plot_image_compare_expense': plot_image_compare_expense})
