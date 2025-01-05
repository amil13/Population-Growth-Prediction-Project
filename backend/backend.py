# backend.py
# Author: Amil Shrivastava
# Description: This handles the data processing and predictions.
# It fetches data from the database, filters it by nationality, 
# and predicts future population trends.

import pandas as pd
from scripts.predict_population_trends import predict_population
from population.models import PopulationData

def load_population_data():
    """
    Loads population data from the Django database using the PopulationData model.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the population data.
    """
    data = PopulationData.objects.all().values('date', 'population_count', 'nationality')
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])  # Ensure 'date' is in datetime format
    return df

def prepare_data():
    """
    Prepares the data for EU, Non-EU, Local, and Unknown populations.
    
    Returns:
        tuple: A tuple containing:
            - df_eu (pd.DataFrame): EU population data.
            - df_non_eu (pd.DataFrame): Non-EU population data.
            - df_local (pd.DataFrame): Local population data.
            - df_combined (pd.DataFrame): Combined population data (EU + Non-EU + Local + Unknown).
    """
    df = load_population_data()  # Load population data

    # Filter data into Local, EU, Non-EU, and Unknown categories
    df_local = df[df['nationality'] == 'Local'].sort_values(by='date').reset_index(drop=True)
    df_eu = df[df['nationality'] == 'EU'].sort_values(by='date').reset_index(drop=True)
    df_non_eu = df[df['nationality'] == 'Non-EU'].sort_values(by='date').reset_index(drop=True)
    df_unknown = df[df['nationality'] == 'Unknown'].sort_values(by='date').reset_index(drop=True)

    # Combine the Local, EU, Non-EU, and Unknown data to get the total population by date
    df_combined = pd.concat([df_local, df_eu, df_non_eu, df_unknown]).groupby(['date']).agg({'population_count': 'sum'}).reset_index()
    
    return df_eu, df_non_eu, df_local, df_combined

def get_population_predictions(df_eu, df_non_eu, df_local, df_combined, future_years):
    """
    Gets population predictions for EU, Non-EU, and Combined populations.

    Args:
        df_eu (pd.DataFrame): EU population data.
        df_non_eu (pd.DataFrame): Non-EU population data.
        df_local (pd.DataFrame): Local population data.
        df_combined (pd.DataFrame): Combined population data (EU + Non-EU + Local).

    Returns:
        tuple: A tuple containing:
            - future_eu (pd.DataFrame): Predicted EU population data.
            - future_non_eu (pd.DataFrame): Predicted Non-EU population data.
            - future_local (pd.DataFrame): Predicted local population data.
            - future_combined (pd.DataFrame): Predicted combined population data.
    """
    future_eu = predict_population(df_eu, years_ahead=future_years)
    future_non_eu = predict_population(df_non_eu, years_ahead=future_years)
    future_local = predict_population(df_local, years_ahead=future_years)
    future_combined = predict_population(df_combined, years_ahead=future_years)
    
    return future_eu, future_non_eu, future_local, future_combined

def add_predictions_to_data(df_eu, df_non_eu, df_local, df_combined, future_eu, future_non_eu, future_local, future_combined):
    """
    Adds the predicted population data to the historical data for smooth visualization.

    Args:
        df_eu (pd.DataFrame): Historical EU population data.
        df_non_eu (pd.DataFrame): Historical Non-EU population data.
        df_local (pd.DataFrame): Historical local population data.
        df_combined (pd.DataFrame): Historical combined population data.
        future_eu (pd.DataFrame): Predicted EU population data.
        future_non_eu (pd.DataFrame): Predicted Non-EU population data.
        future_local (pd.DataFrame): Predicted Local population data.
        future_combined (pd.DataFrame): Predicted combined population data.

    Returns:
        tuple: A tuple containing:
            - df_eu_combined (pd.DataFrame): EU population data including predictions.
            - df_non_eu_combined (pd.DataFrame): Non-EU population data including predictions.
            - df_local_combined (pd.DataFrame): Local population data including predictions.
            - df_combined_all (pd.DataFrame): Combined population data including predictions.
    """
    last_row = df_eu.iloc[[-1]][['date', 'population_count']]
    df_eu_combined = pd.concat([last_row, future_eu])

    last_row = df_non_eu.iloc[[-1]][['date', 'population_count']]
    df_non_eu_combined = pd.concat([last_row, future_non_eu])
    
    last_row = df_local.iloc[[-1]][['date', 'population_count']]
    df_local_combined = pd.concat([last_row, future_local])

    last_row = df_combined.iloc[[-1]][['date', 'population_count']]
    df_combined_all = pd.concat([last_row, future_combined])

    return df_eu_combined, df_non_eu_combined, df_local_combined, df_combined_all
