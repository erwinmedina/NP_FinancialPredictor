import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["your_database_name"]  # Replace with your database name
collection = db["your_collection_name"]  # Replace with your collection name

# Fetch data from MongoDB
cursor = collection.find()

# Convert MongoDB cursor to pandas DataFrame
data = pd.DataFrame(list(cursor))

# Close MongoDB connection
client.close()

# Perform preprocessing and feature engineering as needed

# Split data into features (X) and target variable (y)
X = data.drop(columns=["financial_performance_metric"])
y = data["financial_performance_metric"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on test data
y_pred = model.predict(X_test)

# Evaluate model performance
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Optionally, fine-tune the model and make predictions on new data
