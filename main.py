import streamlit as st
import streamlit_authenticator as auth

st.title("UFC Project")
c = st.container()
uname = c.text_input('Username')
pword = c.text_input('Password')
