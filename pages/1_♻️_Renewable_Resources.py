import altair as alt
import folium
import leafmap.foliumap as foliumap
import pandas as pd
import streamlit as st
from PIL import Image
from folium.plugins import Draw
from streamlit_folium import st_folium
from collections import defaultdict
import branca.colormap as cm
from branca.element import Figure
from folium.plugins import HeatMap

import scripts.state_incentives
from scripts.eddies_functions import *
from scripts.existing_resources import *

st.set_page_config(page_title="Streamlit Geospatial", layout="wide")
# DATA
data = pd.read_csv('data/Power_Plants.csv')
resources = ['Hydroelectric', 'Solar', 'Wind']
data = data[data['PrimSource'].isin(resources)]

# Import df of state renewable energy goals (% from renewable sources)
state_goals = pd.read_csv('data/state_renewable_goals_2021.csv')
# Import df of solar & wind potential
sw_data = pd.read_csv('data/solar_wind_poten.csv')

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

# Construct a dictionary of calculated wind and solar potential for each state:
state_potential_dict = {}
for my_state in states.keys():  # Make dictionary of wind and solar potential values for each state. In the final version these will be calculated in a function from geodata.
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

    st.selectbox("Country", countries, help="Only the United States is currently supported")
    state = st.selectbox("Find Renewable Energy Near You", states, help="Select a state to zoom in on", index=0)
    energy_type = st.selectbox("Renewable Energy Type", energytype,
                               help="Select an energy type you would like displayed")


## MAP


options = st.multiselect(
    'View current renewable energy locations and/or heatmap of totla MW in the US',
    ['Renewable Energy Locations', 'Heatmap of Solar Generation Potential MWh', 'Heatmap of Wind Generation Potential MWh'],
    ['Renewable Energy Locations'])

col1, col2,col3 = st.columns([1,2,1])
with col2:
    m = foliumap.Map(
        location=[40.580585, -95.779294],
        zoom_start=4,
        control_scale=False,
        tiles=None,
        attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="https://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
    )

    if state != 'AK':
        m.zoom_to_bounds(statesBounding[state])

    folium.TileLayer('openstreetmap').add_to(m)
    folium.TileLayer('cartodbpositron').add_to(m)
    lat_long_list_solar = list(map(list, zip(sw_data['latitude'], sw_data['longitude'], sw_data['util_pv_te'])))
    lat_long_list_wind = list(map(list, zip(sw_data['latitude'], sw_data['longitude'], sw_data['dist_wind_'])))
    if "Heatmap of Solar Generation Potential MWh" in options:
        HeatMap(lat_long_list_solar).add_to(m)

    if "Heatmap of Wind Generation Potential MWh" in options:
        HeatMap(lat_long_list_wind).add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)


    if "Renewable Energy Locations" in options:
        #df = pd.read_csv('data/Power_Plants.csv')
        #df = df[(df["StateName"] == states[state]) & (df["PrimSource"] == energy_type)]
        #if not df.empty:
        #    locations = df[["latitude", "longitude"]].values.tolist()
        #    colors = {"Wind": "#8d99ae", "Solar": "#ffd166", "Water": "#118ab2"}
        #    color = colors[energy_type]

        #    for location in locations:
        #        folium.CircleMarker(location, radius=8, color=color, fill_color=color).add_to(m)

        if state == 'AK':
            for coord in wind:
                folium.CircleMarker([coord[0], coord[1]], radius=4, color='#8d99ae', fill_color="#8d99ae").add_to(m)
            for coord in solar:
                folium.CircleMarker([coord[0], coord[1]], radius=4, color='#ffd166', fill_color="#ffd166").add_to(m)
            for coord in water:
                folium.CircleMarker([coord[0], coord[1]], radius=4, color='#118ab2', fill_color="#118ab2").add_to(m)

        else:
            if energy_type in state_dict[states[state]]:
                for coord in state_dict[states[state]][energy_type]:
                    if energy_type == "Wind":
                        folium.CircleMarker([coord[0], coord[1]], radius=8, color='#8d99ae',
                                            fill_color="#8d99ae").add_to(m)
                    elif energy_type == "Solar":
                        folium.CircleMarker([coord[0], coord[1]], radius=8, color='#ffd166',
                                            fill_color="#ffd166").add_to(m)
                    else:
                        folium.CircleMarker([coord[0], coord[1]], radius=8, color='#118ab2',
                                            fill_color="#118ab2").add_to(m)

    output = st_folium(m, key="init", width=1000, height=600)



labels = ['Wind', 'Solar', 'Hydroelectric']
colors = ['#8d99ae', '#ffd166', '#118ab2']


col1, col2,col3 = st.columns([2,1,2])
# chart_data = pd.DataFrame(
#     {'Resource Type': ["Solar", "Wind", "Hydro"],
#      'pistachio': [10,50,78],
#      'kw/year': np.random.randint(130, size=3)})
# st.write(state + " Power Production From Renewables")
# st.line_chart(historical_gen, x = 'year', y = state)
# st.write(state)
# st.write(state_potential_dict[state])
# Make altair chart that is more customizable then default line_chart
# append columns to historical_gen
# define color scale:
# scale = alt.Scale(domain=['historical_gen', 'solar_potential', 'wind_potential'], range=['blue', 'red', 'green'])
with col1:
    historical_gen_chart = (
        alt.Chart(
            data=historical_gen,
            title=state + " Power Produced From Renewables ",
        )
        .mark_line()
        .encode(
            # x=alt.X("capacity 1", axis=alt.Axis(title="Capacity 1")),
            # x=alt.X("capacity 2", axis=alt.Axis(title="Capacity 2")),
            x=alt.X('year', title='year'),
            y=alt.Y(state, title='GWh'),
            # color = alt.Color('blue')
        )
        # .mark_rule(color='red').encode(y=alt.datum(1))
        # .mark_rule(color='red').encode(y=alt.datum(state_potential_dict[state]['solar_potential']))
    )

    # make new data frame for predicted renewable generation from 2020 to 2050
    future_years = list(range(2020, 2051))
    hgf_df = pd.DataFrame({
        'year': future_years,
        # 'Predicted Renewable Generation': smooth2(future_years, historical_gen[state]) })
        'Predicted Renewable Generation': renewable_forecast(state, historical_gen, solar_gen, wind_gen, hydro_gen, geothermal_gen)})

    hgf_chart = (  # historical generation fit chart
        alt.Chart(hgf_df).mark_line(color='blue', strokeDash=[2, 6], size=2).encode(
            x='year',
            y='Predicted Renewable Generation',
        )
    )

    sp_df = pd.DataFrame({
        'Solar Potential': [state_potential_dict[state]['solar_potential']] * len(list(range(1960, 2051))),
        'year': list(range(1960, 2051))})

    #  solar_potential_line = alt.Chart(sp_df).mark_line(color= 'red').encode(
    solar_potential_line = alt.Chart(sp_df).mark_line(color='red', strokeDash=[12, 6], size=2).encode(
        x='year',
        y='Solar Potential',
        # color = alt.Color('red')
        # .mark_text(text='doubles every 2 days', angle=0)
    )

    # # This needs to correspond to a df with only 1 coordinate, not sp_df
    # solar_potential_text = alt.Chart(sp_df).mark_text(text= state + ' Maximum Solar Potential', color = 'red', angle=0).encode(
    # x= 'year',
    # y= 'Solar Potential',
    # #color = alt.Color('red')
    # # .mark_text(text='doubles every 2 days', angle=0)
    # )

    wp_df = pd.DataFrame({
        'Wind Potential': [state_potential_dict[state]['wind_potential']] * len(list(range(1960, 2051))),
        'year': list(range(1960, 2051))})

    wind_potential_line = alt.Chart(wp_df).mark_line(color='green', strokeDash=[12, 6], size=2).encode(
        x='year',
        y='Wind Potential',
    )
    st.altair_chart(historical_gen_chart + hgf_chart + solar_potential_line + wind_potential_line, use_container_width=True)

    # st.altair_chart(historical_gen_chart + hgf_chart + solar_potential_line + solar_potential_text + wind_potential_line)

    # Now try to make a second chart here:

    # chart_data = pd.DataFrame(
    #     {'Resource Type': ["Solar", "Wind", "Hydro"], 'LCOE': np.random.randint(130, size=3)})
    # st.write("Levelized Cost of Energy (lifetime cost/lifetime output")
    # st.bar_chart(chart_data, x='Resource Type', y='LCOE')
with col3:
    renewable_fraction_chart = (
        alt.Chart(
            data=renewable_energy_fraction,
            title=state + " % Power Produced From Renewables",
        )
        .mark_line()
        .encode(
            x=alt.X('year', title='year'),
            y=alt.Y(state, title=' % Power Produced From Renewables', scale=alt.Scale(domain=[0, 100])),
            # y = alt.Y('count()', scale=alt.Scale(domain=[0, 120]),
            # color = alt.Color('blue')
        )
        # .mark_rule(color='red').encode(y=alt.datum(1))
        # .mark_rule(color='red').encode(y=alt.datum(state_potential_dict[state]['solar_potential']))
    )
    # make new data frame for predicted renewable generation from 2020 to 2050
    pred_percent_df = pd.DataFrame({
        'year': future_years,
        # 'Predicted Percent Power From Renewables': smooth2(future_years, renewable_energy_fraction[state]) })
         # multiply by 100.0 to go from fraction to %
        'Predicted Percent Power From Renewables': 100.0 * renewable_fraction_forecast(state, renewable_energy_fraction, coal_gen, oil_gen, nat_gas_gen,
                                                                wood_and_waste_gen, nuclear_gen, biomass_for_biofuels_gen,
                                                                renewable_forecast(state, historical_gen, solar_gen, wind_gen, hydro_gen, geothermal_gen))})

    pred_percent_chart = (  # historical generation fit chart
        alt.Chart(pred_percent_df).mark_line(clip=True, color='blue', strokeDash=[2, 6], size=2).encode(
            x='year',
            y='Predicted Percent Power From Renewables',
        )
    )
    state_goals_chart = (  # put state % renewable goals on the same chart.

        alt.Chart(get_renewable_goals(state, state_goals)).mark_point(shape='circle', color='green', size=25).encode(
            x='year',
            y='goal'
        )
    )

    st.altair_chart(renewable_fraction_chart + pred_percent_chart + state_goals_chart, use_container_width=True)

    st.markdown(get_goal_details(state, state_goals))

col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown(f"## Incentives for renewable energy in {state}:")
    incentives = scripts.state_incentives.show_resources(state)
    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.write(incentives, unsafe_allow_html=True)

# https://stackoverflow.com/questions/69409255/how-to-get-city-state-and-country-from-a-list-of-latitude-and-longitude-coordi#
