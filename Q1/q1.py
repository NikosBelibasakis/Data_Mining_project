#version 3

import os
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
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

    # Calculate the frequency of each label
    label_distribution = sampled_df['label'].value_counts()

    # Create a bar chart
    plt.figure(figsize=(8, 6))
    sns.barplot(x=label_distribution.index, y=label_distribution.values)
    plt.xlabel('Activity Label')
    plt.ylabel('Frequency')
    plt.title('Distribution of Activity Labels')
    plt.show()

    # Calculate summary statistics for each group
    grouped_data = sampled_df.groupby('label')

    # Columns to analyze
    sensor_columns = ['back_x', 'back_y', 'back_z', 'thigh_x', 'thigh_y', 'thigh_z']

    # Plot histograms for each sensor value grouped by label
    for label, group in grouped_data:
        plt.figure(figsize=(12, 8))
        plt.suptitle(f'Distribution of Sensor Values for Activity ID {label}')
        
        # Plot histograms for each sensor column
        for idx, sensor_col in enumerate(sensor_columns, 1):
            plt.subplot(2, 3, idx)
            sns.histplot(group[sensor_col], kde=True, bins=30, color='blue')
            plt.title(sensor_col)
        
        plt.tight_layout()
        plt.show()

        '''# Plot acceleration over time for each action
        plt.figure(figsize=(12, 8))
        plt.suptitle(f'Acceleration Over Time for Activity ID {label}')
        
        # Plot each sensor column against time
        for idx, sensor_col in enumerate(sensor_columns, 1):
            plt.subplot(2, 3, idx)
            sns.lineplot(x=group['timestamp'], y=group[sensor_col])
            plt.title(sensor_col)
            plt.xlabel('Time')
            plt.ylabel('Acceleration (g)')
        
        plt.tight_layout()
        plt.show()
        THE ABOVE NEEDS WORK
        1.FIND A WAY TO NOT DISPLAY EVERY FIGURE AFTER CLODING THE OTHER
        2.MAKE FEWER GRAPHS (CONSIDER MAKING LIKE A MEDIAN)
'''
    # Plot boxplots for each sensor value grouped by label
    plt.figure(figsize=(15, 10))
    for idx, sensor_col in enumerate(sensor_columns):
        plt.subplot(2, 3, idx + 1)
        sns.boxplot(data=sampled_df, x='label', y=sensor_col)
        plt.title(sensor_col)
    plt.suptitle('Boxplots of Sensor Values by Label')
    plt.tight_layout()
    plt.show()

    # Define the new CSV filename
    new_csv_filename = f'{filename}.csv'

    # Full path for the new CSV file in the 'new_data' folder
    new_csv_fullpath = os.path.join(new_data_path, new_csv_filename)

    # Save the sampled dataframe to the new CSV file
    sampled_df.to_csv(new_csv_fullpath, index=False)

    print(f'New CSV file created: {new_csv_fullpath}')
