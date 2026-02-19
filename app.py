import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
import time

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(page_title="IoT AQI Monitoring System", layout="wide")

# -----------------------------------
# AUTO REFRESH (30 seconds default)
# -----------------------------------
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

refresh_interval = 30  # 30 seconds

if time.time() - st.session_state.last_refresh > refresh_interval:
    st.session_state.last_refresh = time.time()
    st.rerun()

# Optional 1-second live mode
live_mode = st.sidebar.checkbox("Enable 1-Second Live Mode")

if live_mode:
    time.sleep(1)
    st.rerun()

# -----------------------------------
# TIMESTAMP
# -----------------------------------
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"### 🕒 Last Updated: {current_time}")

# -----------------------------------
# SIMULATED 4 NODE DATA
# (Replace with real sensor data later)
# -----------------------------------
nodes = {
    "Node 1": {"PM2.5": np.random.randint(40, 200), "Humidity": np.random.randint(30, 80)},
    "Node 2": {"PM2.5": np.random.randint(40, 200), "Humidity": np.random.randint(30, 80)},
    "Node 3": {"PM2.5": np.random.randint(40, 200), "Humidity": np.random.randint(30, 80)},
    "Node 4": {"PM2.5": np.random.randint(40, 200), "Humidity": np.random.randint(30, 80)},
}

# -----------------------------------
# AQI COLOR FUNCTION
# -----------------------------------
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

# -----------------------------------
# DISPLAY 4 NODES
# -----------------------------------
cols = st.columns(4)

for i, (node, values) in enumerate(nodes.items()):
    pm25 = values["PM2.5"]
    humidity = values["Humidity"]

    color, category = get_aqi_color(pm25)

    with cols[i]:
        st.markdown(
            f"""
            <div style="
                background-color:{color};
                padding:20px;
                border-radius:15px;
                text-align:center;
                color:white;
                font-size:18px;
                font-weight:bold;">
                {node} <br><br>
                PM2.5 (AQI): {pm25} <br>
                Status: {category} <br><br>
                Humidity: {humidity}%
            </div>
            """,
            unsafe_allow_html=True
        )

# -----------------------------------
# SYSTEM DESCRIPTION
# -----------------------------------
st.markdown("### 📘 System Description")
st.write("""
• Four IoT sensor nodes monitor PM2.5 and Humidity.  
• AQI is color-coded based on standard air quality ranges.  
• Dashboard refreshes automatically every 30 seconds.  
• Optional 1-second live monitoring mode available.  
• Timestamp shows real-time system update.
""")
