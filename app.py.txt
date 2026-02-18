import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random
import plotly.express as px

st.set_page_config(page_title="IoT AQI Mitigation System", layout="wide")

st.title("🌫 IoT-Based Hyperlocal AQI Monitoring & Mitigation System")
st.write("Prototype for Delhi Colony Deployment")

# ---------------------------
# CPCB AQI CALCULATION (PM2.5)
# ---------------------------

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
        return "Good", "green"
    elif aqi <= 100:
        return "Satisfactory", "lightgreen"
    elif aqi <= 200:
        return "Moderate", "yellow"
    elif aqi <= 300:
        return "Poor", "orange"
    elif aqi <= 400:
        return "Very Poor", "red"
    else:
        return "Severe", "darkred"

# ---------------------------
# SIMULATED SENSOR DATA
# ---------------------------

def generate_sensor_data():
    pm25 = random.randint(80, 260)
    humidity = random.randint(40, 85)
    return pm25, humidity

nodes = {}

for i in range(1, 5):
    pm25, humidity = generate_sensor_data()
    aqi = calculate_aqi_pm25(pm25)
    category, color = get_aqi_category(aqi)
    nodes[f"Node {i}"] = {
        "PM2.5": pm25,
        "Humidity": humidity,
        "AQI": aqi,
        "Category": category,
        "Color": color
    }

# ---------------------------
# DASHBOARD
# ---------------------------

st.header("📡 Real-Time Sensor Dashboard")

cols = st.columns(4)

for i, (node, data) in enumerate(nodes.items()):
    with cols[i]:
        st.metric(node, f"AQI: {data['AQI']}")
        st.write(f"PM2.5: {data['PM2.5']} µg/m³")
        st.write(f"Humidity: {data['Humidity']} %")
        st.write(f"Category: {data['Category']}")

# ---------------------------
# 24-HOUR PREDICTION (Mock)
# ---------------------------

st.header("📈 24-Hour AQI Prediction")

hours = pd.date_range(datetime.datetime.now(), periods=24, freq="H")
predicted_values = np.clip(
    np.random.normal(loc=200, scale=40, size=24), 80, 350
)

df_pred = pd.DataFrame({
    "Time": hours,
    "Predicted AQI": predicted_values
})

fig = px.line(df_pred, x="Time", y="Predicted AQI",
              title="Next 24 Hours AQI Forecast",
              markers=True)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# SPRINKLER CONTROL LOGIC
# ---------------------------

st.header("💧 Smart Sprinkler Control Panel")

avg_aqi = np.mean([data["AQI"] for data in nodes.values()])
avg_humidity = np.mean([data["Humidity"] for data in nodes.values()])

st.write(f"Average Colony AQI: {round(avg_aqi)}")
st.write(f"Average Humidity: {round(avg_humidity)}%")

threshold = 200

activation_reason = ""
activate = False

if avg_aqi > threshold and avg_humidity < 80:
    activate = True
    activation_reason = "AQI above threshold and humidity safe."
elif avg_humidity >= 80:
    activation_reason = "High humidity — sprinkler disabled."
else:
    activation_reason = "AQI below activation threshold."

st.subheader("🤖 Auto Activation Status")

if activate:
    st.error("🚨 Sprinkler ACTIVATED")
else:
    st.success("✅ Sprinkler NOT Activated")

st.write("Reason:", activation_reason)

# Manual Override
st.subheader("🔘 Manual Override")

manual = st.checkbox("Force Activate Sprinkler")

if manual:
    st.warning("Manual Activation Enabled")

# Water Usage Simulation
st.subheader("💦 Water Usage")

recommended_duration = 15  # minutes
water_per_minute = 10  # liters
total_water = recommended_duration * water_per_minute

st.write(f"Recommended Duration: {recommended_duration} minutes")
st.write(f"Estimated Water Usage: {total_water} liters")

# Trigger History Log
st.subheader("📜 Trigger History Log")

log_data = pd.DataFrame({
    "Timestamp": [datetime.datetime.now()],
    "AQI Before": [round(avg_aqi)],
    "Sprinkler Activated": [activate or manual]
})

st.dataframe(log_data)
