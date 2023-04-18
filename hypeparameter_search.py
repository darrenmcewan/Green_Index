from autots import AutoTS
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt

start_date = '1960'
data_dir = 'C:/Users/abi/Documents/GitHub/Wind_visualization/data/'
for file in ['historical_renewable_energy_production_by_state_in_billion_Btu.csv', 'geothermal_production.csv']:
    for state in ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'US', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']:
        df = pd.read_csv(os.path.join(data_dir, file), usecols=['year', state])
        df['year'] = pd.to_datetime(df['year'], format='%Y')
        df = df.sort_values('year')
        print(df[:2])

        long=True
        model = AutoTS(
            forecast_length=10,
            frequency='infer',
            prediction_interval=0.9,
            ensemble=None,
            model_list="fast",
            transformer_list="fast",
            drop_most_recent=1,
            max_generations=4,
            num_validations=2,
            validation_method="backwards"
        )
        model = model.fit(
            df,
            date_col='year' if long else None,
            value_col=state if long else None,
            # id_col='123' if long else None,
        )

        prediction = model.predict()
        prediction.plot(model.df_wide_numeric,
                        series=model.df_wide_numeric.columns[0],
                        start_date=start_date)
        print(model)
        forecasts_df = prediction.forecast
        forecasts_up, forecasts_low = prediction.upper_forecast, prediction.lower_forecast

        # accuracy of all tried model results
        model_results = model.results()
        # and aggregated from cross validation
        validation_results = model.results("validation")