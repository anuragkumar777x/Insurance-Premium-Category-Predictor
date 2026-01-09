import streamlit as st
import requests

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="💼",
    layout="centered"
)

# ---------------- Custom CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
}

h1 {
    text-align: center;
    color: #e5e7eb;
    font-weight: 700;
}

h3 {
    text-align: center;
    color: #94a3b8;
    font-weight: 400;
}

p, label {
    color: #cbd5f5 !important;
}

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    background-color: #020617;
    border-radius: 10px;
    border: 1px solid #1e293b;
}

.stButton > button {
    background: linear-gradient(90deg, #2563eb, #3b82f6);
    color: white;
    width: 100%;
    height: 48px;
    border-radius: 12px;
    font-size: 18px;
    font-weight: 600;
    border: none;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #1d4ed8, #2563eb);
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Title ----------------
st.title("Insurance Premium Category Predictor")
st.markdown("<h3>AI-Powered Risk Assessment</h3>", unsafe_allow_html=True)
st.markdown("---")

# ---------------- API ----------------
API_URL = "http://127.0.0.1:8000/predict"

# ---------------- Inputs ----------------
with st.container():
    age = st.text_input("Age", placeholder="Enter your age")
    weight = st.text_input("Weight (kg)", placeholder="Enter your weight in kilograms")
    height = st.text_input("Height (m)", placeholder="Enter your height in meters")
    income_lpa = st.text_input("Annual Income (LPA)", placeholder="Enter your annual income in LPA")
    smoker_choice = st.selectbox("Are you a smoker?", options=["Yes", "No"])
    smoker = True if smoker_choice == "Yes" else False
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

# ---------------- Prediction ----------------
st.markdown("")

if st.button("Predict Premium Category"):
    input_data = {
        "age": int(age),
        "weight": float(weight),
        "height": float(height),
        "income_lpa": float(income_lpa),
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        response = requests.post(API_URL, json=input_data)

        if response.status_code == 200:
            result = response.json()
            st.success(
                f"Predicted Insurance Premium Category: **{result['predicted_category']}**"
            )
        else:
            st.error(
                f"API Error: {response.status_code} - {response.text}"
            )

    except requests.exceptions.ConnectionError:
        st.error(
            "Could not connect to the FastAPI server. Make sure it's running on port 8000."
        )