import cv2
import sys
import numpy as np
import random as rand 
import click
import pandas as pd
from data_extraction import DataExtractor
from database_utils import DatabaseConnector
class DataCleaning:

   '''
   Cleans and transforms data for various data sources, ensuring data consistency and formatting.
   '''
    
   def __init__(self)-> None:
        pass
   
   def clean_user_data(self):

    '''
        Cleans the user data from the 'legacy_users' SQL table by processing addresses 
        and join dates. Returns a cleaned pandas DataFrame.

        - Replaces newline characters in the 'address' column with a single space.
        - Converts the 'join_date' column to a uniform date format ('yyyy-mm-dd') and 
          filters out rows with invalid dates.
        - Saves the cleaned data to an Excel file.

        Returns:
           pd.DataFrame: The cleaned pandas DataFrame with user data.
    '''   

    dt_extractor=DataExtractor() #Intialising data extractor

    client_data=dt_extractor.read_rds_table('legacy_users') #getting python dataframe storing client data
    
    # in address column replacing '\n' with ' '
    client_data['address'] = client_data['address'].str.replace('\n', ' ', regex=False)

    # Assuming df_unfiltered is your dataframe and contains a 'join_date' column
    
    # Helper function to handle different custom date formats
    def parse_custom_dates(date_str):
       try:
        # First attempt to parse using the default format
        return pd.to_datetime(date_str, format='%Y-%m-%d', errors='raise')
       except:
        # Try to handle formats like 'Month dd, yyyy' or 'Month yyyy dd'
         try:
            return pd.to_datetime(date_str, errors='coerce')  # This will parse a wider range of formats
         except:
            return pd.NaT  # If all fails, mark as NaT

    # Convert 'join_date' to datetime, forcing errors to 'NaT' for invalid dates
    client_data['join_date'] = client_data['join_date'].apply(parse_custom_dates)

    # Filter out rows where 'join_date' couldn't be converted (i.e., where it's NaT)
    client_data_filtered = client_data[client_data['join_date'].notna()]

    # Converts the join_date column from a datetime object into a string representation in 'yyyy-mm-dd'
    client_data_filtered['join_date'] = client_data_filtered['join_date'].dt.strftime('%Y-%m-%d')

    print(client_data_filtered.tail())

    output_path = 'client_data_filtered.xlsx'

    # Write the filtered DataFrame to an Excel file
    client_data_filtered.to_excel(output_path, index=False)

    # This will save the filtered DataFrame to an Excel file without the index
    print(f"DataFrame successfully saved to {output_path}")
   
    return client_data_filtered #returns the cleaned client data

cleaned=DataCleaning()

DBCon=DatabaseConnector()

DBCon.upload_to_db('dim_users',cleaned.clean_user_data())