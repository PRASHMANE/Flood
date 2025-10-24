import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go

# Load model and scaler once
model = joblib.load("C:/Users/User/OneDrive/Documents/Flood_Monitor/xgb_flood_model.pkl")
scaler = joblib.load("C:/Users/User/OneDrive/Documents/Flood_Monitor/scaler.pkl")

def pre():
    st.title("🌊 Flood Prediction Dashboard")

    # Input fields initially empty
    rainfall = st.number_input("Rainfall (mm)", min_value=0.0, value=None, key="rainfall")
    humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=None, key="humidity")
    river_level = st.number_input("River Level (m)", min_value=0.0, value=None, key="river_level")
    temperature = st.number_input("Temperature (°C)", min_value=-10.0, max_value=50.0, value=None, key="temperature")

    # --- Automatically predict if all inputs are entered ---
    if None not in [rainfall, humidity, river_level, temperature]:
        # Prepare input
        X_new = pd.DataFrame([[rainfall, humidity, river_level, temperature]],
                             columns=["rainfall_mm", "humidity_percent", "river_level_m", "temperature_c"])
        X_new_scaled = scaler.transform(X_new)
        flood_risk = model.predict(X_new_scaled)[0]  # 0 or 1

        # Display graph
        prob_flood = 0.7 if flood_risk == 1 else 0.3
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=["Flood Risk Probability", "No Flood Probability"],
            y=[prob_flood, 1 - prob_flood],
            marker_color=["red", "green"]
        ))
        fig.update_layout(title_text=f"Flood Risk Prediction: {'YES ⚠️' if flood_risk==1 else 'NO ✅'}",
                          yaxis=dict(title="Probability"),
                          template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Please enter all input values to see the prediction.")

def pre1():
    pre()

# Run the app
if __name__ == "__main__":
    pre1()
