import streamlit as st
import pandas as pd
import joblib
import openai
openai.api_key =st.secrets ["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"]

# Load model
model = joblib.load("sdg6_water_model.pkl")

# Page setup
st.set_page_config(page_title="SDG 6: Clean Water Predictor", layout="centered")
st.title("💧WaterBot")

# Tabs
tab1, tab2 = st.tabs(["🔍 Predict Water Quality", "💬 Ask SDG 6 Chatbot"])

# --- Prediction tab ---
with tab1:
    st.subheader("📥 Enter Water Parameters")

    pH = st.slider("pH (Ideal 6.5–8.5)", 0.0, 14.0, 7.0)
    hardness = st.number_input("Hardness", 0.0, 500.0, 150.0)
    solids = st.number_input("Solids (ppm)", 0.0, 50000.0, 20000.0)
    chloramines = st.number_input("Chloramines", 0.0, 15.0, 6.5)
    sulfate = st.number_input("Sulfate", 0.0, 500.0, 250.0)
    conductivity = st.number_input("Conductivity", 0.0, 1000.0, 400.0)
    organic_carbon = st.number_input("Organic Carbon", 0.0, 50.0, 10.0)
    trihalomethanes = st.number_input("Trihalomethanes", 0.0, 120.0, 45.0)
    turbidity = st.number_input("Turbidity (NTU)", 0.0, 10.0, 3.5)

    if st.button("Predict"):
        features = pd.DataFrame([[pH, hardness, solids, chloramines, sulfate,
                                  conductivity, organic_carbon, trihalomethanes, turbidity]],
                                columns=['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate',
                                         'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity'])

        pred = model.predict(features)[0]
        prob = model.predict_proba(features).max()

        if pred == 1:
            st.success(f"✅ Water is likely SAFE to drink (Confidence: {prob:.2%})")
        else:
            st.error(f"⚠️ Water is likely UNSAFE to drink (Confidence: {prob:.2%})")

# --- Chatbot tab ---
with tab2:
    st.subheader("💬 Ask me about SDG 6 or water safety")

    user_q = st.text_input("Your question:")

    def simple_bot_response(query):
        query = query.lower()
        if "sdg 6" in query:
            return "SDG 6 aims to ensure clean water and sanitation for all by 2030."
        elif "pH" in query:
            return "Safe drinking water usually has a pH between 6.5 and 8.5."
        elif "turbidity" in query:
            return "Turbidity measures how clear the water is. Lower is safer."
        elif "how to clean water" in query:
            return "Boiling, filtering, or using chlorination are ways to clean water."
        else:
            return "I'm here to help with water quality and SDG 6 questions!"

    if user_q:
        st.info(simple_bot_response(user_q))
