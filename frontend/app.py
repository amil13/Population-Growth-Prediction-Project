# app.py
# Author: Amil Shrivastava
# Description:This is the entry point of the Streamlit app. 
# It connects the backend and frontend, making the app modular and easier to maintain.

import streamlit as st
import sys
import os
import django
from frontend import plot_population_trends_with_predictions

# Constants
FUTURE_YEARS = 3

# Add the root directory of your Django project to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Adjust '..' based on app.py's location
sys.path.append(project_root)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'population_growth_project.settings')  # Replace with your project's settings
django.setup()

from backend.backend import prepare_data, get_population_predictions, add_predictions_to_data

def prepare_data_opt():
    """
    Prepares data before running the app to optimize speed 
    """
    # Prepare data
    df_eu, df_non_eu, df_local, df_combined = prepare_data()

    # Get predictions
    future_eu, future_non_eu, future_local, future_combined = get_population_predictions(df_eu, df_non_eu, df_local, df_combined, future_years=FUTURE_YEARS)

    # Add predictions to the historical data for plotting
    df_eu_combined, df_non_eu_combined, df_local_combined, df_combined_all = add_predictions_to_data(df_eu, df_non_eu, df_local, df_combined, future_eu, future_non_eu, future_local, future_combined)
    
    return df_eu, df_non_eu, df_local, df_combined, df_eu_combined, df_non_eu_combined, df_local_combined, df_combined_all, future_eu, future_non_eu, future_local, future_combined 
    

def main():
    """
    Main function that runs the Streamlit app, loads the data, makes predictions,
    and plots the population trends with predictions.
    """
    
    df_eu, df_non_eu, df_local, df_combined, df_eu_combined, df_non_eu_combined, df_local_combined, df_combined_all, future_eu, future_non_eu, future_local, future_combined  = prepare_data_opt()

    # Plot data
    st.header('Population Trends with Predictions')
    st.markdown(
    'Source of data: [Opendata of Ajuntament of Barcelona](https://opendata-ajuntament.barcelona.cat/data/en/dataset/pad_mdbas_nacionalitat-g_sexe)',
    unsafe_allow_html=True
)
    st.write(
    """
    This project showcases my expertise in data processing, backend development, API design, and data visualization.
    Using publicly available data from the source mentioned above, I demonstrate end-to-end data handling by:

    - Cleaning and preprocessing raw data.
    - Storing the processed data in a robust Django backend.
    - Building APIs for seamless data retrieval and integration.
    - Visualizing trends and insights through an interactive Streamlit dashboard.

    Additionally, the project incorporates a linear regression machine learning model to forecast population trends in Barcelona
    for the next three years, providing actionable insights based on historical data.
    """
)
    plot_population_trends_with_predictions(df_eu, df_non_eu, df_local, df_combined, df_eu_combined, df_non_eu_combined, df_local_combined, df_combined_all)
    
# Run the app
if __name__ == "__main__":
    main()
