import streamlit as st
import requests

# Define the URL of the mock API endpoint
API_URL = 'https://projects.propublica.org/nonprofits/api/v2/organizations/94-1340523.json'

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
    st.title("Postman Mock API Data Viewer")

    # Fetch data from the mock API
    data = fetch_data()

    if data:
        st.subheader("Data from Postman Mock API")
        st.write(data)
    else:
        st.warning("No data available. Please check your API URL.")

if __name__ == "__main__":
    main()
