import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="AQI Monitor", layout="wide")

# -------------------------
# AUTO REFRESH (30 sec)
# -------------------------
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

refresh_interval = 30  # seconds

if time.time() - st.session_state.last_refresh > refresh_interval:
    st.session_state.last_refresh = time.time()
    st.rerun()

# -------------------------
# SIMULATED DATA (Replace with real sensor later)
# -------------------------
predicted_aqi = np.random.randint(50, 300)
predicted_humidity = np.random.randint(30, 90)

# -------------------------
# AQI COLOR INDICATOR
# -------------------------
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

color, category = get_aqi_color(predicted_aqi)

# -------------------------
# DISPLAY TIMESTAMP
# -------------------------
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"### 🕒 Last Updated: {current_time}")

# -------------------------
# AQI DISPLAY WITH COLOR
# -------------------------
st.markdown(
    f"""
    <div style="
        background-color:{color};
        padding:20px;
        border-radius:10px;
        text-align:center;
        color:white;
        font-size:28px;
        font-weight:bold;">
        AQI: {predicted_aqi} <br>
        Status: {category}
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------
# HUMIDITY DISPLAY
# -------------------------
st.metric("Humidity (%)", predicted_humidity)

# -------------------------
# OPTIONAL: 1 SECOND LIVE MODE
# -------------------------
live_mode = st.checkbox("Enable 1-Second Live Mode")

if live_mode:
    time.sleep(1)
    st.rerun()
