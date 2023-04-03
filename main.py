import streamlit as st
import psycopg2
import pandas as pd
import numpy as np


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


# filter the dataframe based on user input
def filter_df(dataframe, search_text):
    return dataframe[dataframe.apply(lambda x: search_text.lower() in ' '.join(x.astype(str)).lower(), axis=1)]


def cosine_similarity(x, y):
    numerator = np.dot(x, y)
    denominator = np.linalg.norm(x) * np.linalg.norm(y)
    return numerator / denominator


# Load data from database into a pandas dataframe
df = pd.DataFrame(run_query('Select * from bouts order by date desc;'), columns=["Event", "Bout", "Date", "URL"])
df = df.iloc[:, 0:3]

# Allow user to select multiple bouts
selected_bouts = st.multiselect('Select Bouts', df[['Bout', 'Event', 'Date']].drop_duplicates().apply(
    lambda x: ' -- '.join(x.astype(str)), axis=1).tolist())


data = [b.split(" -- ") for b in selected_bouts]
selected_bouts_df = (pd.DataFrame(data, columns=["Bout", "Event", "Date"]))
st.table(selected_bouts_df)

rec = st.number_input("Enter how many fights to be recommended", min_value=1, max_value=100, step=1, value=10)
if len(selected_bouts) != 0 and st.button('Submit selections'):
    events = selected_bouts_df["Event"].tolist()
    bouts = selected_bouts_df["Bout"].tolist()

    cols = ["Kd", "SigStrLand", "SigStrAtt",
            "TotalStrLand", "TotalStrAtt", "Td", "TdAtt", "SubAtt", "Reversal", "CtrlTimeSec",
            "HeadLand", "HeadAtt", "BodyLand", "BodyAtt", "LegLand", "LegAtt", "StandStrLand",
            "StandStrAtt", "ClinchStrLand", "ClinchStrAtt", "GroundStrLand", "GroundStrAtt", "FightTimeSec"]

    bt = pd.DataFrame(run_query('Select * from bouttotals;'),
                      columns=["Event", "Bout", "Weightclass", "Titlefight", "Kd", "SigStrLand", "SigStrAtt",
                               "TotalStrLand", "TotalStrAtt", "Td", "TdAtt", "SubAtt", "Reversal", "CtrlTimeSec",
                               "HeadLand", "HeadAtt", "BodyLand", "BodyAtt", "LegLand", "LegAtt", "StandStrLand",
                               "StandStrAtt", "ClinchStrLand", "ClinchStrAtt", "GroundStrLand", "GroundStrAtt",
                               "Winner", "WinBy", "LastRound", "FightTimeSec", "Format"])
    result = bt[(bt['Event'].isin(events)) & (bt['Bout'].isin(bouts))].reset_index(drop=True)

    # st.dataframe(result)

    st.write("Your Fights Selected")
    boutsSelectedDescriptiveStats = result.describe()
    # st.dataframe(boutsSelectedDescriptiveStats)

    numerical_columns = boutsSelectedDescriptiveStats.columns.tolist()
    for _ in range(3):
        numerical_columns.pop(22)
    result_per_min = result.copy()
    result_per_min["FightTimeSec"] = result_per_min["FightTimeSec"] / 60
    result_per_min[numerical_columns] = result_per_min[numerical_columns].div(result_per_min["FightTimeSec"], axis=0)
    st.dataframe(result_per_min.describe())

    # st.write("UFC Overall")
    # ufcBoutsDescriptiveStats = bt.describe()
    # st.dataframe(ufcBoutsDescriptiveStats)

    bt_per_min = bt.copy()
    bt_per_min["FightTimeSec"] = bt_per_min["FightTimeSec"] / 60
    bt_per_min[numerical_columns] = bt_per_min[numerical_columns].div(bt_per_min["FightTimeSec"], axis=0)
    bt_per_min.dropna(inplace=True)
    # st.dataframe(bt_per_min.head())
    # st.dataframe(bt_per_min.describe())

    st.write('Recommended Fights')
    # Calculate the cosine similarity between the row of interest in df1 and all rows in df2
    row1 = result_per_min[numerical_columns].mean()
    similarity_scores = np.apply_along_axis(lambda row2: cosine_similarity(row1, row2), axis=1, arr=bt_per_min[numerical_columns].values)

    # Sort the similarity scores in descending order and extract the top 10 most similar rows
    most_similar_indices = np.argsort(similarity_scores)[-rec:][::-1]
    most_similar_rows = bt_per_min.iloc[most_similar_indices, :]
    st.dataframe(most_similar_rows.reset_index(drop=True))
    # st.write(most_similar_rows.describe())


