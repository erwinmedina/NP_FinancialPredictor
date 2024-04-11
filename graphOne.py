import os
import streamlit as st
import pandas as pd
import pymongo
from dotenv import load_dotenv

load_dotenv("./.env")
mongo_uri = os.environ.get("MONGODB_URI")
print(mongo_uri)

client = pymongo.MongoClient(mongo_uri)
db = client.get_database("nonprofit")
collection = db.get_collection("organization")

data = collection.find()  # Retrieve all documents from the collection

orgName = data[0]["organization"].get("name")
taxPeriodYear = []
totalRevenue = []

def main():
    for filings in data[0]["filings_with_data"]:
        taxPeriodYear.append(filings.get("tax_prd_yr"))
        totalRevenue.append(filings.get("totrevenue"))
    
    chart_data = pd.DataFrame({"Tax Year": taxPeriodYear, "Total Revenue": totalRevenue})
    chart_data = chart_data.set_index("Tax Year")
    st.subheader(orgName)
    st.subheader("Total Revenue Over Time")
    st.bar_chart(chart_data)

    client.close()

 
if __name__ == "__main__":
    main()