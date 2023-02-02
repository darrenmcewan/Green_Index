import streamlit as st
import leafmap

st.header("Demo App for Wind Visualizations")
st.subheader("Showcasing potential wind farm locations")

m = leafmap.Map(minimap_control=True)
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)
