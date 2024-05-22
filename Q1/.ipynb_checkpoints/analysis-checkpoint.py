import os
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import glob
from datetime import datetime, timedelta

# Get the current working directory (where the script is running)
current_dir = os.getcwd()

# Path to the folder containing the CSV files
folder_path = os.path.join(current_dir, 'new_data')  # Assuming you want to work with the sampled data

# Get all the CSV files from the folder
csv_files = glob.glob(folder_path + '/*.csv')

# Columns to analyze
sensor_columns = ['back_x', 'back_y', 'back_z', 'thigh_x', 'thigh_y', 'thigh_z']

# Create a dictionary to store the grouped data for each action
action_labels = [1, 2, 3, 4, 5, 6, 7, 8, 13, 14, 130, 140] #action labels
action_data_dict = {label: [] for label in action_labels} #dictionary initialization

# List to store data from all files
all_data = []

# Load each CSV file and group data by action (label)
for idx,csv_file in enumerate(csv_files):
    # Load the CSV file into a dataframe
    df = pd.read_csv(csv_file)

    # Add a new column 'file_id' containing the identifier
    df['file_id'] = idx + 1  # Adding 1 to start file IDs from 1
    
    # Append the DataFrame to the list
    all_data.append(df)
    
    # Group data by label and store in the dictionary
    grouped_data = df.groupby('label')
    for label, group in grouped_data:
        action_data_dict[label].append(group)

# Combine all data into a single DataFrame
combined_data = pd.concat(all_data)


"""DISTRIBUTION OF ACTIVITY LABELS"""

# Calculate the frequency of each label
label_distribution = combined_data['label'].value_counts()

# Create a bar chart
plt.figure(figsize=(8, 6))
sns.barplot(x=label_distribution.index, y=label_distribution.values)
plt.xlabel('Activity Label')
plt.ylabel('Frequency')
plt.title('Distribution of Activity Labels')


"""DISTRIBUTION OF SENSOR VALUES"""
# Plot histograms for each sensor value grouped by label across different participants
for label, groups in action_data_dict.items():
    plt.figure(figsize=(12, 8))
    plt.suptitle(f'Distribution of Sensor Values for Activity ID {label} across Participants')
    
    # Plot histograms for each sensor column
    for idx, sensor_col in enumerate(sensor_columns, 1):
        plt.subplot(2, 3, idx)
        
        # Plot data from different participants on the same graph
        # Loop through each action label
        for group in groups:
            # Plot PDF for sensor data of the current action label with KDE
            sns.kdeplot(group[sensor_col], fill=False)
    
    # Add a small pause to allow plots to display properly
    plt.pause(1.0)


"""ACCELARATION OF ACTIONS IN TIME"""
combined_data=combined_data.iloc[::100]
grouped_data = combined_data.groupby('label')
time_threshold =  timedelta(seconds=2)  # 200 ms the time threshold

# Iterate through each group (activity label)
for label, group in grouped_data:
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    fig.suptitle(f'Acceleration over Time for Activity {label}')
    # Flatten the axes array for easier indexing
    axes = axes.flatten()

    # Initialize variables for the loop
    file=0
    previous_timestamp = None
    time_difference = timedelta(seconds=0)
    time=[]
    accelaration_rows = {col: [] for col in sensor_columns}

    # Iterate through the rows in the group
    for idx, row in group.iterrows():
        # Convert current timestamp to datetime object
        current_timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        # Adjust the timestamp
        #firstly remove the date
        current_timestamp = (current_timestamp - current_timestamp.replace(hour=0, minute=0, second=0, microsecond=0))

        #initialize every beginning of an action to time zero
        if row["file_id"]!=file:
            time_difference=current_timestamp
            file=row['file_id']

        current_timestamp = current_timestamp - time_difference # subtracting the cumulative time difference

        # Calculate the time difference from the previous timestamp
        if previous_timestamp is not None:
            time_diff = current_timestamp - previous_timestamp

            # If time difference exceeds the threshold, reset time_difference
            if time_diff > time_threshold:
                time_difference += time_diff

                # Iterate through the sensor columns and plot each one in a different subplot
                for i, sensor_col in enumerate(sensor_columns):
                    sns.lineplot(x=time, 
                                y=accelaration_rows[sensor_col], 
                                ax=axes[i])
                    axes[i].set_title(sensor_col)
                
                # Reset the lists for the next segment
                time = []
                accelaration_rows = {col: [] for col in sensor_columns}

        #populate with the values of each segment
        time.append(current_timestamp)
        for col in sensor_columns:
            accelaration_rows[col].append(row[col])
        
        # Update the previous timestamp for the next iteration
        previous_timestamp = current_timestamp

    # Set common labels for the figure
    for ax in axes:
        ax.set_xlabel('Adjusted Time')
        ax.set_ylabel('Acceleration')
    
    # Adjust layout and show the plot
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

plt.show()
