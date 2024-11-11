import cv2
import sys
import numpy as np
import random as rand 
import click
from database_utils import DatabaseConnector
import pandas as pd
import tabula
import requests
import json
import boto3

class DataExtractor():

    '''
    Extracts data from various data sources, including SQL databases, and loads it into pandas DataFrames.
    '''
    
    def __init__(self)-> None:
    
        """
        Initializes the DataExtractor instance, setting up a header dictionary 
        with an API key for accessing store data.
        """
        #header dict for accessing the stores data API
        self.header_dict={'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}


    def read_rds_table(self,table_name):

        '''
        Extracts data from the specified table in the online PostgreSQL database
        and returns it as a pandas DataFrame.

        Args:
           table_name (str): The name of the table to read from the database.

        Returns:
           pd.DataFrame: A pandas DataFrame containing the extracted data from the SQL table.
        '''    

        # Create an instance of DatabaseConnector
        db_connector=DatabaseConnector()
        
        # Initialize the database engine
        engine=db_connector.init_db_engine()
        
        # List tables
        db_connector.list_db_tables()
        
        # Read the SQL table into a pandas DataFrame
        df = pd.read_sql_table(table_name, con=engine)

        pd.set_option('display.max_rows', None)  # Show all rows
        pd.set_option('display.max_columns', None)  # Show all columns

        # Display the DataFrame
        print(df.tail()) 

        return df 

    def retrieve_pdf_data(self,pdf_url):

        """
         Takes in a link as an argument, converts the pdf to pandas DataFrame and returns it.

         Args:
            pdf_url (str): url of the pdf that is being converted

        Returns:

            card_details_df (pd.DataFrame): pandas dataframe containing the card detail table   
        """
        
        #Converting pdf in to list of dataframes
        card_details_df_list=tabula.read_pdf(pdf_url,stream=True,pages='all')
        
        # Combine all the DataFrames in the list into a single DataFrame
        card_details_df = pd.concat(card_details_df_list, ignore_index=True)

        pd.set_option('display.max_columns', None)  # Show all columns
    
        print(card_details_df)

        return card_details_df
    
    def list_number_of_stores(self, no_stores_api_endpoint,header_dict):
        
        """
        Retrieves the total number of stores from an API endpoint.

        Args:
            no_stores_api_endpoint (str): The API endpoint URL to fetch the number of stores.
            header_dict (dict): Dictionary containing the headers required for API access.

        Returns:
            int: The total number of stores if the request is successful, otherwise None.
        """

        response = requests.get(no_stores_api_endpoint, headers=header_dict)

        if response.status_code == 200:
            no_stores = response.json().get('number_stores',0)  # Extract number_of_stores key
            return no_stores
        else:
            print(f"Failed to retrieve number of stores. Status code: {response.status_code}")
            return None

    def retrieve_stores_data(self, retrieve_stores_api_endpoint,header_dict):
        
        """
        Retrieves store data from an API endpoint for a specified number of stores.

        Args:
            retrieve_stores_api_endpoint (str): The API endpoint to retrieve each store's data.
            header_dict (dict): Dictionary containing headers required for API access.

        Returns:
            pd.DataFrame: A pandas DataFrame containing data for each store.
        """

        # Get the number of stores
        no_stores = self.list_number_of_stores('https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores',header_dict)

        if no_stores is None:
            print("Unable to retrieve store data due to missing store count.")
            return
        #getting dateframe first store retreived through api and intialising store_df
        response = requests.get(retrieve_stores_api_endpoint.format(0),headers=header_dict)
        
        store_df=response.json()
        
        store_df=pd.DataFrame([store_df])

        print(f"Store {0} data: {store_df}")

        
        # Loop through each store after the first one and retrieve data
        for store_number in range(no_stores-1):
            response = requests.get(retrieve_stores_api_endpoint.format(store_number+1),headers=header_dict)

            if response.status_code == 200:
                store_data = response.json()  # Corrected to use .json() as a method

                current_store_df=pd.DataFrame([store_data])

                store_df=pd.concat([store_df,current_store_df])

                #print(f"Store {store_number+1} data: {store_data}")
            else:
                print(f"Failed to retrieve data for store {store_number}.  Status code: {response.status_code}")
        
        #optional save to excel file
        #store_df.to_excel('stores_data.xlsx', index=False)  

        return store_df      

    def extract_from_s3(self):

        """
        Downloads a product information CSV file from an Amazon S3 bucket, encoded in UTF-8, and loads it into a pandas DataFrame.

        This method connects to an S3 bucket, downloads a specified CSV file containing product information, and 
        reads it into a pandas DataFrame for further processing. The CSV file is read using UTF-8 encoding, ensuring
        proper handling of special characters. The function assumes a default region and file path for saving the 
        downloaded file locally.

        Returns:
            pd.DataFrame: A pandas DataFrame containing product information from the downloaded CSV file, with UTF-8 encoding applied.
        """

        #dowloading product information .csv file
        s3 = boto3.client('s3', region_name='eu-west-2')

        local_file_path=r'C:\Users\micha\multinational-retail-data-centralisation\multinational-retail-data-centralisation\product_information.csv'

        s3.download_file('data-handling-public', 'products.csv',local_file_path)
        
        #saving product information dataframe
        product_information = pd.read_csv(local_file_path, encoding='utf-8')

        #optional
        #product_information.to_excel('product_data_uncleaned.xlsx', index=False)

        return product_information

    def extract_json_from_s3(self):
     
     """
    Downloads a JSON file containing date details from an Amazon S3 bucket, 
    loads it into a pandas DataFrame, and optionally saves it as an Excel file.

    This method connects to an S3 bucket, downloads a specified JSON file,
    and reads it into a pandas DataFrame for further processing. 

    Returns:
        pd.DataFrame: A pandas DataFrame containing the data from the JSON file.
     """

     # Connect to S3
     s3 = boto3.client('s3', region_name='eu-west-1')

     local_file_path=r'C:\Users\micha\multinational-retail-data-centralisation\multinational-retail-data-centralisation\date_details.json'

     s3.download_file('data-handling-public', 'date_details.json',local_file_path)

     date_details=pd.read_json(local_file_path,encoding='utf-8')
     
     #optional
     #date_details.to_excel('date_details.xlsx', index=False)

     return date_details





DX=DataExtractor()
#header={'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
#DX.retrieve_stores_data('https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{}',header)

#DX.extract_from_s3()

DX.extract_json_from_s3()