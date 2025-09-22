import streamlit as st
import pandas as pd
import altair as alt

# Titel
st.title("FastAPI Benchmark Ergebnisse")

# CSV laden
data = pd.read_csv("benchmark_results.csv")

# Daten anzeigen
st.write("Rohdaten:")
st.dataframe(data)

# Balkendiagramm erstellen
chart = alt.Chart(data).mark_bar().encode(
    x='requests:N',          # X-Achse = Anzahl Requests
    y='duration_ms:Q',       # Y-Achse = Dauer in ms
    color='server:N',        # Farbe nach Server
    tooltip=['server', 'type', 'duration_ms']
)

st.altair_chart(chart, use_container_width=True)
