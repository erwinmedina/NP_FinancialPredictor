import json

# Open the JSON file containing the EIN values
with open('eins.json', 'r') as file:
    ein_list = json.load(file)

# Print the length of the list
print("Number of EIN values:", len(ein_list))
