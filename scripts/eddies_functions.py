# Function that uses double exponential smoothing to predict renewable energy production and % energy from renewables up to the year 2050.
def smooth2(x_future, y_data, alpha, beta):  # takes "array-like" data let's try a panda's series.
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    # create model
    ex_smooth_model = ExponentialSmoothing(y_data, trend='additive')
    # fit model
    ex_fit = ex_smooth_model.fit(smoothing_level=alpha, smoothing_trend=beta)
    # make prediction
    yhat = ex_fit.predict(start=len(y_data), end=len(y_data) + len(x_future) - 1)  # predict y values for future years
    return yhat


# Use solar, wind, hydro, and geothermal data to predict future renewable production in the state.
def renewable_forecast(state, solar_gen, wind_gen, hydro_gen, geothermal_gen):
    future_years = list(
        range(2020, 2051))  # Data sets in this function go from 1989-2020, predictions go from 2020-2050
    yhat_solar = smooth2(future_years, solar_gen[state], 0.8, 0.3)  # alpha = 0.8 captures more recent trends
    yhat_wind = smooth2(future_years, wind_gen[state], 0.8, 0.3)  # alpha = 0.8 captures more recent trends
    yhat_hydro = smooth2(future_years, hydro_gen[state], 0.1,
                         0)  # alpha = 0.1 ignores yearly fluctuations and focuses on historical trends.
    yhat_geothermal = smooth2(future_years, geothermal_gen[state], 0.8, 0.3)  # alpha = 0.8 captures more recent trends
    # Sum all the dataframes to get predicted  total generation from non-combustible renewables
    r_forecast_df = yhat_solar + yhat_wind + yhat_hydro + yhat_geothermal
    return r_forecast_df


def renewable_fraction_forecast(state, historical_total,
                                r_forecast_df):  # predict Fraction or renewables generated from 2020 to 2050
    # get values between 1989 to 2020 to match solar_gen, wind_gen, etc...
    hist_total = historical_total[(historical_total['year'] >= 1989) & (historical_total['year'] <= 2020)]
    future_years = list(range(2020, 2051))
    # hist_total uses all data from 1960 to 2020
    yhat_hist_total = smooth2(future_years, hist_total[state], 0.8, 0.3)  # alpha = 0.8 captures more recent trends
    yhat_renewable_fraction = r_forecast_df / yhat_hist_total
    return yhat_renewable_fraction


def get_renewable_goals(state, state_goals):  # takes imported df of state_goals
    import pandas as pd
    # get goals for the particular state
    if state_goals['state'].isin([state]).any():  # If the state_goals df contains the selected state
        # get the subset of the state_goals df for the state
        sg = state_goals[state_goals['state'] == state]
        # details = sg['details'].iloc[0] # print this text below the state goals chart
        sg_clean = sg[sg['goal'].notna()]  # eliminate nan values. only plot if it has_goals == True
        sg_final = sg_clean[['year', 'goal']]  # return the year and goal columns for plotting.
    else:
        # sg_final = pd.DataFrame() # return empty frame
        sg_final = pd.DataFrame({'year': pd.Series(dtype='int'),
                                 'goal': pd.Series(dtype='float')})
    return sg_final


def get_goal_details(state, state_goals):  # takes imported df of state_goals and gets details text
    # get goals for the particular state
    if state_goals['state'].isin([state]).any():  # If the state_goals df contains the selected state
        # get the subset of the state_goals df for the state
        sg = state_goals[state_goals['state'] == state]
        details = sg['details'].iloc[0]  # print this text below the state goals chart
        if not isinstance(details, str):  # if nan set to empty sting
            details = ''
    else:
        details = ''
    return details
