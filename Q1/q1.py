#version 2

import os
import pandas as pd
import glob

# Get the current working directory (where the script is running)
current_dir = os.getcwd()

# Path to the folder containing the CSV files
folder_path = os.path.join(current_dir, 'harth')

# Get all the CSV files from the folder
csv_files = glob.glob(folder_path + '/*.csv')

# Create a dictionary to store the dataframes / CSV files
dataframes_dict = {}

# Load each CSV file into the dictionary
for csv_file in csv_files:
    # Extract the file's name without the .csv extension
    filename = os.path.splitext(os.path.basename(csv_file))[0]

    # Load the CSV file into a dataframe
    df = pd.read_csv(csv_file)

    # Store the dataframe in the dictionary. The key is the file's name.
    dataframes_dict[filename] = df

# Create the 'new_data' folder (where the new CSV files will be stored) in the current directory if it doesn't exist
new_data_path = os.path.join(current_dir, 'new_data')
os.makedirs(new_data_path, exist_ok=True)

# Sample every 10 rows and create a new CSV file for each original CSV
for filename, df in dataframes_dict.items():
    # Sample every 10th row
    sampled_df = df.iloc[::10]

    # Define the new CSV filename
    new_csv_filename = f'{filename}.csv'

    # Full path for the new CSV file in the 'new_data' folder
    new_csv_fullpath = os.path.join(new_data_path, new_csv_filename)

    # Save the sampled dataframe to the new CSV file
    sampled_df.to_csv(new_csv_fullpath, index=False)

    print(f'Νew CSV file created: {new_csv_fullpath}')
