import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random
import plotly.express as px
import time

st.set_page_config(page_title="AI AQI Monitoring System", layout="wide")

# --------------------------------------------------
# AUTO REFRESH (30 seconds)
# --------------------------------------------------

if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

if time.time() - st.session_state.last_refresh > 30:
    st.session_state.last_refresh = time.time()
    st.rerun()

# Optional 1-second live mode
if st.sidebar.checkbox("Enable 1-Second Live Mode"):
    time.sleep(1)
    st.rerun()

# --------------------------------------------------
# TIMESTAMP DISPLAY
# --------------------------------------------------

current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"### 🕒 Last Updated: {current_time}")

st.title("🌫 AI-Powered Hyperlocal AQI Monitoring & Mitigation")
st.write("30-Minute Smart Prediction System for Colony-Level Deployment")

# --------------------------------------------------
# CPCB AQI CALCULATION (PM2.5)
# --------------------------------------------------

def calculate_aqi_pm25(concentration):
    breakpoints = [
        (0, 30, 0, 50),
        (31, 60, 51, 100),
        (61, 90, 101, 200),
        (91, 120, 201, 300),
        (121, 250, 301, 400),
        (251, 500, 401, 500)
    ]

    for bp in breakpoints:
        if bp[0] <= concentration <= bp[1]:
            Clow, Chigh, Ilow, Ihigh = bp
            aqi = ((Ihigh - Ilow)/(Chigh - Clow)) * (concentration - Clow) + Ilow
            return round(aqi)

    return 500


def get_aqi_category(aqi):
    if aqi <= 50:
        return "🟢 Good"
    elif aqi <= 100:
        return "🟡 Satisfactory"
    elif aqi <= 200:
        return "🟠 Moderate"
    elif aqi <= 300:
        return "🔴 Poor"
    elif aqi <= 400:
        return "🟣 Very Poor"
    else:
        return "🟤 Severe"

# --------------------------------------------------
# SIMULATED SENSOR DATA (4 NODES)
# --------------------------------------------------

def generate_sensor_data():
    pm25 = random.randint(80, 260)
    humidity = random.randint(40, 85)
    return pm25, humidity

nodes = {}

for i in range(1, 5):
    pm25, humidity = generate_sensor_data()
    aqi = calculate_aqi_pm25(pm25)
    category = get_aqi_category(aqi)

    nodes[f"Node {i}"] = {
        "PM2.5": pm25,
        "Humidity": humidity,
        "AQI": aqi,
        "Category": category
    }

# --------------------------------------------------
# LIVE SENSOR DASHBOARD
# --------------------------------------------------

st.header("📡 Real-Time 4-Node Sensor Dashboard")

cols = st.columns(4)

for i, (node, data) in enumerate(nodes.items()):
    with cols[i]:
        st.metric(node, f"AQI: {data['AQI']}")
        st.write(f"PM2.5: {data['PM2.5']} µg/m³")
        st.write(f"Humidity: {data['Humidity']}%")
        st.write(f"Category: {data['Category']}")

avg_aqi = np.mean([data["AQI"] for data in nodes.values()])
avg_humidity = np.mean([data["Humidity"] for data in nodes.values()])

st.subheader("🏘 Colony Average Conditions")
st.write(f"Average AQI: {round(avg_aqi)}")
st.write(f"Average Humidity: {round(avg_humidity)}%")

# --------------------------------------------------
# ROLLING 30-MINUTE AQI PREDICTION (Updates every 5 min)
# --------------------------------------------------

st.header("📈 Rolling 30-Minute AQI Forecast")

# Align to nearest 5-minute interval
now = datetime.datetime.now()
minute = (now.minute // 5) * 5
aligned_time = now.replace(minute=minute, second=0, microsecond=0)

future_times = pd.date_range(
    start=aligned_time,
    periods=7,   # 0 to 30 minutes
    freq="5min"
)

trend = np.linspace(avg_aqi, avg_aqi + 15, 7)
noise = np.random.normal(0, 4, 7)

predicted_values = np.clip(trend + noise, 50, 500)

df_future = pd.DataFrame({
    "Time": future_times,
    "Predicted AQI": predicted_values
})

fig = px.line(
    df_future,
    x="Time",
    y="Predicted AQI",
    markers=True,
    title="Next 30 Minutes AQI Prediction"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# AI DECISION ENGINE
# --------------------------------------------------

st.header("🧠 AI Mitigation Decision Engine")

max_predicted = max(predicted_values)

if max_predicted > 250:
    st.error("🚨 AQI expected to worsen significantly.")
elif max_predicted > 200:
    st.warning("⚠ AQI likely to enter Poor category.")
else:
    st.success("🌿 AQI expected to remain stable.")
