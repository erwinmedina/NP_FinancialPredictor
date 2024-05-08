import requests
import json

# **************************************************************************************************************** #
# This script simply obtained a giant list of EIN values for us to utilize and retrieve data for each organization #
# **************************************************************************************************************** #

# Base URL of the API endpoint
base_url = 'https://projects.propublica.org/nonprofits/api/v2/search.json'

# Create an empty set to store unique EIN values
ein_set = set()

# Define the number of items per page and the total number of pages
items_per_page = 25 
total_pages = 399

# Iterate through pages
for page_num in range(1, total_pages + 1):

    url = f'{base_url}?page={page_num}'
    response = requests.get(url)
    data = response.json()
    organizations = data['organizations']
    print(f'Processed page {page_num}/{total_pages}')

    for org in organizations:
        ein = org['ein']
        ein_set.add(ein)

unique_eins = list(ein_set)

with open('eins.json', 'w') as file:
    json.dump(unique_eins, file)

print("EIN values saved to 'eins.json' file.")

