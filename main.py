import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Store data in session state
if "data_store" not in st.session_state:
    st.session_state.data_store = {}

st.title("Live Data Bar Chart")

# Endpoint to receive data via Streamlit API
def receive_data():
    st.subheader("Received Data")
    st.write(st.session_state.data_store)

# Streamlit UI to display chart
def show_chart():
    if not st.session_state.data_store:
        st.warning("No data available")
        return
    
    df = pd.DataFrame(list(st.session_state.data_store.items()), columns=["Category", "Value"])
    fig = px.bar(df, x="Category", y="Value", title="Live Data Bar Chart")
    st.plotly_chart(fig, use_container_width=True)

# Create a simple API endpoint in Streamlit
st.write("Send data using the local script.")

# Show live chart
show_chart()

# Expose API-like functionality
st.sidebar.header("Data Receiver")
new_data = st.sidebar.text_area("Paste JSON data here and submit manually:")

if st.sidebar.button("Submit Data"):
    try:
        json_data = json.loads(new_data)
        st.session_state.data_store[json_data["category"]] = json_data["value"]
        st.sidebar.success("Data added successfully!")
    except Exception as e:
        st.sidebar.error(f"Invalid JSON format: {e}")

receive_data()
