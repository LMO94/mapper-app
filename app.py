from re import M
import pandas as pd

import streamlit as st

sales_channels = ["Manor", "Galaxus", "WooCommerce"]

        
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


sheet_url = st.sidebar.text_input("Please paste Google Sheet link with config dict")

url_1 = sheet_url.replace("/edit#gid=0", "/export?format=csv")
config_df = pd.read_csv(url_1, index_col=0).fillna("")


st.sidebar.header("Inputs")
option = st.sidebar.multiselect("Which sales channel do you want to configure?", sales_channels)



req = list(config_df.loc[config_df["buyogo_req"] == True]["internal"])

galaxus_req = list(config_df.loc[config_df["galaxus_req"] == True]["internal"])

manor_req = list(config_df.loc[config_df["manor_req"] == True]["internal"])

woocommerce_req = list(config_df.loc[config_df["woocommerce_req"] == True]["internal"])

st.title("Welcome to the Buyogo Product Integrator Mapper")


uploaded_file = st.sidebar.file_uploader("Choose a XLSX or CSV file")
if uploaded_file is not None:
    dataframe = pd.read_excel(uploaded_file)
    available_columns = list(dataframe.columns)

    #st.write(dataframe)
    
    if sorted(option) == ["Galaxus", "Manor", "WooCommerce"]:
        full_req = req + galaxus_req + manor_req + woocommerce_req
        
    if sorted(option) == ["Galaxus", "WooCommerce"]:
        full_req = req + galaxus_req + woocommerce_req
        
    if sorted(option) == ["Galaxus", "Manor"]:
        full_req = req + galaxus_req + manor_req

    if sorted(option) == ["Manor", "WooCommerce"]:
        full_req = req + manor_req + woocommerce_req
        
    if sorted(option) == ["Galaxus"]:
        full_req = req + galaxus_req
        
    if sorted(option) == ["Manor"]:
        full_req = req + manor_req

    if sorted(option) == ["WooCommerce"]:
        full_req = req + woocommerce_req


    mapping_dict = {}
    
    full_req =  list(dict.fromkeys(full_req))
       
    st.header("Full Mapping")
    with st.form("standard_form"):
        for i in full_req:
            key = i
            value = st.selectbox(f"{i}", available_columns)
            mapping_dict[key] = value
    # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
    
    
    
    
    
    # st.header("Buyogo Mapping")
    # with st.form("standard_form"):
    #     for i in req:
    #         key = i
    #         value = st.selectbox(f"{i}", available_columns)
    #         buyogo_dict[key] = value
    # # Every form must have a submit button.
    #     submitted = st.form_submit_button("Submit")
    
    # if "Galaxus" in option:    
    #     st.header("Galaxus Mapping")
    #     with st.form("galaxus_form"):
    #         for i in galaxus_req:
    #             st.selectbox(f"{i}", available_columns)
    #     # Every form must have a submit button.
    #         submitted = st.form_submit_button("Submit") 
            
    # if "Manor" in option:    
    #     st.header("Manor Mapping")
    #     with st.form("manor_form"):
    #         for i in manor_req:
    #             st.selectbox(f"{i}", available_columns)
    #     # Every form must have a submit button.
    #         submitted = st.form_submit_button("Submit")
    
    # if "WooCommerce" in option:    
    #     st.header("WooCommerce Mapping")
    #     with st.form("woocommerce_form"):
    #         for i in manor_req:
    #             st.selectbox(f"{i}", available_columns)
    #     # Every form must have a submit button.
    #         submitted = st.form_submit_button("Submit") 
    while submitted == True:
        st.balloons()
        
        
        mapped_df = pd.DataFrame.from_dict(mapping_dict, orient='index')
        
        st.dataframe(mapped_df)

        st.download_button(label="Download data as CSV",
            data=convert_df(mapped_df),
            file_name='large_df.csv',
            key="data_download")
        break