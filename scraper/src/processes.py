
import pandas as pd
import scrapy
# from scrapy.crawler import CrawlerProcess
# from src.policy_scraper.policy_scraper.spiders.keyword_spider import KeywordSpider
from src.constants.scraper_constants import SCRAPER_JSON_PATH
import logging
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import OperationalError


# import psycopg2
# from policy_scraper.policy_scraper.utils import get_project_settings

logger = logging.getLogger(__name__)


def init_grafana_pg_engine(
        database="my_grafana_db",
        user="my_grafana_user",
        password="my_grafana_pwd",
        host="pg_grafana",
        port=5432,
):
    """ Initialize connection to the PostgreSQL database using SQLAlchemy. """
    
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


def write_exec_time_json_to_postgres(engine,
                           table,
                           schema = None):

        # Read JSON file into a DataFrame
        df = pd.read_json(SCRAPER_JSON_PATH, lines = True)
        df = df.set_index("timestamp")
        df = df.tz_localize(tz = "Europe/Tallinn")
         #df = df.reset_index()

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



# def transform_json_and_save_to_postgres():

#     df = pd.read_json(
#         SCRAPER_JSON_PATH
#     )

#     write_df_to_postgres(
#         database="my_grafana_db",
#         user="my_grafana_user",
#         password="my_grafana_pwd",
#         host="pg_grafana",
#         port=5432,
#         schema = "scraping_analysis"
#     )

#     print("Transforming json and saving to postgres")
#     pass

    

# def init_grafana_pg_conn(
#         database="my_grafana_db",
#         user="my_grafana_user",
#         password="my_grafana_pwd",
#         host="pg_grafana",
#         port=5432,
# ):
#     """ Initialize connection to the Graphana PostgreSQL database. """
    
#     conn = psycopg2.connect(database=database, 
#                             user=user, password=password, host=host, port=port)
    
#     return conn

# def check_schema_and_table_existance(conn,
#                                      table, 
#                                      schema):
    
#     cursor = conn.cursor()

#     try:
#         # Check if the schema exists
#         cursor.execute("SELECT EXISTS(SELECT 1 FROM pg_namespace WHERE nspname = %s)", (schema,))
#         schema_exists = cursor.fetchone()[0]

#         if not schema_exists:
#             print(f"Schema '{schema}' does not exist.")
#             return

#         # Check if the table exists
#         cursor.execute("""
#             SELECT EXISTS (
#                 SELECT 1
#                 FROM information_schema.tables
#                 WHERE table_schema = %s AND table_name = %s
#             )
#         """, (schema, table))
#         table_exists = cursor.fetchone()[0]

#         if not table_exists:
#             print(f"Table '{table}' does not exist.")
#             return
    
#     except Exception as e:
#         print(f"An error occurred: {e}")

#     finally:
#         # Closing the cursor and connection
#         cursor.close()
#         conn.close()
# from sqlalchemy import create_engine, MetaData, Table

# def check_schema_and_table_existance(engine, table_name, schema_name):
#     try:
#         # Reflecting the metadata
#         metadata = MetaData(engine)
#         metadata.reflect()

#         # Check if the schema exists
#         schema_exists = engine.dialect.has_schema(engine, schema_name)
#         if not schema_exists:
#             print(f"Schema '{schema_name}' does not exist.")
#             return

#         # Check if the table exists
#         table_exists = table_name in metadata.tables
#         if not table_exists:
#             print(f"Table '{table_name}' does not exist.")
#             return

#     except Exception as e:
#         print(f"An error occurred: {e}")

#     finally:
#         # Disposing the engine
#         engine.dispose()
  
# Works with pandas==2.2.0


# def create_table_if_not_exists(conn, 
#                                schema = {'a': 'INTEGER', 'b': 'INTEGER'}, 
#                                table = "STATS", 
#                                columns = ["a", "b"]):
#     try:
#         # Establishing connection to the PostgreSQL database
#         # conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
#         cursor = conn.cursor()

#         # Check if the schema exists, if not, create it
#         cursor.execute("CREATE SCHEMA IF NOT EXISTS {};".format(schema))

#         # Check if the table exists
#         cursor.execute("""
#             SELECT EXISTS (
#                 SELECT 1
#                 FROM information_schema.tables
#                 WHERE table_schema = %s AND table_name = %s
#             )
#         """, (schema, table))
#         table_exists = cursor.fetchone()[0]

#         # If the table doesn't exist, create it
#         if not table_exists:
#             columns_str = ', '.join([f"{column} {columns[column]}" for column in columns])
#             create_table_query = f"CREATE TABLE {schema}.{table} ({columns_str})"
#             cursor.execute(create_table_query)
#             print(f"Table '{table}' has been created.")

#         else:
#             print(f"Table '{table}' already exists.")

#         # Committing the changes and closing the connection
#         conn.commit()

#     except Exception as e:
#         print(f"An error occurred: {e}")

#     finally:
#         # Closing the cursor and connection
#         cursor.close()
#         conn.close()


# def scrap_data_from_web_and_store_as_json():
#     # print("Scapping data from web and storing as json")
#     logger.info("Scraping data from web and storing as json")
#     print("Here")
#     process = CrawlerProcess(
#         settings={
#             "FEEDS": {
#                 "items.json": {"format": "json"},
#             },
#         }
#     )

#     # print(process)

#     try:
#         process.crawl(KeywordSpider)
#         process.start() 
#     except Exception as e:
#         print("An error occurred while crawling: {e}")
#         logger.error(f"An error occurred while crawling: {e}")

#     logger.info("Finished scraping")

#     return "Finished scraping"