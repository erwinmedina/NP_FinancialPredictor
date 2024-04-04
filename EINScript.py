import requests
import json

# Base URL of the API endpoint
base_url = 'https://projects.propublica.org/nonprofits/api/v2/search.json'

# Create an empty set to store unique EIN values
ein_set = set()

# Define the number of items per page and the total number of pages
items_per_page = 25  # Adjust this based on the API's pagination settings
total_pages = 399    # Assuming there are 400 pages in total

# Iterate through pages
for page_num in range(1, total_pages + 1):  # Pages are 1-indexed
    # Construct the URL with the current page number
    url = f'{base_url}?page={page_num}'

    # Send a GET request to the API endpoint for the current page
    response = requests.get(url)
    
    # Parse the JSON response
    data = response.json()
    
    # Extract the "organizations" array from the JSON response
    organizations = data['organizations']
    
    # Optional: Print progress
    print(f'Processed page {page_num}/{total_pages}')

    # Iterate over the organizations array and extract EIN values
    for org in organizations:
        ein = org['ein']
        ein_set.add(ein)

# Convert the set to a list
unique_eins = list(ein_set)

# Save the list to a JSON file
with open('eins.json', 'w') as file:
    json.dump(unique_eins, file)

print("EIN values saved to 'eins.json' file.")

