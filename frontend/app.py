
import streamlit as st
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

st.title("SuperKart Sales Prediction App")
st.write(
    "Predict **Product_Store_Sales_Total** based on product and store details."
)

# Input fields for product and store data
Product_Weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
Product_Allocated_Area = st.number_input("Product Allocated Area", min_value=0.0, value=0.05, step=0.001, format="%.3f")
Product_MRP = st.number_input("Product MRP", min_value=0.0, value=150.0, step=1.0)
Store_Size = st.selectbox("Store Size", ["Small", "Medium", "High"])
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox(
    "Store Type",
    ["Grocery Store", "Supermarket Type1", "Supermarket Type2", "Supermarket Type3", "Food Mart", "Departmental Store"]
)
Product_Id_char = st.selectbox("Product ID Prefix (first 2 chars)", ["FD", "NC", "DR"])
Store_Establishment_Year = st.number_input("Store Establishment Year", min_value=1900, max_value=2100, value=2000, step=1)
Product_Type_Category = st.selectbox(
    "Product Type",
    [
        "Fruits and Vegetables", "Snack Foods", "Dairy", "Frozen Foods", "Household",
        "Baking Goods", "Canned", "Health and Hygiene", "Meat", "Soft Drinks",
        "Breads", "Hard Drinks", "Others", "Starchy Foods", "Breakfast", "Seafood"
    ],
)

product_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Id_char": Product_Id_char,
    "Store_Establishment_Year": int(Store_Establishment_Year),
    "Product_Type_Category": Product_Type_Category
}

if st.button("Predict", type='primary'):
    response = requests.post(f"{BACKEND_URL}/v1/sales/predict", json=product_data)
    if response.status_code == 200:
        result = response.json()
        predicted_sales = result["Sales"]
        st.write(f"Predicted Product Store Sales Total: ₹{predicted_sales:.2f}")
    else:
        st.error("Error in API request")
