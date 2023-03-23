# Renewable Energy Production Forecast

This Python script includes four functions to predict future renewable energy production and the percentage of energy generated from renewables up to the year 2050 for a specific state in the USA.

## Functions

1. smooth2(x_future, y_data, alpha, beta)

- This function uses double exponential smoothing to forecast time-series data for a given alpha and beta value. The function takes the following parameters:

    - x_future: A list of future years for which to make predictions.
    - y_data: A pandas series containing the historical data to fit and predict.
    - alpha: A smoothing parameter for the level component.
    - beta: A smoothing parameter for the trend component.

- The function returns a pandas series of predicted values for the future years.

2. renewable_forecast(state, solar_gen, wind_gen, hydro_gen, geothermal_gen)

- This function uses the smooth2() function to predict future renewable energy production for a specific state in the USA. The function takes the following parameters:

    - state: A string specifying the state for which to make predictions.
    - solar_gen: A dictionary containing the historical solar energy generation data for each state.
    - wind_gen: A dictionary containing the historical wind energy generation data for each state.
    - hydro_gen: A dictionary containing the historical hydro energy generation data for each state.
    - geothermal_gen: A dictionary containing the historical geothermal energy generation data for each state.

- The function returns a pandas series of predicted values for the total renewable energy production for the future years.

3. renewable_fraction_forecast(state, historical_total, r_forecast_df)

- This function uses the smooth2() function to predict the percentage of energy generated from renewables for a specific state in the USA. The function takes the following parameters:

    - state: A string specifying the state for which to make predictions.
    - historical_total: A pandas dataframe containing the historical total energy generation data for each state.
    - r_forecast_df: A pandas series of predicted values for the total renewable energy production for the future years.

- The function returns a pandas series of predicted values for the percentage of energy generated from renewables for the future years.

4. get_renewable_goals(state, state_goals)

- This function returns a pandas dataframe containing the renewable energy goals for a specific state. The function takes the following parameters:

    - state: A string specifying the state for which to get the renewable energy goals.
    - state_goals: A pandas dataframe containing the renewable energy goals for all states in the USA.

- If the specified state has renewable energy goals, the function returns a pandas dataframe containing the year and goal columns. Otherwise, it returns an empty dataframe.

5. get_goal_details(state, state_goals)

- This function returns a string containing the details of the renewable energy goals for a specific state. The function takes the following parameters:

    - state: A string specifying the state for which to get the renewable energy goal details.
    - state_goals: A pandas dataframe containing the renewable energy goals for all states in the USA.

- If the specified state has renewable energy goals, the function returns a string containing the details. Otherwise, it returns an empty string.

## Usage

To use these functions, import the script into your Python environment and call the functions with the appropriate parameters.

Note: Before using these functions, you must have the necessary data available in the correct format.
