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

# # Tab  style
# font_css = """
# <style>
# button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
#   font-size: 24px;
# }
# </style>
# """
# st.title("Data Science Salary Prediction")

# st.write(font_css, unsafe_allow_html=True)
# whitespace = 28
# listTabs = ["Predict", "Explore", "Analysis"]
# tabs = st.tabs([s.center(whitespace, "\u2001") for s in listTabs])
# with tabs[0]:
#     show_predict_page()
# with tabs[1]:
#     show_explore_page()
# with tabs[2]:
#     show_explore_page()
