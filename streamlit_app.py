import streamlit as st
import leafmap.foliumap as leafmap


st.set_page_config(page_title="Streamlit Geospatial", layout="wide")
st.header("Demo App for Wind Visualizations")
st.text("Quick demo that utilizes wind data from https://data.nrel.gov/submissions/54 and leafmap")

filepath = "wtk_site_metadata.csv"
USbounds = [-124.848974, 24.396308,-66.885444, 49.384358]

st.header("Wind Speed")
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

st.header("Capacity Factor")
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
