import streamlit as st
from explore_page import show_explore_page
from predict_page import show_predict_page
from analysis_page import show_analysis_page

# Hide streamlit mark
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

page = st.sidebar.selectbox(
    "Predict / Explore / Analysis", ("Predict", "Explore", "Analysis"))

if page == "Predict":
    show_predict_page()
elif page == "Explore":
    show_explore_page()
elif page == "Analysis":
    show_analysis_page()
