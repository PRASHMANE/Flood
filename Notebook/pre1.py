import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

# --- Page config ---
st.set_page_config(page_title="🌊 Flood Prediction Dashboard", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        font-size: 18px;
        border-radius: 8px;
        height: 50px;
        width: 150px;
        margin-top: 10px;
    }
    .stNumberInput>div>input {
        font-size: 18px;
        height: 40px;
        border-radius: 5px;
    }
    h1 {
        color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌊 Flood Prediction Dashboard")

# --- Load pre-trained model and scaler ---
# Replace these with your actual files
# model = joblib.load("xgb_flood_model.pkl")
# scaler = joblib.load("scaler.pkl")

# --- Input form ---
st.subheader("Enter Flood Parameters")
rainfall = st.number_input("Rainfall (mm)", min_value=0.0, value=10.0)
humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=70.0)
river_level = st.number_input("River Level (m)", min_value=0.0, value=3.0)
temperature = st.number_input("Temperature (°C)", min_value=-10.0, max_value=50.0, value=28.0)

if st.button("Predict Flood Risk"):
    # --- Prepare input ---
    X_new = pd.DataFrame([[rainfall, humidity, river_level, temperature]],
                         columns=["rainfall_mm", "humidity_percent", "river_level_m", "temperature_c"])
    
    # Uncomment if you have scaler
    # X_new_scaled = scaler.transform(X_new)

    # For demo, simulate flood risk probability
    prob_flood = min((rainfall/100 + humidity/100 + river_level/10)/3, 1)  # dummy probability
    flood_risk = 1 if prob_flood > 0.5 else 0

    # --- Display results in graph ---
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Flood Risk Probability", "No Flood Probability"],
        y=[prob_flood, 1-prob_flood],
        marker_color=["red", "green"]
    ))
    fig.update_layout(title_text=f"Flood Risk Prediction: {'YES ⚠️' if flood_risk==1 else 'NO ✅'}",
                      yaxis=dict(title="Probability"),
                      template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)
