import pandas as pd
from sqlalchemy import create_engine

def test_postgres_connection(host, port, database, user, password):
    # Construct the database URL
    db_url = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    
    try:
        # Create a SQLAlchemy engine
        engine = create_engine(db_url)
        
        # Test the connection by executing a simple SQL query
        pd.read_sql_query('SELECT 1', con=engine)
        
        # If the query executed successfully, print connection success
        print("Connection to PostgreSQL successful!")
    except Exception as e:
        # If there was an error, print connection failure and the error message
        print("Connection to PostgreSQL failed:", e)

# Replace these values with your PostgreSQL server details
host = 'your_host'
port = 'your_port'
database = 'your_database'
user = 'your_username'
password = 'your_password'

# Call the function to test the connection
test_postgres_connection(host, port, database, user, password)