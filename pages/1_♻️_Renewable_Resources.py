import altair as alt
import folium
import leafmap.foliumap as foliumap
import pandas as pd
import streamlit as st
import geopandas as gpd
from PIL import Image
from folium.plugins import Draw
from streamlit_folium import st_folium
from collections import defaultdict
import branca.colormap as cm
from branca.element import Figure
from folium.plugins import HeatMap
from folium import Choropleth


import scripts.state_incentives
from scripts.eddies_functions import *
from scripts.existing_resources import *


st.markdown("""
            <style>
            .css-15zrgzn {display: none}
            .css-eczf16 {display: none}
            .css-jn99sy {display: none}
            </style>
            """, unsafe_allow_html=True)

st.set_page_config(page_title="Streamlit Geospatial", layout="wide")
# DATA
resources = ['Hydroelectric', 'Solar', 'Wind']

@st.cache_data
def getData():
    data = pd.read_csv('data/Power_Plants.csv')
    # Import df of state renewable energy goals (% from renewable sources)
    state_goals = pd.read_csv('data/state_renewable_goals_2021.csv')
    # Import df of solar & wind potential
    sw_data = pd.read_csv('data/project_data_3.csv')
    sw_data['solar_sum'] = sw_data[['util_pv_te', 'resid_pv_t', 'com_pv_tec']].astype(float).sum(1)
    # load in county geoJSON
    geojson = gpd.read_file('data/county_reduced.geojson')
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
state_sw_potential = sw_data[['state_name','solar_sum', 'dist_wind_']]
state_sw_potential = state_sw_potential.groupby('state_name', as_index  = False).sum()
# divide by 1000 to change units from MWh to GWh
state_sw_potential['solar_sum'] = state_sw_potential['solar_sum']/1000.0
state_sw_potential['dist_wind_'] = state_sw_potential['dist_wind_']/1000.0
# rename columns to add units
state_sw_potential.rename(columns = {'solar_sum': 'solar_sum (GWh)', 'dist_wind_': 'dist_wind_ (GWh)'}, inplace = True)
# swap states keys and values so that full names in state_sw_potential can be abreviated.
states_abrv_dict = dict((v,k) for k,v in states.items()) 
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
    energy_type = st.selectbox("Renewable Energy Type", ['All']+energytype,
                               help="Select an energy type you would like displayed")



## MAP


options = st.selectbox(
    'View current renewable energy locations and/or heatmap of totla MW in the US',
    ['Renewable Energy Locations', 'Heatmap of Solar Generation Potential MWh', 'Heatmap of Wind Generation Potential MWh'])


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

        if state != 'AK':
            m.zoom_to_bounds(statesBounding[state])

        folium.TileLayer('openstreetmap').add_to(m)
        if "Heatmap of Solar Generation Potential MWh" in options:
            folium.Choropleth(
                geo_data=geojson,
                data=sw_data,
                columns=['fips', 'solar_sum'],
                key_on = 'feature.properties.cnty_code2',
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


            if state == 'AK':
                data = data[data["PrimSource"].isin(['Wind', 'Solar','Hydroelectric'])]
                color = "#76c893"
            else:
                data = data[(data["StateName"] == states[state]) & data["PrimSource"].isin(['Wind', 'Solar','Hydroelectric'])]
                colors = {"Wind": "#8d99ae", "Solar": "#ffd166", "Hydroelectric": "#118ab2"}

            locations = data[["Latitude", "Longitude", "Utility_Name", "PrimSource"]].values.tolist()
            if energy_type == 'All':

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


    #output = st_folium(m, key="init", width=600, height=600)


labels = ['Wind', 'Solar', 'Hydroelectric']
colors = ['#8d99ae', '#ffd166', '#118ab2']


#col1, col2 = st.columns(2)
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
with col2:
    ########################## Start example code for matplot lib ###########################################################
    # From:  https://blog.streamlit.io/make-your-st-pyplot-interactive/
    # Imports for all of the code
    import matplotlib.pyplot as plt
    import mpld3
    import numpy as np
    from mpld3 import plugins
    import streamlit.components.v1 as components
    if energy_type != 'All':
    
        # Redefine dataframes to be plotted each time a new state is selected
        future_years = list(range(2020, 2051))
        hgf_df = pd.DataFrame({
            'year': future_years,
            'Predicted Renewable Generation': renewable_forecast(state, historical_gen, solar_gen, wind_gen, hydro_gen, geothermal_gen)})
        sp_df = pd.DataFrame({
            'Solar Potential': list(state_sw_potential['solar_sum (GWh)'][state_sw_potential['state_name'] == state])*len(list(range(1960, 2051))),
            'year': list(range(1960, 2051))})
        wp_df = pd.DataFrame({
            'Wind Potential': list(state_sw_potential['dist_wind_ (GWh)'][state_sw_potential['state_name'] == state])*len(list(range(1960, 2051))),
            'year': list(range(1960, 2051))})
        pred_percent_df = pd.DataFrame({
            'year': future_years,
            'Predicted Percent Power From Renewables': 100.0 * renewable_fraction_forecast(state, renewable_energy_fraction, coal_gen, oil_gen, nat_gas_gen,
                                                                    wood_and_waste_gen, nuclear_gen, biomass_for_biofuels_gen,
                                                                    renewable_forecast(state, historical_gen, solar_gen, wind_gen, hydro_gen, geothermal_gen))})
        state_goals_df = get_renewable_goals(state, state_goals)

        two_subplot_fig = plt.figure(figsize=(6,8))
        two_subplot_fig.tight_layout()
        # two_subplot_fig.add_axes([0.1, 0.1, 0.6, 0.75])

        plt.subplot(211)
        plt.subplots_adjust(hspace=0.5)
        plt.plot(historical_gen['year'], historical_gen[state], color='tab:green', label="From Renewables")
        plt.plot(hgf_df['year'], hgf_df['Predicted Renewable Generation'], color='tab:green', linestyle='dashed', label="Forecast")
        plt.plot(sp_df['year'], sp_df['Solar Potential'], color='tab:orange', linestyle='dashed', label="Solar Potential")
        plt.plot(wp_df['year'], wp_df['Wind Potential'], color='tab:blue', linestyle='dashed', label="Wind Potential")
        # plt.plot(t2, f(t2), color='black', marker='.')
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        plt.title(state + " Power Produced From Renewables")
        plt.xlabel("Year")
        plt.xlim([1960, 2050])
        plt.ylabel("GWh")
        plt.yscale('log')
        plt.grid(axis = 'y')

        plt.subplot(212)
        plt.subplots_adjust(hspace=0.5)
        #plt.plot(t2, np.cos(2*np.pi*t2), color='tab:orange', linestyle='--', marker='.')
        plt.ylim(0, 100) # fix y axis range from 0 to 100 %
        plt.plot(renewable_energy_fraction['year'], renewable_energy_fraction[state], color='#054907', label="Historical Data")
        plt.plot(pred_percent_df['year'], pred_percent_df['Predicted Percent Power From Renewables'], color='#054907', linestyle='dashed', label="Forecast")
        plt.plot(state_goals_df['year'], state_goals_df['goal'], '*', color='tab:red', markersize=11, label="State Goal")
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        plt.title(state + " % Of Total Power From Renewables")
        plt.xlabel("Year")
        plt.xlim([1960, 2050])
        plt.ylabel("%")
        plt.grid(axis = 'y')

        st.pyplot(two_subplot_fig)
    # # Define some CSS to control our custom labels
    # css = '''
    # table
    # {
    # border-collapse: collapse;
    # }
    # th
    # {
    # color: #ffffff;
    # background-color: #000000;
    # }
    # td
    # {
    # background-color: #cccccc;
    # }
    # table, th, td
    # {
    # font-family:Arial, Helvetica, sans-serif;
    # border: 1px solid black;
    # text-align: right;
    # }
    # '''

    # for axes in two_subplot_fig.axes:
    #     for line in axes.get_lines():
    #         xy_data = line.get_xydata()
    #         labels = []
    #         for x,y in xy_data:
    #             html_label = f'<table border="1" class="dataframe"> <thead> <tr style="text-align: right;"> </thead> <tbody> <tr> <th>x</th> <td>{x}</td> </tr> <tr> <th>y</th> <td>{y}</td> </tr> </tbody> </table>'
    #             labels.append(html_label)
    #         tooltip = plugins.PointHTMLTooltip(line, labels, css=css)
    #         plugins.connect(two_subplot_fig, tooltip)

    # fig_html = mpld3.fig_to_html(two_subplot_fig)
    # components.html(fig_html, height=300, width=1500) # need to figure out how to resize the figure.

    ########################## End example code for matplot lib #############################################################
#     historical_gen_chart = (
#         alt.Chart(
#             data=historical_gen,
#             title=state + " Power Produced From Renewables ",
#         )
#         .mark_line()
#         .encode(
#             # x=alt.X("capacity 1", axis=alt.Axis(title="Capacity 1")),
#             # x=alt.X("capacity 2", axis=alt.Axis(title="Capacity 2")),
#             x=alt.X('year', title='year'),
#             y=alt.Y(state, title='GWh'),
#             # color = alt.Color('blue')
#         )
#         # .mark_rule(color='red').encode(y=alt.datum(1))
#         # .mark_rule(color='red').encode(y=alt.datum(state_potential_dict[state]['solar_potential']))
#     )

#     # make new data frame for predicted renewable generation from 2020 to 2050
#     future_years = list(range(2020, 2051))
#     hgf_df = pd.DataFrame({
#         'year': future_years,
#         # 'Predicted Renewable Generation': smooth2(future_years, historical_gen[state]) })
#         'Predicted Renewable Generation': renewable_forecast(state, historical_gen, solar_gen, wind_gen, hydro_gen, geothermal_gen)})

#     hgf_chart = (  # historical generation fit chart
#         alt.Chart(hgf_df).mark_line(color='blue', strokeDash=[2, 6], size=2).encode(
#             x='year',
#             y='Predicted Renewable Generation',
#         )
#     )

#     sp_df = pd.DataFrame({
#         'Solar Potential': [state_potential_dict[state]['solar_potential']] * len(list(range(1960, 2051))),
#         'year': list(range(1960, 2051))})

#     #  solar_potential_line = alt.Chart(sp_df).mark_line(color= 'red').encode(
#     solar_potential_line = alt.Chart(sp_df).mark_line(color='red', strokeDash=[12, 6], size=2).encode(
#         x='year',
#         y='Solar Potential',
#         # color = alt.Color('red')
#         # .mark_text(text='doubles every 2 days', angle=0)
#     )

#     # # This needs to correspond to a df with only 1 coordinate, not sp_df
#     # solar_potential_text = alt.Chart(sp_df).mark_text(text= state + ' Maximum Solar Potential', color = 'red', angle=0).encode(
#     # x= 'year',
#     # y= 'Solar Potential',
#     # #color = alt.Color('red')
#     # # .mark_text(text='doubles every 2 days', angle=0)
#     # )

#     wp_df = pd.DataFrame({
#         'Wind Potential': [state_potential_dict[state]['wind_potential']] * len(list(range(1960, 2051))),
#         'year': list(range(1960, 2051))})

#     wind_potential_line = alt.Chart(wp_df).mark_line(color='green', strokeDash=[12, 6], size=2).encode(
#         x='year',
#         y='Wind Potential',
#     )
#     st.altair_chart(historical_gen_chart + hgf_chart + solar_potential_line + wind_potential_line, use_container_width=True)

#     # st.altair_chart(historical_gen_chart + hgf_chart + solar_potential_line + solar_potential_text + wind_potential_line)

#     # Now try to make a second chart here:

#     # chart_data = pd.DataFrame(
#     #     {'Resource Type': ["Solar", "Wind", "Hydro"], 'LCOE': np.random.randint(130, size=3)})
#     # st.write("Levelized Cost of Energy (lifetime cost/lifetime output")
#     # st.bar_chart(chart_data, x='Resource Type', y='LCOE')
# #with col2:
#     renewable_fraction_chart = (
#         alt.Chart(
#             data=renewable_energy_fraction,
#             title=state + " % Power Produced From Renewables",
#         )
#         .mark_line()
#         .encode(
#             x=alt.X('year', title='year'),
#             y=alt.Y(state, title=' % Power Produced From Renewables', scale=alt.Scale(domain=[0, 100])),
#             # y = alt.Y('count()', scale=alt.Scale(domain=[0, 120]),
#             # color = alt.Color('blue')
#         )
#         # .mark_rule(color='red').encode(y=alt.datum(1))
#         # .mark_rule(color='red').encode(y=alt.datum(state_potential_dict[state]['solar_potential']))
#     )
#     # make new data frame for predicted renewable generation from 2020 to 2050
#     pred_percent_df = pd.DataFrame({
#         'year': future_years,
#         # 'Predicted Percent Power From Renewables': smooth2(future_years, renewable_energy_fraction[state]) })
#          # multiply by 100.0 to go from fraction to %
#         'Predicted Percent Power From Renewables': 100.0 * renewable_fraction_forecast(state, renewable_energy_fraction, coal_gen, oil_gen, nat_gas_gen,
#                                                                 wood_and_waste_gen, nuclear_gen, biomass_for_biofuels_gen,
#                                                                 renewable_forecast(state, historical_gen, solar_gen, wind_gen, hydro_gen, geothermal_gen))})

#     pred_percent_chart = (  # historical generation fit chart
#         alt.Chart(pred_percent_df).mark_line(clip=True, color='blue', strokeDash=[2, 6], size=2).encode(
#             x='year',
#             y='Predicted Percent Power From Renewables',
#         )
#     )
#     state_goals_chart = (  # put state % renewable goals on the same chart.

#         alt.Chart(get_renewable_goals(state, state_goals)).mark_point(shape='circle', color='green', size=25).encode(
#             x='year',
#             y='goal'
#         )
#     )

    # st.altair_chart(renewable_fraction_chart + pred_percent_chart + state_goals_chart, use_container_width=True)

    # st.markdown(get_goal_details(state, state_goals))


