View [here](https://darrenmcewan-wind-visualization-streamlit-app-web2hk.streamlit.app/)

# Streamlit Geospatial

This is a demo app that uses wind data from the National Renewable Energy Laboratory (NREL) to visualize wind energy. It was created using Folium and Streamlit, and uses the streamlit-folium package to integrate Folium maps with Streamlit.

## How to Use

1. Download the required data by clicking the "Download wind csv here 💨" button. The data is stored in a file named "wtk_site_metadata.csv".

2.  Select the country (only "USA" is currently supported), state, and energy type using the dropdown menus.

3. The map will display a colored circle at each location where wind data is available. The color indicates the wind power density (W/m²) at that location.

4. Click on a circle to display a popup with additional information about that location, including latitude, longitude, elevation, and the wind power density.

5. Use the toolbar on the top right of the map to zoom, pan, and toggle the display of different layers.

6. Use the drawing tools on the left side of the map to draw shapes, markers, and lines.

## Code Explanation

- The code uses the folium package to create the interactive map and add the data points. The streamlit-folium package is used to integrate the Folium map with Streamlit.

- The data is loaded from the "wtk_site_metadata.csv" file using the pandas package. The dropdown menus for country, state, and energy type are created using the streamlit package.

- The folium.plugins.Draw class is used to add drawing tools to the map.

- The map is displayed using the st_folium function from the streamlit-folium package.
