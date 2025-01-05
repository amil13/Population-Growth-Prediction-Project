# frontend.py
# Author: Amil Shrivastava
# Description: This is responsible for the Streamlit front-end. 
# It renders the plots, handles the UI, and displays data.

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

# Custom Y-axis formatter
def format_y_axis(value, pos):
    """
    Custom formatter for large numbers on the y-axis.

    Args:
        value (float): The y-axis value.
        pos (int): The tick position.

    Returns:
        str: The formatted value.
    """
    if value >= 1000:
        return f'{value/1000:.0f}k'
    return f'{value:.0f}'

def plot_population_trends_with_predictions(df_eu, df_non_eu, df_local, df_combined, future_eu, future_non_eu, future_local, future_combined):
    """
    Plots the historical and predicted population trends.

    Args:
        df_eu (pd.DataFrame): Historical EU population data.
        df_non_eu (pd.DataFrame): Historical Non-EU population data.
        df_local (pd.DataFrame): Historical local population data.
        df_combined (pd.DataFrame): Historical combined population data.
        future_eu (pd.DataFrame): Predicted EU population data.
        future_non_eu (pd.DataFrame): Predicted Non-EU population data.
        future_local (pd.DataFrame): Predicted local population data.
        future_combined (pd.DataFrame): Predicted combined population data.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the historical and predicted data
    sns.lineplot(data=df_eu, x='date', y='population_count', ax=ax, label='EU Population (Historical)', color='blue', linestyle='solid', marker='o', markersize=4) 
    sns.lineplot(data=future_eu, x='date', y='population_count', ax=ax, color='black', linestyle='dotted', marker='o', markersize=4) 
    
    sns.lineplot(data=df_non_eu, x='date', y='population_count', ax=ax, label='Non-EU Population (Historical)', color='red', linestyle='solid', marker='o', markersize=4)
    sns.lineplot(data=future_non_eu, x='date', y='population_count', ax=ax, color='black', linestyle='dotted', marker='o', markersize=4)
    
    sns.lineplot(data=df_local, x='date', y='population_count', ax=ax, label='Local Population (Historical)', color='Yellow', linestyle='solid', marker='o', markersize=4)
    sns.lineplot(data=future_local, x='date', y='population_count', ax=ax, color='black', linestyle='dotted', marker='o', markersize=4)
    
    sns.lineplot(data=df_combined, x='date', y='population_count', ax=ax, label='Total Population (Historical)', color='green', linestyle='solid', marker='o', markersize=4)
    sns.lineplot(data=future_combined, x='date', y='population_count', ax=ax, label='Predicted Population', color='black', linestyle='dotted', marker='o', markersize=4)

    # Format y-axis
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_y_axis))

    ax.set_title('Barcelona City Population Trends (EU, Non-EU, Local and Total) with Predictions')
    ax.set_xlabel('Year')
    ax.set_ylabel('Population Count')
    plt.xticks(rotation=45) 
    ax.legend()
    st.pyplot(fig)
