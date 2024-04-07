import streamlit as st
import requests
import streamlit as st
import pandas as pd
import numpy as np

# Define the URL of the mock API endpoint
API_URL = 'https://projects.propublica.org/nonprofits/api/v2/search.json'

def fetch_data():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def main():
    st.title("Nonprofit Financial Analysis")

    st.text("Our goal is to provide publicly available financial information about nonprofit organizations and predict their success in the future.")

    # Fetch data from the mock API
    data = fetch_data()

    if data:
        st.subheader("Data from Postman Mock API")
        st.write(data)
    else:
        st.warning("No data available. Please check your API URL.")

    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

    st.subheader("Financial Development Over Last 5 Years")
    st.line_chart(chart_data)

    st.subheader("Predicted Financial Development Over Next 5 Years")
        



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
