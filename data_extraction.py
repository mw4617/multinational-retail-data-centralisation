import cv2
import sys
import numpy as np
import random as rand 
import click
from database_utils import DatabaseConnector
import pandas as pd
import tabula

class DataExtractor():

    '''
    Extracts data from various data sources, including SQL databases, and loads it into pandas DataFrames.
    '''
    
    def __init__(self)-> None:
   
        pass


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


