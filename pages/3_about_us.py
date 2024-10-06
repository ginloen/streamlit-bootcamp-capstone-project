import streamlit as st

from utility import check_password

st.set_page_config(
    page_title="About Us",
    page_icon="🏠"
)

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()

st.title("About Us")

st.header("Project Scope:")
st.subheader("Domain Area: Buying HDB flat in the resale market")
st.markdown('''
    The goal of this application is to assist buyers in navigating the complex process of purchasing a resale flat. It provides a step-by-step guide, perform simple eligibility checks and past resale flat prices to facilitate an informed decision-making process.
''')
st.header("Objectives:")
st.subheader("Use cases:")
st.markdown('''
    1. Help buyers determine their eligibility for purchasing a resale flat and understand the associated process.
    2. Providing the most recent resale data.
''')
st.header("Data Sources:")
st.markdown('''
    HDB Website: https://www.hdb.gov.sg/cs/infoweb/homepage  
    Data.gov.sg: https://data.gov.sg/
''')
st.header("Features:")
st.markdown('''
    1. Virtual assistant Clara
        - Provides a quick way to nagivate information on eligibility and process of purchasing a resale flat.
    2. Latest resale prices from 2017
        - Allow buyers to visual the resale market movements to make a more informed decision.
''')