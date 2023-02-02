import streamlit as st
import leafmap.foliumap as leafmap


st.set_page_config(page_title="Streamlit Geospatial", layout="wide")
st.header("Demo App for Wind Visualizations")
st.subheader("Showcasing potential wind farm locations")

filepath = "wtk_site_metadata.csv"
USbounds = [-124.848974, 24.396308,-66.885444, 49.384358]

m = leafmap.Map()
m.add_heatmap(
    filepath,
    latitude="latitude",
    longitude='longitude',
    value="wind_speed",
    name="Heat map",
    radius=20
)
m.zoom_to_bounds(USbounds)
m.to_streamlit(height=700)
