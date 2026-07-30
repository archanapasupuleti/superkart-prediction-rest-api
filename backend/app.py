
# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API
from pathlib import Path

# Initialize Flask app with a name
superkart_api = Flask("superkart_sales_app")

# Load the trained churn prediction model

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "product_store_sales_prediction_model_v1_0.joblib"

model = joblib.load(MODEL_PATH)
# Define a route for the home page
@superkart_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a welcome message and some help on the endpoints supported.
    """
    #logger.info("Home endpoint accessed")

    html = """
      <!DOCTYPE html>
      <html>
      <head>
        <title>SuperKart Sales API</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
            background-color: #f4f4f4;
          }
          h1 {
            color: #333;
            font-size: 3em;
          }
          p {
            color: #666;
            font-size: 1.5em;
            margin-top: 20px;
          }
        </style>
      </head>
      <body>
        <h1>Welcome to SuperKart Sales Prediction API.</h1>
        <p>To obtain sales predictions, please send a POST request to `/v1/sales/predict`.</p>
      </body>
      </html>
    """
    return html

# Define an endpoint to predict churn for a single customer
@superkart_api.post('/v1/sales/predict')
def predict_sales():
    # Get JSON data from the request
    data = request.get_json()

    # Extract relevant customer features from the input data. The order of the column names matters.
    sample = {
        'Product_Weight': data['Product_Weight'],
        'Product_Sugar_Content': data['Product_Sugar_Content'],
        'Product_Allocated_Area': data['Product_Allocated_Area'],
        'Product_MRP': data['Product_MRP'],
        'Store_Size': data['Store_Size'],
        'Store_Location_City_Type': data['Store_Location_City_Type'],
        'Store_Type': data['Store_Type'],
        'Product_Id_char': data['Product_Id_char'],
        'Store_Establishment_Year': data['Store_Establishment_Year'],
        'Product_Type_Category': data['Product_Type_Category']
    }

    # Convert the extracted data into a DataFrame
    input_data = pd.DataFrame([sample])

    # Make a churn prediction using the trained model
    prediction = model.predict(input_data).tolist()[0]

    # Return the prediction as a JSON response
    return jsonify({'Sales': prediction})


# Run the Flask app in debug mode
if __name__ == '__main__':
    superkart_api.run(debug=True)
