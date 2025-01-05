# data_processing.py
# Author: Amil Shrivastava
# Description: This script processes raw CSV files in the current folder, cleans them by removing invalid entries, 
# drops unnecessary columns, and then aggregates the data based on nationality and reference date. The cleaned files 
# are saved into an output folder called cleaned_data for further analysis.

import pandas as pd
import os

# Paths to input and output folders
input_folder = "data/."   # Specify the path to the folder containing the raw input CSV files
output_folder = "data/cleaned_data"  # Specify the path to the folder where cleaned CSV files will be saved

# Create the output folder if it doesn't already exist
os.makedirs(output_folder, exist_ok=True)

# Mapping for NACIONALITAT_G column to more readable country names
nationality_mapping = {
    1: 'Local',
    2: 'EU',
    3: 'Non-EU',
    4: 'Unknown'
}

def clean_csv_file(file_path, output_path):
    """
    Cleans a CSV file by performing the following operations:
    - Removes unnecessary columns
    - Replaces invalid values ('..') with NaN and drops rows with NaN values
    - Maps numerical nationality values to readable names
    - Aggregates data by nationality and sums the 'Valor' column
    - Saves the cleaned data to a new CSV file
    
    Args:
        file_path (str): Path to the input CSV file.
        output_path (str): Path to save the cleaned CSV file.
    """
    # Read the raw CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Drop unnecessary columns that are not relevant to the analysis
    columns_to_drop = ['Codi_Districte', 'Nom_Districte', 'Codi_Barri', 'Nom_Barri', 'SEXE', 'EDAT_Q']
    df = df.drop(columns=columns_to_drop)
    
    # Replace '..' with NaN and drop rows with missing values
    df = df.replace('..', pd.NA).dropna()
    
    # Map the 'NACIONALITAT_G' column values to country names using the predefined mapping
    df['NACIONALITAT_G'] = df['NACIONALITAT_G'].map(nationality_mapping)    
    
    # Convert 'Valor' column to numeric, coercing errors to NaN
    df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')

    # Group by 'NACIONALITAT_G' and sum the 'Valor' for each nationality
    # Also, retain the 'Data_Referencia' as the first value in the group
    df = df.groupby('NACIONALITAT_G', as_index=False).agg({
        'Valor': 'sum',
        'Data_Referencia': 'first'
    })    
    
    # Reorganize the columns to match the desired output format
    df = df[['Data_Referencia', 'Valor', 'NACIONALITAT_G']]
    
    # Save the cleaned DataFrame to a new CSV file
    df.to_csv(output_path, index=False)
    ## Debugging
    # print(f"Processed: {file_path} -> {output_path}")

# Iterate over all files in the input folder
for file_name in os.listdir(input_folder):
    # Skip processing for 'pad_dimensions.csv' as it's not required
    if file_name == "pad_dimensions.csv":
        print("Skipping 'pad_dimensions.csv'")
        continue
    
    # Process only CSV files
    if file_name.endswith('.csv'):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, f"cleaned_{file_name}")
        clean_csv_file(input_path, output_path)

# Final message indicating that processing is complete
print("Processing complete. All cleaned files are saved in the output folder.")
