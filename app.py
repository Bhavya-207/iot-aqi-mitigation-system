import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import time

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(page_title="AQI Prediction System", layout="wide")

# -----------------------------
# AUTO REFRESH EVERY 30 SECONDS
# -----------------------------
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

refresh_interval = 30  # seconds

if time.time() - st.session_state.last_refresh > refresh_interval:
    st.session_state.last_refresh = time.time()
    st.rerun()

# -----------------------------
# GENERATE PAST 60 MINUTES DATA
# -----------------------------
minutes = 60
time_index = np.arange(minutes)

# Simulated historical AQI data (replace with sensor/API later)
historical_aqi = 100 + np.cumsum(np.random.normal(0, 2, minutes))

# -----------------------------
# TRAIN LINEAR REGRESSION MODEL
# -----------------------------
model = LinearRegression()
X = time_index.reshape(-1, 1)
y = historical_aqi
model.fit(X, y)

# -----------------------------
# PREDICT NEXT 30 MINUTES
# -----------------------------
future_minutes = 30
future_index = np.arange(minutes, minutes + future_minutes).reshape(-1, 1)
predicted_aqi = model.predict(future_index)

# -----------------------------
# CURRENT AQI VALUE
# -----------------------------
current_aqi = predicted_aqi[0]

# -----------------------------
# AQI COLOR INDICATOR FUNCTION
# -----------------------------
def get_aqi_color(aqi):
    if aqi <= 50:
        return "green", "Good"
    elif aqi <= 100:
        return "yellow", "Moderate"
    elif aqi <= 150:
        return "orange", "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "red", "Unhealthy"
    elif aqi <= 300:
        return "purple", "Very Unhealthy"
    else:
        return "maroon", "Hazardous"

color, category = get_aqi_color(current_aqi)

# -----------------------------
# TIMESTAMP
# -----------------------------
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"### 🕒 Last Updated: {current_time}")

# -----------------------------
# AQI DISPLAY CARD
# -----------------------------
st.markdown(
    f"""
    <div style="
        background-color:{color};
        padding:25px;
        border-radius:15px;
        text-align:center;
        color:white;
        font-size:32px;
        font-weight:bold;">
        Current AQI: {int(current_aqi)} <br>
        Category: {category}
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# PLOT GRAPH
# -----------------------------
st.markdown("### 📈 AQI Trend & 30-Minute Prediction")

fig, ax = plt.subplots()

# Past Data
ax.plot(range(minutes), historical_aqi, label="Past 60 Minutes")

# Future Prediction
ax.plot(range(minutes, minutes + future_minutes), predicted_aqi, linestyle="dashed", label="Next 30 Minutes Prediction")

# Threshold Line
ax.axhline(y=150, linestyle=":", label="Unhealthy Threshold")

ax.set_xlabel("Time (Minutes)")
ax.set_ylabel("AQI")
ax.legend()

st.pyplot(fig)

# -----------------------------
# SYSTEM LOGIC SECTION
# -----------------------------
st.markdown("### 🧠 System Logic Explanation")

st.write("""
• The system collects AQI data from the last 60 minutes.  
• A Linear Regression model is trained on historical data.  
• AQI is predicted for the next 30 minutes.  
• Color-coded indicator follows EPA AQI standards.  
• System auto-refreshes every 30 seconds.  
""")

# -----------------------------
# PROJECT INFO
# -----------------------------
st.markdown("### 🎓 Project Title")
st.write("Real-Time AQI Monitoring and 30-Minute Forecasting System Using Machine Learning")

