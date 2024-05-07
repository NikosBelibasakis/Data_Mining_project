#version 3

from datetime import datetime
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

# Columns to round to 4 decimal digits (back_x,back_y,back_z,thigh_x,thigh_y,thigh_z)
columns_to_round = ["back_x", "back_y", "back_z", "thigh_x", "thigh_y", "thigh_z"]

# Sample every 10 rows and create a new CSV file for each original CSV
for filename, df in dataframes_dict.items():
    # Sample every 10th row
    sampled_df = df.iloc[::10]

    # Round the columns back_x,back_y,back_z,thigh_x,thigh_y,thigh_z
    sampled_df.loc[:, columns_to_round] = sampled_df[columns_to_round].round(4)


    # Some csv files have included nanoseconds on their timestamps
    #              eg. 2016-12-05 13:17:56.548657565 in file S020
    # while most of them have only for milliseconds which is easier for analyzing our data
    # Truncate the timestamps in the specified columns
    sampled_df.loc[:, 'timestamp'] = sampled_df['timestamp'].str[:23]

    # Define the new CSV filename
    new_csv_filename = f'{filename}.csv'

    # Full path for the new CSV file in the 'new_data' folder
    new_csv_fullpath = os.path.join(new_data_path, new_csv_filename)

    # Save the sampled dataframe to the new CSV file
    sampled_df.to_csv(new_csv_fullpath, index=False)

    print(f'New CSV file created: {new_csv_fullpath}')
