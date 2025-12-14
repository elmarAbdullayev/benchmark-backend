# stats_app.py
import streamlit as st
import pandas as pd

st.title("Stats (Min / Avg / Max)")
try:
    df = pd.read_csv("statistiken_results.csv")
    st.dataframe(df)
    st.line_chart(df.set_index("test_session_id")[["avg_response_time", "min_response_time", "max_response_time"]])
except Exception as e:
    st.warning("Keine Statistiken gefunden: " + str(e))
