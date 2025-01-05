# population_prediction.py
# Author: Amil Shrivastava
# Description: This script predicts future population counts based on historical data using linear regression.
# The function takes a DataFrame containing historical population data and forecasts the population for a specified number of future years.

from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

def predict_population(df, years_ahead=3):
    """
    Predicts future population counts based on historical data using linear regression.
    
    The function groups the data by year, applies linear regression to model the population growth trend, 
    and predicts the population count for the specified number of future years.
    
    Args:
        df (pd.DataFrame): DataFrame containing historical data with a 'date' and 'population_count' column.
        years_ahead (int): Number of years ahead to predict. Default is 3 years.
        
    Returns:
        pd.DataFrame: DataFrame containing predicted population counts for the future years.
    """
    
    # Ensure the 'date' column is in datetime format, if it's not already
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Extract the year from the 'date' column for aggregation
    df['year'] = df['date'].dt.year
    
    # Group the data by year and calculate the total population count for each year
    df_grouped = df.groupby('year').agg({'population_count': 'sum'}).reset_index()
    
    # Prepare the feature (X) and target (y) variables for the linear regression model
    X = df_grouped[['year']] # Years as the feature variable
    y = df_grouped['population_count']     # Population counts as the target variable
    
    # Initialize and train the linear regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Generate a DataFrame for the future years based on the latest year in the dataset
    future_years = pd.DataFrame({
        'year': list(range(df_grouped['year'].max() + 1, df_grouped['year'].max() + 1 + years_ahead))
    })
    
    ## debugging
    # print(f"Predicting population for the following future years: {future_years['year'].values}")
    
    # Predict the population for the future years using the trained model
    predicted_population = model.predict(future_years[['year']])
    
    # Combine the predicted population with the corresponding future years into a DataFrame
    future_df = pd.DataFrame({
        'date': pd.to_datetime(future_years['year'], format='%Y'),  # Convert 'year' to datetime format
        'population_count': predicted_population
    })
    
    return future_df
