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
        
    '''
    Intialises DataCleaning class by creating an instance of DataExtractor for use by DataCleaning methods
    '''
    self.dt_extractor=DataExtractor() #Intialising data extractor

        # Helper function to handle different custom date formats
   def parse_custom_dates(self,date_str):
       """
    Attempts to parse a date string into a datetime object, supporting multiple date formats.

    The function first tries to parse the date string in the 'yyyy-mm-dd' format. If it fails,
    it attempts to coerce the date string into a valid datetime object by trying to handle
    other common formats like 'Month dd, yyyy' or 'Month yyyy dd'. If parsing fails completely,
    it returns NaT (Not a Time).

    Args:
        date_str (str): The date string to be parsed.

    Returns:
        pd.Timestamp or pd.NaT: The parsed date as a pandas Timestamp if successful, or NaT if parsing fails.
       """
       try:
        # First attempt to parse using the default format
        return pd.to_datetime(date_str, format='%Y-%m-%d', errors='raise')
       except:
        # Try to handle formats like 'Month dd, yyyy' or 'Month yyyy dd'
         try:
            return pd.to_datetime(date_str, errors='coerce')  # This will parse a wider range of formats
         except:
            return pd.NaT  # If all fails, mark as NaT
   
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

    client_data=self.dt_extractor.read_rds_table('legacy_users') #getting python dataframe storing client data
    
    # in address column replacing '\n' with ' '
    client_data['address'] = client_data['address'].str.replace('\n', ' ', regex=False)

    # Assuming df_unfiltered is your dataframe and contains a 'join_date' column

    # Convert 'join_date' to datetime, forcing errors to 'NaT' for invalid dates
    client_data['join_date'] = client_data['join_date'].apply(self.parse_custom_dates)

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
   
   def clean_card_data(self,url):
     
     """
    Cleans the card details data extracted from a PDF file at the provided URL, ensuring date consistency and proper formatting.

    This method:
    
    1. Extracts card details data from the specified PDF file using the 'retrieve_pdf_data' method.
    2. Processes the 'date_payment_confirmed' column by:
       - Parsing the date strings into a uniform 'yyyy-mm-dd' format.
       - Filtering out rows where the 'date_payment_confirmed' could not be successfully converted (i.e., invalid dates).
    3. Removes unnecessary or erroneous columns such as 'card_number expiry_date' and 'Unnamed: 0' (if they exist).
    4. Returns the cleaned pandas DataFrame with valid data and consistent formatting.

    Args:
        url (str): The URL of the PDF file containing the card details to be extracted and cleaned.

    Returns:
        pd.DataFrame: A cleaned pandas DataFrame containing valid card details with consistent date formatting and relevant columns only.
     """
     #extracting pandas dateframe containing card details
     card_deatils_df=self.dt_extractor.retrieve_pdf_data(url)
     
     # Convert 'date_payment_confirmed' to datetime, forcing errors to 'NaT' for invalid dates
     card_deatils_df['date_payment_confirmed'] = card_deatils_df['date_payment_confirmed'].apply(self.parse_custom_dates)

     # Filter out rows where 'date_payment_confirmed' couldn't be converted (i.e., where it's NaT)
     card_deatils_df_filtered = card_deatils_df[card_deatils_df['date_payment_confirmed'].notna()]
     
     #dropping erronous columns with null values
     card_deatils_df_filtered = card_deatils_df_filtered.drop(columns=['card_number expiry_date', 'Unnamed: 0'], errors='ignore')

     #Return filtered dataframe
     return card_deatils_df_filtered

cleaned=DataCleaning()

DBCon=DatabaseConnector()

DBCon.upload_to_db('dim_users',cleaned.clean_user_data())

DBCon.upload_to_db('dim_card_details',cleaned.clean_card_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf'))