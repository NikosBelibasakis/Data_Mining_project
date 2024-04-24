#version 1

import pandas as pd
import glob

#Open the folder where the csv files are stored
folder_path = 'C:/Users/30690/Desktop/harth'

#Get all the csv files from the folder
csv_files = glob.glob(folder_path + '/*.csv')

#Create a dictionary to store all the dataframes (CSVs)
dataframes_dict = {}

#Load every csv file and add it in the dictionary
for csv_file in csv_files:
    #Get the file's name
    filename = csv_file.split('\\')[-1].split('.')[0]

    #Load the csv file
    df = pd.read_csv(csv_file)

    #Store the dataframe / CSV in the dictionary. The key is each CSV's name.
    dataframes_dict[filename] = df





