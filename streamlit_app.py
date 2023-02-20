import folium
import pandas as pd
import streamlit as st
from folium.plugins import Draw
from streamlit_folium import st_folium
import numpy as np

st.set_page_config(page_title="Streamlit Geospatial", layout="wide")
original_title = '<h1 style=display:inline;>The </h1> <h1 style="font-family:Courier; color:Green;display:inline;">Green</h1> <h1 style=display:inline;> Solution</h1>'
st.markdown(original_title, unsafe_allow_html=True)

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
        location=[36.87962060502676, -460.01953125000006],
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
    folium.TileLayer('cartodbpositron').add_to(m)

    output = st_folium(m, key="init", width=1000, height=600)
    if output:
        if output["all_drawings"] is not None:
            for i in output['all_drawings'][0]['geometry']['coordinates'][0]:
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
col1.metric(label="Best resource", value="Solar")
col1.metric(label="Best Investment", value="Wind")
col1.metric(label=f"Incentives for solar in:", value=f"{state}")
col1.metric(label=f"Restrictions for solor in:", value=f"{state}")


