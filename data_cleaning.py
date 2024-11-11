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

    """
    Initializes the DataCleaning class by creating an instance of DataExtractor.
    """    

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
        Cleans the user data from the 'legacy_users' SQL table from the AI core provided, stored locally "sales data" database by processing addresses 
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
   

   def called_clean_store_data(self):

     """
    Cleans and standardizes store data extracted from the API, addressing formatting 
    and consistency issues in the 'continent' and 'opening_date' columns.

    This method:
    
    1. Extracts store data via the API using 'retrieve_stores_data' method.
    2. Corrects common errors in the 'continent' column.
    3. Filters data to include only valid continents ('America' and 'Europe').
    4. Parses the 'opening_date' column to ensure consistent date formatting.
    5. Removes erroneous or unnecessary columns, such as 'lat'.

    Returns:
        pd.DataFrame: A cleaned pandas DataFrame containing store data with consistent formatting.
     """
         
     #getting pd dataframe about stores data that was earlier obtained from the AI core api
     store_data=self.dt_extractor.retrieve_stores_data('https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{}',{'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'})
     
     #correcting common error, changing eeContinent to Continent
     store_data['continent']=store_data['continent'].str.replace('ee','',regex=False)
     
     #continets that store are present on
     store_continents=['America','Europe']

     #cleaning up continents, removing rows with incorrect name
     store_data=store_data[store_data['continent'].isin(store_continents)]

     #getting the date in correct format
     store_data['opening_date']=store_data['opening_date'].apply(self.parse_custom_dates)
     
     #dropping an erronous column
     store_data = store_data.drop('lat', axis=1)

     #optional save to excel file
     #store_data.to_excel('stores_data_cleaned.xlsx', index=False) 
    
     return store_data 
    
   def convert_product_weights(self,products):
     
     """
     Converts product weights from various units and formats into a standardized float format (kilograms).

     This method processes weights given in different formats and units, such as 'kg', 'g', 'ml', and 'oz', and 
     converts them into kilograms (kg) as float values. The function also handles expressions like 'a x b' by 
     multiplying the values, then applying the appropriate unit conversion. Invalid or malformed entries 
     are removed from the data.

     Args:
        products (pd.DataFrame): A DataFrame containing a 'weight' column with product weight data in various formats.

     Returns:
        pd.DataFrame: A pandas DataFrame with the 'weight' column standardized to float values in kilograms (kg).
    """
     
     #function that returns float from a string value, handles a x b input form and single values
     def convert_to_float(string_val):
        
        """
        Converts a string representation of product weight into a float value, handling both 'a x b' formats and single numeric values.

        This function processes weight strings that may appear in formats like 'a x b' (e.g., '2 x 500'), where it splits 
        the string, converts each component to a float, multiplies them, and returns the computed value. For single numeric 
        values, it directly converts the string to a float. Unit suffixes such as 'kg', 'g', 'ml', and 'oz' are stripped 
        before processing, as only numeric values are used in the computation.

        Args:
           string_val (str): The string representing the weight. It may be in the format 'a x b' or a single numeric value with an optional unit suffix.

        Returns:
           float_val (float): The computed weight in numeric form, based on the provided string. This is either the product of 'a x b' values or a direct conversion of a single numeric value. The output is always a float, regardless of the input format.
        """
       
        if " x " in string_val:
          
          # Remove any suffix (e.g., 'g') before splitting and converting
          string_val = string_val.rstrip("kgmlg")
          
          # Split and multiply if in "a x b" format
          num1, num2 = map(float, string_val.split(" x "))
          
          #number to be returned
          float_val=num1*num2
          
          return float_val
        
        else:

          #converting to float
          float_val=float(string_val)

        # Directly convert to float if it's a single number
          return float_val
     
     #removing . if it's the last character
     products['weight'] = products['weight'].apply(lambda x: str(x).rstrip('.').strip() if isinstance(x, str) else str(x))

     #getting the length of the column
     no_rows=products['weight'].count()
       
     i=0
     
     #intialising an list of products
     product_list=[]

     #digits tuple
     digits=('0','1','2','3','4','5','6','7','8','9')
     
     

     for item in products['weight']:
         # Ensure item is a string for consistent handling
         item = str(item)  
         
         if len(item) <2:

          #removing this faulty row
          products = products.drop(i)

          continue

         #if kg
         if(item[-2]=='k' and item[-1]=='g'):
           
           #saving each string value as float number, a x b expression is converted to product of multiplication
           #value is rounded to 3 decimal places and finally adding it to a list
           product_list.append(round(convert_to_float(item[:-2]),3))
       
         #if ml, ml==gram
         elif(item[-2]=='m' and item[-1]=='l'):

           #same conversion as above, but also converting from grams to kilograms
           product_list.append(round(0.001*convert_to_float(item[:-2]),3))
       
         #just the grams case
         elif(item[-2] in digits and item[-1]=='g'):
         
           product_list.append(round(0.001*convert_to_float(item[:-1]),3))

         #if oz, oz==28.35grams
         elif(item[-2]=='o' and item[-1]=='z'):

           product_list.append(round(0.001*28.35*convert_to_float(item[:-2]),3))
         #other case == invalid
         else:
         
           #removing this faulty row
           products = products.drop(i)
        
         i+=1

     products['weight']=product_list

     products['date_added']=products['date_added'].apply(self.parse_custom_dates)
     
     #optional 
     #products.to_excel('product_data_cleaned.xlsx', index=False)
     return products
   
   def clean_orders_data(self):
    
    """
    Retrieves order data from the local sales database and removes specified columns.

    This function fetches order data from the 'orders_table' using self.dt_extractor.read_rds_table.
    Furthemore it drops the columns 'first_name', 'last_name', and '1' if present to clean the data.

    Returns:
    
    order_data(pd.DataFrame): Cleaned order data with unnecessary columns removed.
    """
    #retring orders data from the AI core local sales data database and saving in pd datateframr
    order_data=self.dt_extractor.read_rds_table('orders_table') 
    
    #dropping erronous columns
    order_data=order_data.drop(columns=['first_name','last_name','1'], errors='ignore')
    
    #Optional save to excel
    #order_data.to_excel('order_data.xlsx', index=False)
    
    return order_data 

   def clean_date_events_data(self): 
     
     """
    Cleans date event data by filtering out rows with invalid 'month' values.

    This method:
    
    Extracts date event data from a JSON file on S3 using the extract_json_from_s3 method.
    Applies a filter to ensure that only rows with integer values in the 'month' column are retained.
    By saving the data to excel inspect the data and by further using chagpt to inspect the data, it was confirmed
    that if non-integer value exist in dateframe in a given row then it will also be non-integer in month column. Hence
    it is possible to filter based on month column alone to remove all erronous values. This function optionally saves the cleaned DataFrame to an Excel file for further review.

    Returns:
        pd.DataFrame: A cleaned DataFrame containing date event data with valid values.
     """
     
     # Extract date events data from the S3 JSON file in to pd dataframe
     date_events_data=self.dt_extractor.extract_json_from_s3()

     # Filter out rows where 'month' column can be safely converted to an integer
     def is_integer(value):
       
       """
        Determines if a given value can be safely converted to an integer.

        Args:
            value (Any): The value to check, typically a string or number.

        Returns:
            bool: True if the value can be converted to an integer, otherwise False.
       """

       try:

        int(value) # Attempt to convert to integer

        return True
       
       except ValueError:

        return False

     # Filter out rows where column 'month' has non-integer values
     date_events_data = date_events_data[date_events_data['month'].apply(is_integer)]
    
     #Optionally save the dataframe to excel
     #date_events_data.to_excel('filtered_date_details.xlsx', index=False)

     return date_events_data

cleaned=DataCleaning()

DBCon=DatabaseConnector()

#DBCon.upload_to_db('dim_users',cleaned.clean_user_data())

#DBCon.upload_to_db('dim_card_details',cleaned.clean_card_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf'))

#cleaned.called_clean_store_data()

#DBCon.upload_to_db('dim_store_details',cleaned.called_clean_store_data())
#Task 6
#DBCon.upload_to_db('dim_products',cleaned.convert_product_weights(cleaned.dt_extractor.extract_from_s3()))

#Task7
#table_list=DBCon.list_db_tables()

#print(table_list)

#cleaned.clean_orders_data()

#DBCon.upload_to_db('orders_table',cleaned.clean_orders_data())

#Task8
DBCon.upload_to_db('dim_date_times',cleaned.clean_date_events_data())


