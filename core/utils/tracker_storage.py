import json
import streamlit as st

# Save tracker data to downloadable .json file
def save_tracker_button(tracker_data):
    json_string = json.dumps(tracker_data, indent=2)
    st.download_button(
        label="Download Tracker",
        data=json_string,
        file_name="joblight_tracker.json",
        mime="application/json"
    )

# Load tracker data from uploaded .json file
def load_tracker_upload():
    uploaded_file = st.file_uploader("Upload Tracker (.json)", type="json")
    if uploaded_file:
        try:
            tracker_data = json.load(uploaded_file)
            st.success("Tracker loaded.")
            return tracker_data
        except Exception as e:
            st.error(f"Error loading tracker: {e}")
    return None
