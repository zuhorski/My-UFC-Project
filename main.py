import streamlit as st

st.title("UFC Project")
login, signup = st.tabs(['Login', 'Signup'])
with login:
    with st.form(key='LoginForm'):
        uname1 = st.text_input('Username', key='User')
        pword1 = st.text_input('Password', key='Password')
        dataTuple = (uname1, pword1)
        submitted = st.form_submit_button('Submit')


with signup:
    c = st.container()
    uname = c.text_input('Username')
    pword = c.text_input('Password')
    dataTuple = (uname, pword)


if dataTuple[0] != '' and dataTuple[1] != '':
    st.write(dataTuple)