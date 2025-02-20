import streamlit as st
import pandas as pd
import plotly.express as px
import threading
from flask import Flask, request, jsonify
import requests

# Storage for incoming data
if "data_store" not in st.session_state:
    st.session_state.data_store = {}

# Flask API to receive data
app = Flask(__name__)

@app.route("/send_data", methods=["POST"])
def receive_data():
    data = request.json  # Get JSON payload
    if "category" in data and "value" in data:
        st.session_state.data_store[data["category"]] = data["value"]
        return jsonify({"message": "Data received", "data": st.session_state.data_store}), 200
    return jsonify({"error": "Invalid data format"}), 400

# Run Flask API in a separate thread
def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

thread = threading.Thread(target=run_flask, daemon=True)
thread.start()

# Streamlit UI
st.title("Live Data Bar Chart")

st.write("Send data using a local script via `http://your-deployed-app-url/send_data`")

# Display data in a bar chart
def show_chart():
    if not st.session_state.data_store:
        st.warning("No data available")
        return
    
    df = pd.DataFrame(list(st.session_state.data_store.items()), columns=["Category", "Value"])
    fig = px.bar(df, x="Category", y="Value", title="Live Data Bar Chart")
    st.plotly_chart(fig, use_container_width=True)

show_chart()