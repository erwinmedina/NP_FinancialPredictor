import requests
import json
import streamlit as st

def fetch_nonprofit_data(ein):
    url = f"https://projects.propublica.org/nonprofits/api/v2/organizations/{ein}.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def main():
    count = 1
    with open("eins.json", "r") as file:
        eins = json.load(file)
    results = []
    for i in range(100):
        count += 1
        data = fetch_nonprofit_data(eins[i])
        if data:
            results.append(data)
        print(count)
    

    # for ein in eins:
    #     count += 1
    #     data = fetch_nonprofit_data(ein)
    #     if data:
    #         results.append(data)
    #     print(count)
    with open("nonprofit_data.json", "w") as outfile:
        json.dump(results, outfile, indent=4)
    st.json(results)

if __name__ == "__main__":
    main()