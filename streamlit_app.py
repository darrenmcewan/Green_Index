import folium
import pandas as pd
import streamlit as st
from folium.plugins import Draw
from streamlit_folium import st_folium
import numpy as np
#
st.set_page_config(page_title="Streamlit Geospatial", layout="wide")
original_title = '<h1 style=color:green>The Green Solution</h1>'
st.markdown(original_title, unsafe_allow_html=True)
col1,col2,col3,col4,col5 = st.columns(5)
with col1:
    st.write("Wind")
    st.image("images/wind.JPG")
with col2:
    st.write("Hydro")
    st.image("images/hydro.JPG")
with col3:
    st.write("Solar")
    st.image("images/solar.JPG")
with col4:
    st.write("Biomass")
    st.image("images/biomass.JPG")
with col5:
    st.write("Geothermal")
    st.image("images/geothermal.JPG")

st.write(
    "👈 View the sidebar for help on getting started\n\n\n\n")



countries = ['USA']
states = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
          'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
          'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
          'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
          'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
energytype = ['Biomass', 'Geothermal', 'Hydropower', 'Solor', 'Wind']


col1, col2, col3 = st.columns([1,3,2])
with col1:
    energy_type = st.selectbox("Energy Type", energytype, help="Select an energy type you would like displayed")
with col2:
    m = folium.Map(
        location=[40.580585,-95.779294],
        zoom_start=4,
        control_scale=True,
        attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
    )
    Draw(
        export=False,
        position="topleft",
        draw_options={
            "polyline": False,
            "poly": False,
            "circle": False,
            "polygon": True,
            "marker": False,
            "circlemarker": False,
            "rectangle": False,
        },
    ).add_to(m)
    folium.TileLayer('stamenterrain').add_to(m)


    output = st_folium(m, key="init", width=1000, height=600)
    if output:
        if output["all_drawings"] is not None:
            coords = output['all_drawings'][0]['geometry']['coordinates'][0]
            for i in coords:
                st.write(i)
with col3:

    chart_data = pd.DataFrame(
        {'Resource Type': ["Solar", "Wind", "Hydro", "Biomas","Geothermal"], 'kw/year': np.random.randint(130,size=5)})
    st.write("Average Annual Power Production")
    st.bar_chart(chart_data, x='Resource Type', y='kw/year')

    chart_data = pd.DataFrame(
        {'Resource Type': ["Solar", "Wind", "Hydro", "Biomas", "Geothermal"], 'LCOE': np.random.randint(130, size=5)})
    st.write("Levelized Cost of Energy (lifetime cost/lifetime output")
    st.bar_chart(chart_data, x='Resource Type', y='LCOE')


with st.sidebar.container():
    st.markdown(
        f"""
        # Getting Started 
        1. Click the black polygon on the map
        2. Select the desired locations to analyze various renewable energy options
        3. Optional: Apply customizations
        """,
        unsafe_allow_html=True,
    )
    st.selectbox("Country", countries, help="Only the United States is currently supported")
    state = st.selectbox("States", states, help="Select a state to zoom in on")

col1,col2,col3,col4 = st.columns(4)
with col1:
    st.markdown("## Best Resource")
    st.markdown("- Solar")

with col2:
    st.markdown("## Best Investment")
    st.markdown("- Wind")

with col3:
    st.markdown(f"## Incentives for solar in {state}:")


with col4:
    st.markdown(f"## Incentives for solar in {state}:")


#https://stackoverflow.com/questions/69409255/how-to-get-city-state-and-country-from-a-list-of-latitude-and-longitude-coordi#