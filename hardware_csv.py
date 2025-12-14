# hardware_app.py
import streamlit as st
import pandas as pd

st.title("Hardware Info")
try:
    df = pd.read_csv("hardware_info.csv")
    st.dataframe(df)
    st.bar_chart(df.set_index("test_session_id")[["cpu_percent", "memory_used_mb"]])
except Exception as e:
    st.warning("Keine Hardware-Daten gefunden: " + str(e))
