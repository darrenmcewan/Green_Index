import streamlit as st
import leafmap.foliumap as leafmap

st.header("Demo App for Wind Visualizations")
st.subheader("Showcasing potential wind farm locations")

m = leafmap.Map(locate_control=True)
m.add_basemap("ROADMAP")
m.to_streamlit(height=700)


filepath = "wtk_site_metadata.csv"

m = leafmap.Map()
m.add_basemap("Stamen.Toner")
m.add_heatmap(
    filepath,
    latitude="latitude",
    longitude='longitude',
    value="wind_speed",
    name="Heat map",
    radius=20,
)
m.to_streamlit(height=700)
