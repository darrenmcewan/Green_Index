import folium
import pandas as pd
import streamlit as st
from folium.plugins import Draw
from streamlit_folium import st_folium
import numpy as np
from PIL import Image
import leafmap.foliumap as foliumap

#
st.set_page_config(page_title="Streamlit Geospatial", layout="wide")
original_title = '<h1 style=color:green>The Green Solution</h1>'
st.markdown(original_title, unsafe_allow_html=True)
st.write(
    "👈 View the sidebar for help on getting started\n\n\n\n")
col1, col2, col3 = st.columns(3)
with col1:
    st.write("Wind")
    image = Image.open("images/wind.JPG")
    st.image(image)
with col2:
    st.write("Hydro")
    image = Image.open("images/hydro.JPG")
    st.image(image)
with col3:
    st.write("Solar")
    image = Image.open("images/solar.JPG")
    st.image(image)

countries = ['USA']
states = ['AK','AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
          'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
          'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
          'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
          'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
statesBounding = {'AL': [-88.473227, 30.223334, -84.88908, 35.008028],
                  'AK': [-179.148909, 51.214183, 179.77847, 71.365162],
                  'AZ': [-114.81651, 31.332177, -109.045223, 37.00426],
                  'AR': [-94.617919, 33.004106, -89.644395, 36.4996],
                  'CA': [-124.409591, 32.534156, -114.131211, 42.009518],
                  'CO': [-109.060253, 36.992426, -102.041524, 41.003444],
                  'CT': [-73.727775, 40.980144, -71.786994, 42.050587],
                  'DE': [-75.788658, 38.451013, -75.048939, 39.839007],
                  'FL': [-87.634938, 24.523096, -80.031362, 31.000888],
                  'GA': [-85.605165, 30.357851, -80.839729, 35.000659],
                  'HI': [-178.334698, 18.910361, -154.806773, 28.402123],
                  'ID': [-117.243027, 41.988057, -111.043564, 49.001146],
                  'IL': [-91.513079, 36.970298, -87.494756, 42.508481],
                  'IN': [-88.09776, 37.771742, -84.784579, 41.760592],
                  'IA': [-96.639704, 40.375501, -90.140061, 43.501196],
                  'KS': [-102.051744, 36.993016, -94.588413, 40.003162],
                  'KY': [-89.571509, 36.497129, -81.964971, 39.147458],
                  'LA': [-94.043147, 28.928609, -88.817017, 33.019457],
                  'ME': [-71.083924, 42.977764, -66.949895, 47.459686],
                  'MD': [-79.487651, 37.911717, -75.048939, 39.723043],
                  'MA': [-73.508142, 41.237964, -69.928393, 42.886589],
                  'MI': [-90.418136, 41.696118, -82.413474, 48.2388],
                  'MN': [-97.239209, 43.499356, -89.491739, 49.384358],
                  'MS': [-91.655009, 30.173943, -88.097888, 34.996052],
                  'MO': [-95.774704, 35.995683, -89.098843, 40.61364],
                  'MT': [-116.050003, 44.358221, -104.039138, 49.00139],
                  'NE': [-104.053514, 39.999998, -95.30829, 43.001708],
                  'NV': [-120.005746, 35.001857, -114.039648, 42.002207],
                  'NH': [-72.557247, 42.69699, -70.610621, 45.305476],
                  'NJ': [-75.559614, 38.928519, -73.893979, 41.357423],
                  'NM': [-109.050173, 31.332301, -103.001964, 37.000232],
                  'NY': [-79.762152, 40.496103, -71.856214, 45.01585],
                  'NC': [-84.321869, 33.842316, -75.460621, 36.588117],
                  'ND': [-104.0489, 45.935054, -96.554507, 49.000574],
                  'OH': [-84.820159, 38.403202, -80.518693, 41.977523],
                  'OK': [-103.002565, 33.615833, -94.430662, 37.002206],
                  'OR': [-124.566244, 41.991794, -116.463504, 46.292035],
                  'PA': [-80.519891, 39.7198, -74.689516, 42.26986],
                  'RI': [-71.862772, 41.146339, -71.12057, 42.018798],
                  'SC': [-83.35391, 32.0346, -78.54203, 35.215402],
                  'SD': [-104.057698, 42.479635, -96.436589, 45.94545],
                  'TN': [-90.310298, 34.982972, -81.6469, 36.678118],
                  'TX': [-106.645646, 25.837377, -93.508292, 36.500704],
                  'UT': [-114.052962, 36.997968, -109.041058, 42.001567],
                  'VT': [-73.43774, 42.726853, -71.464555, 45.016659],
                  'VA': [-83.675395, 36.540738, -75.242266, 39.466012],
                  'WA': [-124.763068, 45.543541, -116.915989, 49.002494],
                  'WV': [-82.644739, 37.201483, -77.719519, 40.638801],
                  'WI': [-92.888114, 42.491983, -86.805415, 47.080621],
                  'WY': [-111.056888, 40.994746, -104.05216, 45.005904]}
energytype = ['Wind', 'Solar', 'Hydropower', 'Biomass', 'Geothermal']

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
    state = st.selectbox("Find Renewable Energy Near You", states, help="Select a state to zoom in on", index=0)
    energy_type = st.selectbox("Renewable Energy Type", energytype,
                               help="Select an energy type you would like displayed")

col1, col2 = st.columns([3, 1])
with col1:
    m = foliumap.Map(
        location=[40.580585, -95.779294],
        zoom_start=4,
        control_scale=False,
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
    if state!='AK':
        m.zoom_to_bounds(statesBounding[state])
    folium.TileLayer('openstreetmap').add_to(m)

    output = st_folium(m, key="init", width=1000, height=600)
    if output:
        if output["all_drawings"] is not None:
            coords = output['all_drawings'][0]['geometry']['coordinates'][0]
            for i in coords:
                st.write(i)
with col2:
    chart_data = pd.DataFrame(
        {'Resource Type': ["Solar", "Wind", "Hydro", "Biomas", "Geothermal"],
         'kw/year': np.random.randint(130, size=5)})
    st.write("Average Annual Power Production")
    st.bar_chart(chart_data, x='Resource Type', y='kw/year')

    chart_data = pd.DataFrame(
        {'Resource Type': ["Solar", "Wind", "Hydro", "Biomas", "Geothermal"], 'LCOE': np.random.randint(130, size=5)})
    st.write("Levelized Cost of Energy (lifetime cost/lifetime output")
    st.bar_chart(chart_data, x='Resource Type', y='LCOE')



col1, col2, col3, col4 = st.columns(4)
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

# https://stackoverflow.com/questions/69409255/how-to-get-city-state-and-country-from-a-list-of-latitude-and-longitude-coordi#
