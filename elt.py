import logging
import os
import json
import requests
from datetime import date, timedelta, datetime
import pandas as pd
from dotenv import load_dotenv
import pdb
from snowflake.snowpark.session import Session
from snowflake.connector.pandas_tools import write_pandas

def get_config(config_name:str) -> str:
    """
    Retrieves API key from config file
    """
    return os.getenv(config_name)

def get_sentinment_data(ticker_type: str, ticker: str) -> pd.DataFrame:
    """
    EXTRACT
    Makes the API call to Alpha Vantage to retrieve data. The data we are retrieving is non-dynamic, in the sense
    that we specifically want news sentiment for bitcoin from yesterday T0000 till now with a 1000 response item limit
    """
    time_from = f"{(date.today() - timedelta(days=1)).strftime('%Y%m%d')}T0000"
    
    logger.info("Running get_sentiment_data()...")
    logger.info(f"Getting data from {time_from} to now")
    
    ticker = f"{ticker_type.upper()}:{ticker.upper()}"
    url = f"{ALPHA_VANTAGE_API_URL}?function=NEWS_SENTIMENT&tickers={ticker}&time_from={time_from}&limit=1000&apikey={API_KEY}"
    r = requests.get(url)
    data = r.json()
    df = pd.DataFrame(data["feed"])
    
    # Inserting extra metadata
    df["insert_timestamp"] = pd.Timestamp("now").strftime("%Y-%m-%d %H:%M:%S")

    logger.info(f"Retrieved {df.shape[0]} row(s) of data")
    logger.info("Completed get_sentiment_data()...")
    
    return df

def create_snowflake_session() -> Session:
    """
    Create a snowflake session
    """
    account = os.getenv("SNOWFLAKE_ACCOUNT_ID")
    user = os.getenv("SNOWFLAKE_ACCOUNT_USER")
    password = os.getenv("SNOWFLAKE_ACCOUNT_PASSWORD")
    warehouse = os.getenv("SNOWFLAKE_ACCOUNT_WAREHOUSE")
    role = os.getenv("SNOWFLAKE_ACCOUNT_ROLE")
    connection_params = {
        "account": account
        , "user": user
        , "password": password
        , "warehouse": warehouse
        , "role": role
    }
    session = Session.builder.configs(connection_params).create()
    
    logger.info(f"Creating Snowflake session, {session}")
    return session

def push_raw_data_to_snowflake(session, df: pd.DataFrame, schema: str, table_name: str) -> None:
    """
    LOAD
    Write in append mode to provided snowflake schema and table
    """
    session.use_database("raw")
    session.write_pandas(
        df = df
        , database = "raw"
        , schema = schema
        , table_name = table_name
        , quote_identifiers = False
    )
    
    logger.info(f"Upserting data into {session.get_current_database()}.{schema}.{table_name}")
    
    return None

def elt_flow() -> None:
    """
    ELT orchestrator. Master flow
    """
    logger.info("Running ELT pipeline...")
    
    # Retrieve Bitcoin news sentiment from Alpha Vantage API
    df = get_sentinment_data("CRYPTO", "BTC")
    print(df)
    
    # # Create Snowpark connection session to Snowflake
    # session = create_snowflake_session()
    
    # # Upsert raw news sentiment data into Snowflake
    # push_raw_data_to_snowflake(session, df, "ALPHAVANTAGE", "NEWS_SENTIMENT")
    
    # # Close session
    # logger.info(f"Closing Snowflake session, {session}")
    # session.close()

    # logger.info("Extract and load ran successfully with no errors!")

if __name__ == "__main__":
    load_dotenv()

    # Global path variables
    PROJECT_PATH = os.getcwd()
    DATA_PATH = f"{PROJECT_PATH}\\data"
    CONFIG_PATH = f"{PROJECT_PATH}\\config"
    LOG_PATH = f"{PROJECT_PATH}\\logs"

    # Global API variables
    ALPHA_VANTAGE_API_URL = "https://www.alphavantage.co/query"
    API_KEY = get_config("ALPHA_VANTTAGE_API_KEY")
    
    # Initialize logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(f"{LOG_PATH}\\logfile.log")
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    # Call to main function
    elt_flow()