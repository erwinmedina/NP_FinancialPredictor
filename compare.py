# NORMALIZED REVENUE
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
print(df_revenue)
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












# # NORMALIZED EXPENSES
# import pandas as pd
# import os
# import json
# import matplotlib.pyplot as plt

# # Get the absolute path to the directory containing the script
# script_dir = os.path.dirname(os.path.abspath(__file__))
# # Construct the absolute path to the JSON file
# json_file_path = os.path.join(script_dir, 'nonprofit_data.json')

# # Load data from JSON file
# with open(json_file_path, 'r') as file:
#     data = json.load(file)

# expense_data = []
# expense_amount = []
# # Iterate over each organization
# for organization in data:
#     # Extract organization information
#     org_id = organization['organization']['id']
#     org_name = organization['organization']['name']

#     # Extract totfuncexpns for each filing and calculate average
#     totfuncexpns_list = []
#     for filing in organization['filings_with_data']:
#         totfuncexpns_list.append(filing['totfuncexpns'])
    
#     # Calculate average totfuncexpns
#     average_totfuncexpns = sum(totfuncexpns_list) / len(totfuncexpns_list) if totfuncexpns_list else 0
#     expense_amount.append(average_totfuncexpns)

#     # Print results
#     # print(f"Organization ID: {org_id}")
#     # print(f"Organization Name: {org_name}")
#     # print(f"Average totfuncexpns: {average_totfuncexpns}")
#     # print()
#     # print(average_totfuncexpns)

# # Extract state for each organization
# counter = 0
# for entry in data:
#     state = entry["organization"]["state"]
#     # expense_data.append({"State": state, "Expense Amount": expense_amount})
#     expense_data.append({"State": state, "Expense Amount": expense_amount[counter]})
#     counter+=1

# # Convert data to DataFrame
# df_expense = pd.DataFrame(expense_data)
# print(df_expense)
# # Calculate average revenue_amount per state
# df_average_expense = df_expense.groupby('State').mean().reset_index()

# # GDP per capita data with state abbreviations
# gdp_per_capita = {
#     'State': ['NY', 'VA', 'NC', 'MA', 'NH', 'TN', 'AK', 'PA', 'MI', 'CT', 'IA', 'MO', 'CA', 'KS', 'NM', 'ND', 
#               'SD', 'AZ', 'WA', 'WI', 'FL', 'WY', 'OH', 'ME', 'DE', 'OR', 'MT', 'NJ', 'RI', 'KY', 'MD', 'UT', 
#               'AL', 'IL', 'GA', 'SC', 'CO', 'LA', 'ID', 'MN', 'OK', 'WV', 'TX', 'IN', 'AR', 'NE', 'NV', 'MS', 
#               'HI', 'VT', 'DC'],
#     'GDP per Capita': [73531, 55929, 47778, 72635, 55744, 47695, 70936, 55602, 46858, 67784,
#                         54101, 46064, 67698, 52297, 44187, 67308, 51997, 43096, 67242, 51575,
#                         43052, 66413, 51456, 42356, 66023, 50996, 42173, 62263, 50827, 41659,
#                         60886, 49740, 40279, 59980, 49663, 39883, 59057, 49606, 39843, 59057,
#                         48954, 39495, 58417, 48738, 38467, 58141, 48189, 34029, 56880, 47921,
#                         176534]  # GDP per capita in dollars
# }

# # Convert GDP per capita data to DataFrame
# df_gdp_per_capita = pd.DataFrame(gdp_per_capita)

# # Merge DataFrames on 'State'
# df_merged = pd.merge(df_average_expense, df_gdp_per_capita, left_on='State', right_on='State')

# # Normalize average revenue with GDP per capita
# df_merged['Normalized Expense'] = df_merged['Expense Amount'] / df_merged['GDP per Capita']

# # Plotting
# plt.figure(figsize=(12, 8))
# plt.bar(df_merged['State'], df_merged['Normalized Expense'], color='skyblue')
# plt.xlabel('State')
# plt.ylabel('Normalized Expenses')
# plt.title('Normalized Expenses by State')
# plt.xticks(rotation=90)
# plt.tight_layout()
# plt.show()
