import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import pymongo

load_dotenv("./.env")
mongo_uri = os.environ.get("MONGODB_URI")
client = pymongo.MongoClient(mongo_uri)
db = client.get_database("nonprofit")
collection = db.get_collection('organization_10k_original')

def predict_totrevenue(ein):
    # Finds the organization and its corresponding filing data for that EIN value
    organization = collection.find_one({'organization.ein': ein})
    filings_with_data = organization["filings_with_data"]
    
    # Extract relevant features from filings_with_data
    features_list = []
    filing_years = []
    for filing in filings_with_data:
        features = {
            "totfuncexpns": filing.get("totfuncexpns", np.nan),
            "totassetsend": filing.get("totassetsend", np.nan),
            "totliabend": filing.get("totliabend", np.nan),
            "compnsatncurrofcr": filing.get("compnsatncurrofcr", np.nan),
            "othrsalwages": filing.get("othrsalwages", np.nan),
            "payrolltx": filing.get("payrolltx", np.nan),
            "invstmntinc": filing.get("invstmntinc", np.nan),
            "miscrevtot11e": filing.get("miscrevtot11e", np.nan),
            "netrntlinc": filing.get("netrntlinc", np.nan),
            "netincsales": filing.get("netincsales", np.nan),
            "netincfndrsng": filing.get("netincfndrsng", np.nan),
            "netincgaming": filing.get("netincgaming", np.nan),
            "grsincfndrsng": filing.get("grsincfndrsng", np.nan),
            "grsincgaming": filing.get("grsincgaming", np.nan),
            "secrdmrtgsend": filing.get("secrdmrtgsend", np.nan),
            "retainedearnend": filing.get("retainedearnend", np.nan),
            "totnetassetend": filing.get("totnetassetend", np.nan),
            "nonpfrea": filing.get("nonpfrea", np.nan),
            "totrevenue": filing.get("totrevenue", np.nan)
        }
        features_list.append(features)
        filing_years.append(filing.get("tax_prd_yr", np.nan))

    # Create DataFrame with features
    df = pd.DataFrame(features_list)

    # Convert non-numeric values to NaN
    df.replace(['', '  '], np.nan, inplace=True)

    # Convert all data to numeric type
    df = df.apply(pd.to_numeric, errors='coerce')

    # Impute missing values with median
    imputer = SimpleImputer(strategy='median')
    df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

    # Split data into features (X) and target variable (y)
    X = df_imputed.drop(columns=["totrevenue"])  # Features
    y = df_imputed["totrevenue"]  # Target variable

    # Initialize and train Random Forest Regressor model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Predict revenue for each entry in the dataset
    predicted_revenue = model.predict(X)

    # Calculate coefficients of the line of best fit
    coefficients = np.polyfit(filing_years, predicted_revenue, 1)
    line_of_best_fit = np.polyval(coefficients, filing_years)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(filing_years, df["totrevenue"], label="Actual Revenue")
    plt.plot(filing_years, predicted_revenue, 'ro-', label="Predicted Revenue")
    plt.plot(filing_years, line_of_best_fit, 'g--', label="Line of Best Fit")

    # Extend x-axis range for future predictions
    future_years = np.arange(min(filing_years), max(filing_years) + 3)  # Assuming 1 entry per year
    future_predicted_revenue = np.polyval(coefficients, future_years)
    plt.plot(future_years, future_predicted_revenue, 'b--', label="Predicted Revenue (Future)")

    plt.title("Predicted Total Revenue")
    plt.xlabel("Year")
    plt.ylabel("Total Revenue")
    plt.legend()
    plt.grid(True)
    plt.show()

# Provide the EIN of the organization for prediction
organization_ein = 132986881
predict_totrevenue(organization_ein)
