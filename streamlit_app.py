import streamlit as st
import leafmap.foliumap as leafmap


st.set_page_config(page_title="Streamlit Geospatial", layout="wide")
st.header("Demo App for Wind Visualizations")
st.subheader("Showcasing potential wind farm locations")

filepath = "wtk_site_metadata.csv"
maxBounds = [
    [5.499550, -167.276413], 
    [83.162102, -52.233040] 
];

m = leafmap.Map()
m.add_heatmap(
    filepath,
    latitude="latitude",
    longitude='longitude',
    value="wind_speed",
    name="Heat map",
    radius=20,
    maxBounds=maxBounds
)
m.to_streamlit(height=700)
