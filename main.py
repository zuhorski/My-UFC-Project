import streamlit as st
import psycopg2
import pandas as pd

st.title("UFC Project")


@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])


conn = init_connection()


@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


df = pd.DataFrame(run_query('Select * from fightstats;'),
                  columns=[
                    'Event',
                    'Bout',
                    'Weightclass',
                    'TitleFight',
                    'Round',
                    'Fighter',
                    'KD',
                    'SIG_STR_LAND',
                    'SIG_STR_ATT',
                    'TOTAL_STR_LAND',
                    'TOTAL_STR_ATT',
                    'TD',
                    'TD_ATT',
                    'SUB_ATT',
                    'REVERSAL',
                    'CTRL_TIME_SEC',
                    'HEAD_LAND',
                    'HEAD_ATT',
                    'BODY_LAND',
                    'BODY_ATT',
                    'LEG_LAND',
                    'LEG_ATT',
                    'STAND_STR_LAND',
                    'STAND_STR_ATT',
                    'CLINCH_STR_LAND',
                    'CLINCH_STR_ATT',
                    'GROUND_STR_LAND',
                    'GROUND_STR_ATT',
                    'WINNER',
                    'WIN_BY',
                    'LAST_ROUND',
                    'ROUND_TIME_SEC',
                    'FORMAT',
                    'URL'])

st.dataframe(df)


# login, signup = st.tabs(['Login', 'Signup'])
# with login:
#     with st.form(key='LoginForm'):
#         uname1 = st.text_input('Username', key='User')
#         pword1 = st.text_input('Password', key='Password')
#         dataTuple = (uname1, pword1)
#         submitted = st.form_submit_button('Submit')
#
#
# with signup:
#     c = st.container()
#     uname = c.text_input('Username')
#     pword = c.text_input('Password')
#     dataTuple = (uname, pword)

# if dataTuple[0] != '' and dataTuple[1] != '':
#     st.write(dataTuple)