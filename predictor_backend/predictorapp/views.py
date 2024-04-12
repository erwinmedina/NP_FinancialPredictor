from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FinancialRecord
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Create your views here.

def get_financial_records(request):
    # Retrieve all financial records from the database
    records = FinancialRecord.objects.all().values()
    return JsonResponse(list(records), safe=False)

def add_financial_record(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Create a new financial record
        record = FinancialRecord.objects.create(
            category=data['category'],
            amount=data['amount'],
            date=data['date'],
            description=data['description']
        )
        return JsonResponse({'message': 'Financial record added successfully'})
    else:
        return JsonResponse({'error': 'POST request required'})

@csrf_exempt
def ml_endpoint(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Step 1: Data Preprocessing
        def preprocess_data(json_data):
            # Convert JSON data to DataFrame
            df = pd.DataFrame(json_data['fillings_with_data'])
            
            # Drop irrelevant columns and columns with missing values
            df.drop(['tax_pd', 'nonpfrea'], axis=1, inplace=True)
            df.dropna(inplace=True)
            
            return df
        
        # Select relevant features for prediction
        selected_features = ['totrevenue', 'totfuncexpns', 'totassestsend', 'totliabend', 'pct_compnsatncurrofcr']
        
        # Step 2: Feature Selection
        def select_features(df):
            X = df[selected_features]
            y = df['financial_success']  # Assuming this is the target variable
            return X, y
        
        # Step 3: Model Training
        def train_model(X_train, y_train):
            # Initialize and train the model
            model = RandomForestClassifier()
            model.fit(X_train, y_train)
            return model
        
        # Step 4: Model Evaluation
        def evaluate_model(model, X_test, y_test):
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Calculate accuracy
            accuracy = accuracy_score(y_test, y_pred)
            print("Accuracy:", accuracy)
        
        # Step 5: Prediction
        def predict_new_data(model, new_data):
            # Preprocess new data
            new_df = preprocess_data(new_data)
            
            # Select features
            X_new = new_df[selected_features]
            
            # Make predictions
            predictions = model.predict(X_new)
            
            return predictions
        
        # Load JSON data
        with open('nonprofit_data.json') as f:
            data = json.load(f)
        
        # Preprocess data
        df = preprocess_data(data)
        
        # Select features
        X, y = select_features(df)
        
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train the model
        model = train_model(X_train, y_train)
        
        # Evaluate the model
        evaluate_model(model, X_test, y_test)
        
        # Example of predicting new data
        new_data = { ... }  # New organization data
        predictions = predict_new_data(model, new_data)
        
        return JsonResponse({'predictions': predictions})
    else:
        return JsonResponse({'error': 'POST request required'})
