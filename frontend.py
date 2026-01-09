import streamlit as st
import requests

API_URL = "https://insurance-premium-category-predictor-excd.onrender.com/predict"

st.title("Insurance Premium Category Predictor")

age = st.number_input("Age", min_value=1, max_value=120)
weight = st.number_input("Weight (kg)", min_value=1.0)
height = st.number_input("Height (meters)", min_value=0.5, max_value=2.5)
income_lpa = st.number_input("Income (LPA)", min_value=0.1)
smoker = st.checkbox("Smoker")
city = st.text_input("City")
occupation = st.selectbox(
    "Occupation",
    [
        "Student", "Engineer", "HR Executive", "Designer",
        "Sales Executive", "Data Analyst", "Software Engineer",
        "Manager", "Architect", "Entrepreneur", "Business Owner",
        "Contractor", "Teacher", "Factory Manager", "Pensioner"
    ]
)

if st.button("Predict"):
    payload = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=10)

        if response.status_code == 200:
            st.success(f"Predicted Category: {response.json()['predicted_category']}")
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException:
        st.error("Could not connect to the FastAPI server.")
