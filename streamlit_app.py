import streamlit as st
import leafmap.foliumap as leafmap

st.header("Demo App for Wind Visualizations")
st.subheader("Showcasing potential wind farm locations")

m = leafmap.Map(locate_control=True)
m.add_basemap("ROADMAP")
m.to_streamlit(height=700)
