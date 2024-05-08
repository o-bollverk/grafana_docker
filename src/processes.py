
import logging

import pandas as pd
import scrapy

from src.constants.scraper_constants import SCRAPER_JSON_PATH

import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import OperationalError

logger = logging.getLogger(__name__)

def init_grafana_pg_engine(
        database: str,
        user:str,
        password:str,
        host: str,
        port:str,
):
    """ Initializes connection to the PostgreSQL database using SQLAlchemy. """
    
    try:
        # Constructing the connection URL
        #engine = create_engine('postgresql+psycopg2://root:1234567@localhost/mydatabase')
        #db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        
        db_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"

        # Creating the SQLAlchemy engine
        engine = create_engine(db_url)
        
        # Testing the connection by executing a raw SQL query
        engine.execute("SELECT 1")
        
        print("Connection to PostgreSQL database successful")
        
        return engine
    except OperationalError as e:
        print(f"Error: {e}")
        return None


def write_exec_time_json_to_postgres(engine: sqlalchemy.engine,
                           table: str,
                           schema = None):
        """
        Writes the scraped data from the JSON file to the PostgreSQL database.
        Reads json with pandas, converts to UTC.
        """

        if not SCRAPER_JSON_PATH.exists():
             logger.warning("No file found for this hour. Not writing to database.")
             return "No file found for this hour. Not writing to database."

        else:  
            # Read JSON file into a DataFrame
            df = pd.read_json(SCRAPER_JSON_PATH, lines = True)
            df = df.set_index("timestamp")
            df = df.tz_localize(tz = "UTC")

            # Store DataFrame into PostgreSQL table
            # Execute SQL string to insert data
            
            # TODO improve performance
            insert_data_sql = f"""
                INSERT INTO {schema}.{table} (term, incidence, site, timestamp) VALUES (%s, %s, %s, %s);
            """
            with engine.connect() as conn:
                for index, row in df.iterrows():
                    conn.execute(insert_data_sql, (row['term'], row['incidence'], row['site'], index))
            
            # TODO doesn't seem to be compatible with airflow version and sqlalchemy version
            # with conn.connect() as connection:
            #     df.to_sql(table, connection.connection, schema=schema, if_exists='append', index=False)

            logger.info(f'{SCRAPER_JSON_PATH} uploaded to database')

