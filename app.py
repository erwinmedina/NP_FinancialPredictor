import streamlit as st
import requests
import streamlit as st
import pandas as pd
import numpy as np
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


# client = pymongo.MongoClient("mongodb+srv://erwinlmedina:ALufXMuib82KO6cc@cluster0.zsupnfu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# db = client.get_database("sample_mflix")
# collection = db.get_collection("users")

# data = collection.find()  # Retrieve all documents from the collection


uri = "mongodb+srv://erwinlmedina:TIvSHgLjsxURxrMV@cluster0.zsupnfu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



# # Define the URL of the mock API endpoint
# API_URL = 'https://projects.propublica.org/nonprofits/api/v2/search.json'

# def fetch_data():
#     try:
#         response = requests.get(API_URL)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             st.error(f"Failed to fetch data. Status code: {response.status_code}")
#             return None
#     except Exception as e:
#         st.error(f"An error occurred: {str(e)}")
#         return None

def main():
    # st.title("Nonprofit Financial Analysis")

    # st.text("Our goal is to provide publicly available financial information about nonprofit organizations and predict their success in the future.")

    # # Fetch data from the mock API
    # data = fetch_data()

    # if data:
    #     st.subheader("Data from Postman Mock API")
    #     st.write(data)
    # else:
    #     st.warning("No data available. Please check your API URL.")

    # chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

    # st.subheader("Financial Development Over Last 5 Years")
    # st.line_chart(chart_data)

    # st.subheader("Predicted Financial Development Over Next 5 Years")
        
    # # Display data in Streamlit app
    # st.title("MongoDB Data Viewer")

    # # Display each document in the collection
    # for doc in data:
    #     st.write(doc)

    # Close MongoDB connection
    client.close()




    # st.title("Postman Mock API Data Viewer")

    # # Fetch data from the mock API
    # data = fetch_data()

    # if data:
    #     st.subheader("Data from Postman Mock API")

    #     # Add a search bar
    #     search_term = st.text_input("Search", "")

    #     # Filter data based on search term
    #     filtered_data = [item for item in data if search_term.lower() in str(item).lower()]

    #     if filtered_data:
    #         st.write(filtered_data)
    #     else:
    #         st.warning("No matching data found.")
    # else:
    #     st.warning("No data available. Please check your API URL.")

if __name__ == "__main__":
    main()
