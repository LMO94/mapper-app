import pandas as pd

import streamlit as st

sales_channels = ["Manor", "Galaxus", "WooCommerce"]



sheet_url = st.sidebar.text_input("Please paste Google Sheet link with config dict")

url_1 = sheet_url.replace("/edit?usp=sharing", "/export?format=csv")
config_df = pd.read_csv(url_1, index_col=0).fillna("")


st.sidebar.header("Inputs")
option = st.sidebar.multiselect("Which sales channel do you want to configure?", sales_channels)



req = config_df.loc[config_df["buyogo_req"] == True]["internal"]

galaxus_req = config_df.loc[config_df["galaxus_req"] == True]["internal"]

manor_req = config_df.loc[config_df["manor_req"] == True]["internal"]

st.title("Welcome to the Buyogo Product Integrator Mapper")


uploaded_file = st.sidebar.file_uploader("Choose a XLSX or CSV file")
if uploaded_file is not None:
    dataframe = pd.read_excel(uploaded_file)
    available_columns = list(dataframe.columns)

    #st.write(dataframe)
    
    st.header("Buyogo Mapping")
    with st.form("standard_form"):
        for i in req:
            st.selectbox(f"Plaese map your column to {i}", available_columns)
    # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
    
    if "Galaxus" in option:    
        st.header("Galaxus Mapping")
        with st.form("galaxus_form"):
            for i in galaxus_req:
                st.selectbox(f"Plaese map your column to {i}", available_columns)
        # Every form must have a submit button.
            submitted = st.form_submit_button("Submit") 
            
    if "Manor" in option:    
        st.header("Manor Mapping")
        with st.form("manor_form"):
            for i in manor_req:
                st.selectbox(f"{i}", available_columns)
        # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
    
    if "WooCommerce" in option:    
        st.header("WooCommerce Mapping")
        with st.form("woocommerce_form"):
            for i in manor_req:
                st.selectbox(f"{i}", available_columns)
        # Every form must have a submit button.
            submitted = st.form_submit_button("Submit") 
    st.balloons()

