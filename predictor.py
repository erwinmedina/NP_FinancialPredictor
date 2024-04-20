# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import mean_squared_error
# import pymongo

# # Connect to MongoDB
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client["your_database_name"]  # Replace with your database name
# collection = db["your_collection_name"]  # Replace with your collection name

# # Fetch data from MongoDB
# cursor = collection.find()

# # Convert MongoDB cursor to pandas DataFrame
# data = pd.DataFrame(list(cursor))

# # Close MongoDB connection
# client.close()

# # Perform preprocessing and feature engineering as needed

# # Split data into features (X) and target variable (y)
# X = data.drop(columns=["financial_performance_metric"])
# y = data["financial_performance_metric"]

# # Split data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Initialize and train linear regression model
# model = LinearRegression()
# model.fit(X_train, y_train)

# # Make predictions on test data
# y_pred = model.predict(X_test)

# # Evaluate model performance
# mse = mean_squared_error(y_test, y_pred)
# print("Mean Squared Error:", mse)

# # Optionally, fine-tune the model and make predictions on new data


import os
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Get the absolute path to the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the absolute path to the JSON file
json_file_path = os.path.join(script_dir, 'nonprofit_data.json')

# Load data from JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Extract relevant features from JSON data
def extract_features(filings):
    features = {
        "totfuncexpns": [],
        "totassetsend": [],
        "totliabend": []
        # Add more features as needed
    }
    for filing in filings:
        features["totfuncexpns"].append(filing.get("totfuncexpns", np.nan))
        features["totassetsend"].append(filing.get("totassetsend", np.nan))
        features["totliabend"].append(filing.get("totliabend", np.nan))
        # Add more features as needed
    return features


# Apply feature extraction function to each row
features_list = [extract_features(entry["filings_with_data"]) for entry in data]

# Create DataFrame with features
df = pd.DataFrame(features_list)

# Check the shape and head of the DataFrame
print("DataFrame Shape:", df.shape)
print("DataFrame Head:\n", df.head())

# Fill NaN values with zeros
df.fillna(0, inplace=True)

# Check for missing values
print("Missing Values:\n", df.isnull().sum())

# Split data into features (X) and target variable (y)
X = df
y = pd.Series([entry["filings_with_data"]["totrevenue"] for entry in data])  # Assuming totrevenue is the target variable

# Print sample of target variable (y)
print("Sample of Target Variable (y):\n", y.head())

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Flatten the nested lists in X_train
X_train_flat = pd.DataFrame({col: np.concatenate(X_train[col].values) for col in X_train.columns})

# Flatten the nested lists in X_test similarly
X_test_flat = pd.DataFrame({col: np.concatenate(X_test[col].values) for col in X_test.columns})

# Initialize and train linear regression model
model = LinearRegression()
model.fit(X_train_flat, y_train)

# Make predictions on test data
y_pred = model.predict(X_test_flat)

# Evaluate model performance
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)
