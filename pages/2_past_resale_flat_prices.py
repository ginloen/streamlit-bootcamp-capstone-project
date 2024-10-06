import streamlit as st
import pandas as pd
import requests
from io import StringIO

from utility import check_password

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()

# Function to call the API and get the download link
def get_download_link():
    url = "https://api-open.data.gov.sg/v1/public/api/datasets/d_8b84c4ee58e3cfc0ece0d773c8ca6abc/initiate-download"
    response = requests.get(url)
    data = response.json()
    
    if data['code'] == 0:
        return data['data']['url']
    else:
        st.error("Error fetching download link.")
        return None

# Function to download and read the CSV file
def download_and_read_csv(download_url):
    response = requests.get(download_url)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        st.error("Error downloading the CSV file.")
        return None

# Streamlit app layout
st.set_page_config(
    page_title="Past Resale Flat Prices",
    page_icon="🏠",
    layout="wide"  
)
st.title("Resale flat prices based on registration date from Jan-2017 onwards")

# Check if the dataframe is already stored in session state
if 'dataframe' not in st.session_state:
    st.session_state.dataframe = None

if st.button("Fetch Data"):
    download_url = get_download_link()
    
    if download_url:
        st.session_state.dataframe = download_and_read_csv(download_url)

# Display the dataframe if it exists in session state
if st.session_state.dataframe is not None:
    df = st.session_state.dataframe
    
    # Sidebar filters with session state for persistence
    st.sidebar.header("Filter Options")
    
    # Initialize session state for filters if not already done
    if 'filters' not in st.session_state:
        st.session_state.filters = {
            'month': '',
            'town': '',
            'flat_type': '',
            'block': '',
            'street_name': '',
            'storey_range': '',
            'floor_area': 0,
            'flat_model': '',
            'lease_commence_date': '',
            'remaining_lease': '',
            'resale_price': 0,
        }

    # Filter inputs using session state
    month = st.sidebar.text_input("Month (YYYY-MM)", value=st.session_state.filters['month'])
    town = st.sidebar.text_input("Town (Text)", value=st.session_state.filters['town'])
    flat_type = st.sidebar.text_input("Flat type (Text)", value=st.session_state.filters['flat_type'])
    block = st.sidebar.text_input("Block (Text)", value=st.session_state.filters['block'])
    street_name = st.sidebar.text_input("Street name (Text)", value=st.session_state.filters['street_name'])
    storey_range = st.sidebar.text_input("Storey range (Text)", value=st.session_state.filters['storey_range'])
    floor_area = st.sidebar.number_input("Floor area sqm (Numeric)", min_value=0, value=st.session_state.filters['floor_area'])
    flat_model = st.sidebar.text_input("Flat model (Text)", value=st.session_state.filters['flat_model'])
    lease_commence_date = st.sidebar.text_input("Lease commence date (YYYY)", value=st.session_state.filters['lease_commence_date'])
    remaining_lease = st.sidebar.text_input("Remaining lease (Text)", value=st.session_state.filters['remaining_lease'])
    resale_price = st.sidebar.number_input("Resale price (Numeric)", min_value=0, value=st.session_state.filters['resale_price'])

    # Button to clear filters
    if st.sidebar.button("Clear Filters"):
        for key in st.session_state.filters.keys():
            if isinstance(st.session_state.filters[key], str):
                st.session_state.filters[key] = ''  # Reset string filters to empty
            else:
                st.session_state.filters[key] = 0  # Reset numeric filters to 0
            
        # Update sidebar inputs to reflect cleared filters
        month, town, flat_type, block, street_name, storey_range, floor_area, flat_model, lease_commence_date, remaining_lease, resale_price = (
            '', '', '', '', '', '', 0, '', '', '', 0)

        # Reinitialize filter inputs to reflect changes in session state
        month = ''
        town = ''
        flat_type = ''
        block = ''
        street_name = ''
        storey_range = ''
        floor_area = 0
        flat_model = ''
        lease_commence_date = ''
        remaining_lease = ''
        resale_price = 0

    # Apply filters to the dataframe based on user input
    filtered_df = df.copy()
    
    if month:
        filtered_df = filtered_df[filtered_df['month'].str.contains(month, na=False)]
    if town:
        filtered_df = filtered_df[filtered_df['town'].str.contains(town, case=False, na=False)]
    if flat_type:
        filtered_df = filtered_df[filtered_df['flat_type'].str.contains(flat_type, case=False, na=False)]
    if block:
        filtered_df = filtered_df[filtered_df['block'].str.contains(block)]
    if street_name:
        filtered_df = filtered_df[filtered_df['street_name'].str.contains(street_name, case=False, na=False)]
    if storey_range:
        filtered_df = filtered_df[filtered_df['storey_range'].str.contains(storey_range, na=False)]
    if floor_area > 0:
        filtered_df = filtered_df[filtered_df['floor_area_sqm'] >= floor_area]
    if flat_model:
        filtered_df = filtered_df[filtered_df['flat_model'].str.contains(flat_model, case=False, na=False)]
    if lease_commence_date:
        filtered_df = filtered_df[filtered_df['lease_commence_date'].astype(str).str.contains(lease_commence_date)]
    if remaining_lease:
        filtered_df = filtered_df[filtered_df['remaining_lease'].astype(str).str.contains(remaining_lease)]
    if resale_price > 0:
        filtered_df = filtered_df[filtered_df['resale_price'] >= resale_price]

    # Display the DataFrame with filters applied
    st.dataframe(filtered_df, use_container_width=True)