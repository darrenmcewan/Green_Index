import folium
from folium import Choropleth
import geopandas as gpd
import leafmap.foliumap as foliumap
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from scripts.eddies_functions import *
from scripts.existing_resources import *



st.set_page_config(page_title="Streamlit Geospatial", layout="wide")
# DATA
resources = ['Hydroelectric', 'Solar', 'Wind']


@st.cache_data
def getData():
    data = pd.read_csv('data/Power_Plants.csv')
    # Import df of state renewable energy goals (% from renewable sources)
    state_goals = pd.read_csv('data/state_renewable_goals_2021.csv')
    # Import df of solar & wind potential
    sw_data = pd.read_csv('data/project_data_4.csv')
    sw_data['solar_sum'] = sw_data[['util_pv_te', 'resid_pv_t', 'com_pv_tec']].astype(float).sum(1)
    sw_data['fips'] = sw_data['fips'].astype(str)
    # load in county geoJSON
    geojson = gpd.read_file('data/county_reduced_3.geojson')
    # Import historical renewable energy data and make dataframes
    historical_gen_billion_Btu = pd.read_csv('data/historical_renewable_energy_production_by_state_in_billion_Btu.csv')
    # Imoport total energy production by state (including renewables and fossil fuels)
    historical_total_billion_Btu = pd.read_csv('data/historical_total_energy_production_by_state_in_billion_Btu.csv')
    # Import statewide solar power generation data (1989 - 2020) for forecasting
    solar_gen = pd.read_csv('data/solar_production.csv')
    # keep years column for conversion from billion Btu to GWh
    years_before_forecast = solar_gen['year']
    # Import statewide wind power generation data (1989 - 2020) for forecasting
    wind_gen = pd.read_csv('data/wind_production.csv')
    # Import statewide hydropower generation data (1989 - 2020) for forecasting
    hydro_gen = pd.read_csv('data/hydro_production.csv')
    # Import statewide geothermal power generation data (1989 - 2020) for forecasting
    geothermal_gen = pd.read_csv('data/geothermal_production.csv')
    # Import data for all other types of primary power generation data (1989 - 2020) for forecasting
    coal_gen = pd.read_csv('data/coal_production.csv')
    oil_gen = pd.read_csv('data/crude_oil_production.csv')
    nat_gas_gen = pd.read_csv('data/natural_gas_production.csv')
    wood_and_waste_gen = pd.read_csv('data/wood_and_waste_production.csv')
    nuclear_gen = pd.read_csv('data/nuclear_consumption.csv')
    biomass_for_biofuels_gen = pd.read_csv('data/biomass_for_biofuels.csv')

    return data, state_goals, sw_data, geojson, historical_gen_billion_Btu, historical_total_billion_Btu, solar_gen, years_before_forecast, wind_gen, hydro_gen, geothermal_gen, coal_gen, oil_gen, nat_gas_gen, wood_and_waste_gen, nuclear_gen, biomass_for_biofuels_gen


data, state_goals, sw_data, geojson, historical_gen_billion_Btu, historical_total_billion_Btu, solar_gen, years_before_forecast, wind_gen, hydro_gen, geothermal_gen, coal_gen, oil_gen, nat_gas_gen, wood_and_waste_gen, nuclear_gen, biomass_for_biofuels_gen = getData()

# convert all columns (except year) from billion Btu to GWh
historical_gen = historical_gen_billion_Btu.drop('year', axis=1) * (1.0 / 3.412)
historical_total = historical_total_billion_Btu.drop('year', axis=1) * (1.0 / 3.412)
solar_gen = solar_gen.drop('year', axis=1) * (1.0 / 3.412)
wind_gen = wind_gen.drop('year', axis=1) * (1.0 / 3.412)
hydro_gen = hydro_gen.drop('year', axis=1) * (1.0 / 3.412)
geothermal_gen = geothermal_gen.drop('year', axis=1) * (1.0 / 3.412)
coal_gen = coal_gen.drop('year', axis=1) * (1.0 / 3.412)
oil_gen = oil_gen.drop('year', axis=1) * (1.0 / 3.412)
nat_gas_gen = nat_gas_gen.drop('year', axis=1) * (1.0 / 3.412)
wood_and_waste_gen = wood_and_waste_gen.drop('year', axis=1) * (1.0 / 3.412)
nuclear_gen = nuclear_gen.drop('year', axis=1) * (1.0 / 3.412)
biomass_for_biofuels_gen = biomass_for_biofuels_gen.drop('year', axis=1) * (1.0 / 3.412)

# Calclate fraction of energy generated by renewables and put it in a new dataframe.
renewable_energy_fraction = pd.DataFrame()  # new dataframe
for state_name in list(historical_gen):
    renewable_energy_fraction[state_name] = 100.0 * historical_gen[state_name] / historical_total[state_name]

# Add back the year column
historical_gen['year'] = historical_gen_billion_Btu['year']  # Now we can start plotting.
historical_total['year'] = historical_total_billion_Btu['year']
renewable_energy_fraction['year'] = historical_total_billion_Btu['year']
solar_gen['year'] = years_before_forecast
wind_gen['year'] = years_before_forecast
hydro_gen['year'] = years_before_forecast
geothermal_gen['year'] = years_before_forecast
coal_gen['year'] = years_before_forecast
oil_gen['year'] = years_before_forecast
nat_gas_gen['year'] = years_before_forecast
wood_and_waste_gen['year'] = years_before_forecast
nuclear_gen['year'] = years_before_forecast
biomass_for_biofuels_gen['year'] = years_before_forecast

original_title = '<h1 style=color:green>The Green Solution</h1>'
st.markdown(original_title, unsafe_allow_html=True)

st.markdown("""
            <style>
            .css-15zrgzn {display: none}
            .css-eczf16 {display: none}
            .css-jn99sy {display: none}
             button[title="View fullscreen"]{opacity: 1; transform: scale(1);}
            </style>
            """, unsafe_allow_html=True)

st.cache_data()


def state_data():
    with open('data/states.txt', 'r') as f:
        lines = f.readlines()

    states = {}
    statesBounding = {}
    for line in lines:
        state_data = line.strip().split(': ')
        abbr, name = state_data[0], state_data[1].split(':')[0]
        values = [float(x) for x in state_data[2][1:-1].split(', ')]
        states[abbr] = name
        statesBounding[abbr] = values

    return states, statesBounding


states, statesBounding = state_data()

# Construct a dictionary of calculated wind and solar potential for each state:
state_potential_dict = {}
for my_state in states.keys():  # Make dictionary of wind and solar potential values for each state. In the final version these will be calculated in a function from geodata.
    if my_state == 'All':
        continue

    state_potential_dict[my_state] = {'wind_potential': max(historical_gen[my_state]) * 2,
                                      'solar_potential': max(historical_gen[my_state]) * 3}

energytype = ['Wind', 'Solar', 'Hydroelectric']
state_groups = data.groupby(['StateName', 'PrimSource'])
state_dict = {}
for (state, res_type), group in state_groups:
    if state not in state_dict:
        state_dict[state] = {}
    state_dict[state][res_type] = group[['Latitude', 'Longitude']].values.tolist()
wind, water, solar = resource_locations(data)

# Make dataframe containing total solar and wind technical potential for each state.
state_sw_potential = sw_data[['state_name', 'solar_sum', 'dist_wind_']]
state_sw_potential = state_sw_potential.groupby('state_name', as_index=False).sum()
# divide by 1000 to change units from MWh to GWh
state_sw_potential['solar_sum'] = state_sw_potential['solar_sum'] / 1000.0
state_sw_potential['dist_wind_'] = state_sw_potential['dist_wind_'] / 1000.0
# rename columns to add units
state_sw_potential.rename(columns={'solar_sum': 'solar_sum (GWh)', 'dist_wind_': 'dist_wind_ (GWh)'}, inplace=True)
# swap states keys and values so that full names in state_sw_potential can be abreviated.
states_abrv_dict = dict((v, k) for k, v in states.items())
state_sw_potential['state_name'] = state_sw_potential['state_name'].map(states_abrv_dict)

with st.sidebar.container():
    st.markdown(
        f"""
        # Getting Started
        1. Click on the state you would like to see
        2. Select the desired renewable resource to place on the map
        3. Optional: add a heatmap to discover potential energy
        """,
        unsafe_allow_html=True,
    )

    state = st.selectbox("Find Renewable Energy Near You", states, help="Select a state to zoom in on", index=0)

    energy_type = st.selectbox("Renewable Energy Type", ['All'] + energytype,
                               help="Select an energy type you would like displayed")

## MAP


options = st.selectbox(
    'View current renewable energy locations and/or heatmap of total MW in the US',
    ['Renewable Energy Locations', 'Heatmap of Solar Generation Potential MWh',
     'Heatmap of Wind Generation Potential MWh'])

col1, col2 = st.columns(2)
with col1:
    with st.spinner('Visualization Loading'):

        m = foliumap.Map(
            location=[40.580585, -95.779294],
            zoom_start=3.3,
            control_scale=False,
            tiles=None,
            attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="https://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
        )

        if state != 'All':
            m.zoom_to_bounds(statesBounding[state])

        folium.TileLayer('openstreetmap').add_to(m)
        if "Heatmap of Solar Generation Potential MWh" in options:
            folium.Choropleth(
                geo_data=geojson,
                data=sw_data,
                columns=['fips', 'solar_sum'],
                key_on='feature.properties.cnty_code2',
                fill_color='YlOrRd',
                nan_fill_color="white",  # Use white color if there is no data available for the county
                fill_opacity=0.7,
                line_opacity=0.3,
                legend_name="Solar Potential").add_to(m)

        if "Heatmap of Wind Generation Potential MWh" in options:
            folium.Choropleth(
                geo_data=geojson,
                data=sw_data,
                columns=['fips', 'dist_wind_'],
                key_on='feature.properties.cnty_code2',
                fill_color='BuPu',
                nan_fill_color="white",  # Use white color if there is no data available for the county
                fill_opacity=0.7,
                line_opacity=0.3,
                legend_name="Wind Potential").add_to(m)
        folium.LayerControl(collapsed=False).add_to(m)

        if "Renewable Energy Locations" in options:

            if state == 'All':
                data = data[data["PrimSource"].isin(['Wind', 'Solar', 'Hydroelectric'])]
                color = "#76c893"
            else:
                data = data[
                    (data["StateName"] == states[state]) & data["PrimSource"].isin(['Wind', 'Solar', 'Hydroelectric'])]
                colors = {"Wind": "#8d99ae", "Solar": "#ffd166", "Hydroelectric": "#118ab2"}


            if energy_type == 'All':
                locations = data[["Latitude", "Longitude", "Utility_Name", "PrimSource"]].values.tolist()
                for location in locations:
                    if location[3] == "Solar":
                        icon = folium.features.CustomIcon('images/solar.png', icon_size=(20, 20))
                    elif location[3] == "Wind":
                        icon = folium.features.CustomIcon('images/wind.png', icon_size=(20, 20))
                    elif location[3] == "Hydroelectric":
                        icon = folium.features.CustomIcon('images/hydro.png', icon_size=(20, 20))
                    folium.Marker(location=[location[0], location[1]], tooltip=location[2], icon=icon).add_to(m)
            else:
                data = data[(data["StateName"] == states[state]) & (data["PrimSource"] == energy_type)]
                locations = data[["Latitude", "Longitude", "Utility_Name", "PrimSource"]].values.tolist()
                for location in locations:
                    if energy_type == "Solar":
                        icon = folium.features.CustomIcon('images/solar.png', icon_size=(20, 20))
                    elif energy_type == "Wind":
                        icon = folium.features.CustomIcon('images/wind.png', icon_size=(20, 20))
                    elif energy_type == "Hydroelectric":
                        icon = folium.features.CustomIcon('images/hydro.png', icon_size=(20, 20))
                    folium.Marker(location=[location[0], location[1]], tooltip=location[2], icon=icon).add_to(m)
        m.to_streamlit()
    st.success("Map Loaded")

labels = ['Wind', 'Solar', 'Hydroelectric']
colors = ['#8d99ae', '#ffd166', '#118ab2']

with col2:
    if state != 'All':
        # Redefine dataframes to be plotted each time a new state is selected
        future_years = list(range(2020, 2051))
        hgf_df = pd.DataFrame({
            'year': future_years,
            'Predicted Renewable Generation': renewable_forecast(state, historical_gen, solar_gen, wind_gen, hydro_gen,
                                                                 geothermal_gen)})
        sp_df = pd.DataFrame({
            'Solar Potential': list(
                state_sw_potential['solar_sum (GWh)'][state_sw_potential['state_name'] == state]) * len(
                list(range(1960, 2051))),
            'year': list(range(1960, 2051))})
        wp_df = pd.DataFrame({
            'Wind Potential': list(
                state_sw_potential['dist_wind_ (GWh)'][state_sw_potential['state_name'] == state]) * len(
                list(range(1960, 2051))),
            'year': list(range(1960, 2051))})
        pred_percent_df = pd.DataFrame({
            'year': future_years,
            'Predicted Percent Power From Renewables': 100.0 * renewable_fraction_forecast(state,
                                                                                           renewable_energy_fraction,
                                                                                           coal_gen, oil_gen,
                                                                                           nat_gas_gen,
                                                                                           wood_and_waste_gen,
                                                                                           nuclear_gen,
                                                                                           biomass_for_biofuels_gen,
                                                                                           renewable_forecast(state,
                                                                                                              historical_gen,
                                                                                                              solar_gen,
                                                                                                              wind_gen,
                                                                                                              hydro_gen,
                                                                                                              geothermal_gen))})
        state_goals_df = get_renewable_goals(state, state_goals)

        two_subplot_fig = plt.figure(figsize=(6, 8))
        two_subplot_fig.tight_layout()

        plt.subplot(211)
        plt.subplots_adjust(hspace=0.5)
        plt.plot(historical_gen['year'], historical_gen[state], color='tab:green', label="From Renewables")
        plt.plot(hgf_df['year'], hgf_df['Predicted Renewable Generation'], color='tab:green', linestyle='dashed',
                 label="Forecast")
        plt.plot(sp_df['year'], sp_df['Solar Potential'], color='tab:orange', linestyle='dashed',
                 label="Solar Potential")
        plt.plot(wp_df['year'], wp_df['Wind Potential'], color='tab:blue', linestyle='dashed', label="Wind Potential")
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        plt.title(state + " Power Produced From Renewables")
        plt.xlabel("Year")
        plt.xlim([1960, 2050])
        plt.ylabel("GWh")
        plt.yscale('log')
        plt.grid(axis='y')

        plt.subplot(212)
        plt.subplots_adjust(hspace=0.5)
        plt.ylim(0, 100)  # fix y axis range from 0 to 100 %
        plt.plot(renewable_energy_fraction['year'], renewable_energy_fraction[state], color='#054907',
                 label="Historical Data")
        plt.plot(pred_percent_df['year'], pred_percent_df['Predicted Percent Power From Renewables'], color='#054907',
                 linestyle='dashed', label="Forecast")
        plt.plot(state_goals_df['year'], state_goals_df['goal'], '*', color='tab:red', markersize=11,
                 label="State Goal")
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        plt.title(state + " % Of Total Power From Renewables")
        plt.xlabel("Year")
        plt.xlim([1960, 2050])
        plt.ylabel("%")
        plt.grid(axis='y')

        st.pyplot(two_subplot_fig)

        # Display info about state goals below chart
        st.markdown(get_goal_details(state, state_goals))
    else:
        helpful_message = 'Choose a state from the sidebar to view forecasted renewable energy potential'

        st.info(helpful_message, icon="ℹ")
