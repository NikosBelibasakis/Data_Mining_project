import pandas as pd
import os

# Directory where the CSV files are stored
directory = './new_data'  # Replace with the actual directory if different

# List to hold the dataframes
dfs = []

# We process each CSV file in the folder
for idx, filename in enumerate(sorted(os.listdir(directory)), start=1):
    # Read the CSV file
    df = pd.read_csv(os.path.join(directory, filename))

    # Drop the timestamp and label columns
    df = df.drop(columns=['timestamp', 'label'])

    # Calculate the mean of each column and round it to 4 decimal digits
    means = df.mean().round(4).to_frame().T

    # Add an ID column
    means['id'] = idx

    # Append the dataframe to the list
    dfs.append(means)

# Concatenate all dataframes into one
final_df = pd.concat(dfs, ignore_index=True)

# Ensure 'index' and 'Unnamed: 0' columns are not included
if 'Unnamed: 0' in final_df.columns:
    final_df = final_df.drop(columns=['Unnamed: 0'])
if 'index' in final_df.columns:
    final_df = final_df.drop(columns=['index'])

# Save the final dataframe to a new CSV file
final_df.to_csv('new_data2.csv', index=False)
print(f'New CSV file created.')