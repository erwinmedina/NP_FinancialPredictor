import pandas as pd
import os
import json
import matplotlib.pyplot as plt

# Get the absolute path to the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the absolute path to the JSON file
json_file_path = os.path.join(script_dir, 'nonprofit_data.json')

# Load data from JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Extract revenue_amount and state for each organization
revenue_data = []
for entry in data:
    state = entry["organization"]["state"]
    revenue_amount = entry["organization"]["revenue_amount"]
    revenue_data.append({"State": state, "Revenue Amount": revenue_amount})

# Convert data to DataFrame
df_revenue = pd.DataFrame(revenue_data)

# Calculate average revenue_amount per state
df_average_revenue = df_revenue.groupby('State').mean().reset_index()

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
plt.show()
































# import json
# import matplotlib.pyplot as plt

# def compare_revenue_expenses(json_data):
#     # Dictionary to store revenue and expense data by state
#     state_data = {}

#     # Iterate through organizations
#     for organization_data in json_data:
#         state = organization_data["organization"]["state"]
#         filings_with_data = organization_data["filings_with_data"]
        
#         # Extract revenue and expense data
#         revenue = []
#         expenses = []
#         for filing in filings_with_data:
#             revenue.append(filing.get("totrevenue", 0))
#             expenses.append(filing.get("totfuncexpns", 0))
        
#         # Store data by state
#         if state not in state_data:
#             state_data[state] = {"revenue": [], "expenses": []}
#         state_data[state]["revenue"].extend(revenue)
#         state_data[state]["expenses"].extend(expenses)

#     # Plotting
#     for state, data in state_data.items():
#         plt.figure(figsize=(10, 6))
#         plt.plot(data["revenue"], label="Revenue")
#         plt.plot(data["expenses"], label="Expenses")
#         plt.title(f"Comparison of Revenue and Expenses in {state}")
#         plt.xlabel("Filing Index")
#         plt.ylabel("Amount")
#         plt.legend()
#         plt.grid(True)
#         plt.show()

# # JSON data
# json_data = [
#    {
#        "organization": {
#            "id": 251494402,
#            "ein": 251494402,
#            "name": "Sae International",
#            "careofname": "% BRIAN K TRYBEND",
#            "address": "400 COMMONWEALTH DR",
#            "city": "Warrendale",
#            "state": "PA",
#            "zipcode": "15096-1200",
#            "accounting_period": 12,
#            "asset_amount": 105845396,
#            "income_amount": 94444028,
#            "revenue_amount": 82449462,
#            "ntee_code": "U030",
#            "sort_name": None,
#            "created_at": "2023-05-09T20:27:25.941Z",
#            "updated_at": "2024-03-28T16:41:24.395Z",
#            "data_source": "current_2024_03_28",
#            "have_extracts": None,
#            "have_pdfs": None,
#            "latest_object_id": "202333129349302448"
#        },
#        "filings_with_data": [
#            {
#                "tax_prd": 202112,
#                "tax_prd_yr": 2021,
#                "formtype": 0,
#                "pdf_url": None,
#                "updated": "2023-08-07T19:37:01.480Z",
#                "totrevenue": 75961312,
#                "totfuncexpns": 68439973,
#                "totassetsend": 113994097,
#                "totliabend": 41929064,
#                "ein": 251494402
#            },
#            # Other filings...
#        ]
#     },
#    {
#        "organization": {
#            "id": 431718408,
#            "ein": 431718408,
#            "name": "Mercy Health East Communities",
#            "careofname": None,
#            "address": "645 MARYVILLE CENTRE DR STE 100",
#            "city": "Saint Louis",
#            "state": "MO",
#            "zipcode": "63141-5846",
#            "accounting_period": 6,
#            "asset_amount": 541093879,
#            "income_amount": 214709806,
#            "revenue_amount": 214297785,
#            "ntee_code": "X00Z",
#            "sort_name": None,
#            "created_at": "2023-05-09T20:37:57.980Z",
#            "updated_at": "2024-03-28T16:46:06.035Z",
#            "data_source": "current_2024_03_28",
#            "have_extracts": None,
#            "have_pdfs": None,
#            "latest_object_id": "202331329349307638"
#        },
#        "filings_with_data": [
#            {
#                "tax_prd": 202106,
#                "tax_prd_yr": 2021,
#                "formtype": 0,
#                "pdf_url": None,
#                "updated": "2023-08-07T19:40:42.036Z",
#                "totrevenue": 86174797,
#                "totfuncexpns": 90349030,
#                "totassetsend": 429335158,
#                "totliabend": 73338700,
#                "ein": 431718408
#            },
#            # Other filings...
#        ]
#    }
# ]

# # Compare revenue and expenses
# compare_revenue_expenses(json_data)
