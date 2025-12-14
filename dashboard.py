# benchmark_overview.py
import streamlit as st
import pandas as pd

st.title("Benchmark Overview")
try:
    df = pd.read_csv("benchmark_overview.csv")
    st.dataframe(df)
    st.metric("Anzahl Requests", len(df))
    st.line_chart(df.set_index("request_id")["duration_ms"])
except Exception as e:
    st.warning("Keine Benchmark-Daten gefunden: " + str(e))
