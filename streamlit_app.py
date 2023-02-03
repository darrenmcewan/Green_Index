import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd


st.set_page_config(page_title="Streamlit Geospatial", layout="wide")
st.header("Demo App for Wind Visualizations")
st.write("Quick demo that utilizes wind data from [The National Renewable Energy Laboratory (NREL)](https://data.nrel.gov/submissions/) and leafmap to visualize")

filepath = "wtk_site_metadata.csv"
USbounds = [-124.848974, 24.396308,-66.885444, 49.384358]

df = pd.read_csv(filepath, sep=",", header=True)

windspeed_df = df.filter(items=['latitude','longitude','wind_speed'])
capacity_factor_df = df.filter(items=['latitude','longitude','capacity_factor'])
st.header("Wind Speed")
col1, col2 = st.columns(2)
with col1:
    m = leafmap.Map()
    m.add_heatmap(
        filepath,
        latitude="latitude",
        longitude='longitude',
        value="wind_speed",
        name="Wind Speed",
        radius=20
    )
    m.zoom_to_bounds(USbounds)
    m.to_streamlit(height=700)
with col2:
    st.dataframe(windspeed_df)

st.header("Capacity Factor")

col1, col2 = st.columns(2)
with col1:
    m = leafmap.Map()
    m.add_heatmap(
        filepath,
        latitude="latitude",
        longitude='longitude',
        value="capacity_factor",
        name="Capacity Factor",
        radius=20
    )
    m.zoom_to_bounds(USbounds)
    m.to_streamlit(height=700)
with col2:
    st.dataframe(capacity_factor_df)