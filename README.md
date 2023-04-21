# View the project at [greenindex.streamlit.app](https://greenindex.streamlit.app/)

# Description 

The app provides an interactive map showing solar and wind resource potential, historical data on the total power generated from renewable sources (including solar, wind, hydroelectric and geothermal power), as well as information on incentives specific to each state. The app uses an exponential smoothing algorithm with additive trend and damping factor, but without seasonality to forecast percent of RES utilization by 2050. 

[Instructional video on how to run and use the app](https://youtu.be/jH-BRXnBOWs)
# Installation - To run locally: 
1. Clone Github Repo
`git clone https://github.com/darrenmcewan/Green_index`
2. Install the dependencies by running:
`pip3 install -r requirements.txt`
3. Run the Streamlit app by running:
`streamlit run Home.py`
4. Open your web browser and go to the following URL:
http://localhost:8501

You should see the Streamlit app running in your web browser.

# Execution

## ♻️ Renewable Resources
### Folium Leafmap 
1. View all existing renewable energy locations for the US or filter by state and energy type
2. Add a heatmap to showcase solar and wind potential energy


### State Renewable Energy Charts
1. State by state data on existing power produced from renewable energy vs state potential energy from solar and wind
2. Chart showing the current state % of total power from renewables with forecast of future energy. If a state has set a goal, it will be shown

## 📈 State Incentives
View a list of available incentives for a specific state in order to adopt renewable resources

## 📄 Project Proposal
Download our project research paper and view our report video
