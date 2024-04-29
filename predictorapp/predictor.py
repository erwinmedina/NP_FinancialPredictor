import io
import os
import pymongo
import base64
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from django.http import JsonResponse
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from dotenv import load_dotenv
from sklearn.preprocessing import PolynomialFeatures

# ********************************************************
# -----------------TOTREVENUE PREDICTOR-------------------
# ********************************************************
def predict_total_revenue(ein):

    load_dotenv("./.env")
    mongo_uri = os.environ.get("MONGODB_URI")
    client = pymongo.MongoClient(mongo_uri)
    db = client.get_database("nonprofit")
    collection = db.get_collection('organization_10k_original')

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
    years_df = pd.DataFrame(filing_years, columns=['Year'])

    # Initialize Linear Regression and Fit With Data
    linear_regressor = LinearRegression()
    linear_regressor.fit(years_df, predicted_revenue)

    # Get the line of best fit
    line_of_best_fit = linear_regressor.predict(years_df)

    plt.figure(figsize=(10, 6))
    plt.plot(filing_years, df["totrevenue"], label="Actual Revenue")
    plt.plot(filing_years, line_of_best_fit, label='Line of Best Fit')
    plt.plot(filing_years, predicted_revenue, 'ro-', label="Predicted Revenue")

    # Extend x-axis range for future predictions
    future_years = np.arange(min(filing_years), max(filing_years) + 3)  # Assuming 1 entry per year

    # Initialize polynomial features to create a polynomial graph
    poly_features = PolynomialFeatures(degree=4)
    years_poly = poly_features.fit_transform(years_df)
    future_years_poly = poly_features.fit_transform(pd.DataFrame(future_years, columns=['Year']))

    linear_regressor_future = LinearRegression()
    linear_regressor_future.fit(years_poly, predicted_revenue)
    future_predicted_revenue = linear_regressor_future.predict(future_years_poly)

    plt.plot(future_years, future_predicted_revenue, 'b--', label="Predicted Revenue (Future)")
    plt.xlabel('Filing Years')
    plt.ylabel('Predicted Revenue')
    plt.title('Predicted Total Revenue')
    plt.legend()
    plt.grid()

    # Save the plot to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Encode the plot image as a base64 string
    plot_image_revenue = base64.b64encode(buffer.getvalue()).decode()

    return JsonResponse({'plot_image_revenue': plot_image_revenue})

# ********************************************************
# ----------------TOTFUNCEXPNS PREDICTOR------------------
# ********************************************************
def predict_total_expenses(ein):

    load_dotenv("./.env")
    mongo_uri = os.environ.get("MONGODB_URI")
    client = pymongo.MongoClient(mongo_uri)
    db = client.get_database("nonprofit")
    collection = db.get_collection('organization_10k_original')

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
    X = df_imputed.drop(columns=["totfuncexpns"])  # Features
    y = df_imputed["totfuncexpns"]  # Target variable

    # Initialize and train Random Forest Regressor model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Predict revenue for each entry in the dataset
    predicted_expenses = model.predict(X)
    years_df = pd.DataFrame(filing_years, columns=['Year'])

    # Initialize Linear Regression + Fit with Data
    linear_regressor = LinearRegression()
    linear_regressor.fit(years_df, predicted_expenses)

    # Get the line of best fit
    line_of_best_fit = linear_regressor.predict(years_df)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(filing_years, df["totfuncexpns"], label="Actual Expenses")
    plt.plot(filing_years, line_of_best_fit, label="Line of Best Fit")
    plt.plot(filing_years, predicted_expenses, 'ro-', label="Predicted Expenses")

    # Extend x-axis range for future predictions
    future_years = np.arange(min(filing_years), max(filing_years) + 3)  # Assuming 1 entry per year
    
    # Initialize polynomial features to create a polynomial graph
    poly_features = PolynomialFeatures(degree=4)
    years_poly = poly_features.fit_transform(years_df)
    future_years_poly = poly_features.fit_transform(pd.DataFrame(future_years, columns=["Year"]))

    linear_regressor_future = LinearRegression()
    linear_regressor_future.fit(years_poly, predicted_expenses)
    future_predicted_expenses = linear_regressor_future.predict(future_years_poly)
    
    plt.plot(future_years, future_predicted_expenses, 'b--', label="Predicted Expenses (Future)")
    plt.title("Predicted Total Functional Expenses")
    plt.xlabel("Filing Years")
    plt.ylabel("Total Functional Expenses")
    plt.legend()
    plt.grid()

    # Save the plot to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Encode the plot image as a base64 string
    plot_image_expense = base64.b64encode(buffer.getvalue()).decode()

    return JsonResponse({'plot_image_expense': plot_image_expense})