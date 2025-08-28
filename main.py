import streamlit as st 
import os
import sys



registration = st.Page("./pages/registration.py", title="Registration", icon=":material/login:")
home_page = st.Page("./pages/homepage.py", title="Home", icon=":material/house:")
chat_q_bot = st.Page("./pages/chatqbot.py", title="ChatQbot", icon=":material/chat:")
# chat = st.Page("./pages/chatbot.py", title="ChatBot", icon=":material/picture_as_pdf:")




pg = st.navigation([registration, home_page, chat_q_bot])

st.set_page_config(
    page_title="ResQBot",
    page_icon="☣️🚨",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.echominds.africa',
        'Report a bug': "https://www.echominds.africa",
        'About': "# We are a leading insights and predicting big data application, Try *ResQBot* and experience reality!"
    }
)

with st.sidebar:
    st.markdown('📖 For more similar projects visit [click me](https://www.echominds.africa)!')
    
pg.run()