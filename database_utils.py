import yaml

class DatabaseConnector:

    '''
    Manages connections to online and local PostgreSQL databases and provides 
    methods to list tables and upload data to the database.
    '''
    

    def __init__(self)-> None:
        
        '''
        Initializes the DatabaseConnector class by setting up the local database engine.
        '''

        self.local_engine=None
        self.init_db_engine()

    def read_db_creds(self,path):

        '''
        Retrieves yaml credentials of online db and returns them as dictionary.
        Args:
        path (str): The local file path where yaml file with database credentials is saved. 

        Returns:
           credentials dict(str): stores RDS_HOST, RDS_PASSWORD, RDS_USER ,RDS_DATABASE
           RDS_PORT
        '''

        with open(path,'r') as stream:
            credentials=yaml.safe_load(stream)

        return credentials    
    
    def init_db_engine(self):

        '''
        Initializes and returns an SQLAlchemy engine for both the online and local PostgreSQL databases.

        Returns:
           engine (sqlalchemy.engine.Engine): The SQLAlchemy engine for the online PostgreSQL database.
        '''

        credentials=self.read_db_creds(r'C:\Users\micha\multinational-retail-data-centralisation\multinational-retail-data-centralisation\db_creds.yaml') #dictionary that containing sql-alchemy login data
        
        #engine from the online db to extract data from
        from sqlalchemy import create_engine
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = credentials['RDS_HOST']
        USER = credentials['RDS_USER']
        PASSWORD = credentials['RDS_PASSWORD']
        DATABASE = credentials['RDS_DATABASE']
        PORT = credentials['RDS_PORT']
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        
        #engine to store data on local database
        
        local_credentials=self.read_db_creds(r'C:\Users\micha\multinational-retail-data-centralisation\multinational-retail-data-centralisation\local_creds.yaml') #dictionary that containing sql-alchemy login data

        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = local_credentials['RDS_HOST']
        USER = local_credentials['RDS_USER']
        PASSWORD = local_credentials['RDS_PASSWORD']
        DATABASE = local_credentials['RDS_PORT']
        PORT = local_credentials['RDS_PORT']
        self.local_engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        
        return engine
    
    def list_db_tables(self):

        '''
        Retrieves and prints the table names from the database engine and returns them as a list.

        Returns:
           list: A list of table names (str) available in the database.
        '''

        engine=self.init_db_engine() #intialise

        from sqlalchemy import inspect

        table_list = inspect(engine).get_table_names()

        print('The table names in the db are:',*table_list)

        return table_list

    def upload_to_db(self,table_name,table_data_frame):
        

        '''
        Uploads a pandas DataFrame to the specified table in the local PostgreSQL database.

        Args:
          table_name (str): The name of the table to upload the DataFrame into.
          table_data_frame (pd.DataFrame): The pandas DataFrame containing the data to be uploaded.
        '''

        table_data_frame.to_sql(table_name, self.local_engine, if_exists='replace', index=False)








        





