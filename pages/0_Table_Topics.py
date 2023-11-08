from typing import Any

import numpy as np

import streamlit as st
from streamlit.hello.utils import show_code
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import re

st.set_page_config(page_title="Table Topics", page_icon="📹")
st.markdown("# Table Topics")
st.sidebar.header("Table Topics")

conn = st.experimental_connection("gsheets", type=GSheetsConnection)
df = conn.read()
df = df[df['Speech Type'] == 'Table Topics']
df = df.drop('Speech Type',axis=1)
# df['View'] 
# st.write(df)

def dataframe_with_selections(df):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
    )
    selected_indices = list(np.where(edited_df.Select)[0])
    selected_rows = df[edited_df.Select]
    return selected_rows[['Link','Name','Speech Title']]
    return {"selected_rows_indices": selected_indices, "selected_rows": selected_rows}


selection = dataframe_with_selections(df)
st.write(selection)
# st.write()
pattern = r'(?<=t=)\d+s'

for index, row in selection.iterrows():
    match = re.search(pattern, row['Link'])
    time_duration = match.group(0)
    st.header(f"{row['Name']} - {row['Speech Title']}")
    st.write(row['Link'])
    st.video(row['Link'],start_time=int(time_duration[:-1]))
