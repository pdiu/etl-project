import logging
import os
import json
import requests
from datetime import date, timedelta, datetime
import pandas as pd
from prefect import flow, task
import pdb
from snowflake.snowpark.session import Session
from snowflake.connector.pandas_tools import write_pandas

def get_api_key(config_name:str) -> str:
    """
    Retrieves API key from config file
    """
    with open(f"{CONFIG_PATH}\secrets.json") as config_file:
        data = json.load(config_file)

    for config in data:
        if config["name"] == config_name:
            api_key = config["api_key"]
            return api_key
    
    return None

def get_snowflake_config() -> dict:
    """
    Retrieves snowflake config from config file
    """
    with open(f"{CONFIG_PATH}\snowflake.json") as config_file:
        config = json.load(config_file)
        
    return config

@task()
def get_sentinment_data(ticker_type: str, ticker: str) -> pd.DataFrame:
    """
    EXTRACT
    Makes the API call to Alpha Vantage to retrieve data. The data we are retrieving is non-dynamic, in the sense
    that we specifically want news sentiment for bitcoin from yesterday T0000 till now with a 1000 response item limit
    """
    time_from = f"{(date.today() - timedelta(days=7)).strftime('%Y%m%d')}T0000"
    
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

@task
def create_snowflake_session() -> Session:
    """
    Create a snowflake session
    """
    account = SNOWFLAKE_CONFIG["account_id"]
    user = SNOWFLAKE_CONFIG["username"]
    password = SNOWFLAKE_CONFIG["password"]
    warehouse = SNOWFLAKE_CONFIG["warehouse"]
    role = SNOWFLAKE_CONFIG["role"]
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

@task()
def push_raw_data_to_snowflake(session, df: pd.DataFrame, schema: str, table_name: str) -> None:
    """
    Write in append mode to provided snowflake schema and table, database is defined in the snowflake.json file
    """
    session.use_database("raw")
    
    logger.info(f"Upserting data into {session.get_current_database()}.{session.get_current_schema()}.{table_name}")
    
    session.write_pandas(
        df = df
        , database = "raw"
        , schema = schema
        , table_name = table_name
        , quote_identifiers = False
    )
    
    return None

@flow()
def elt_flow() -> None:
    """
    ELT orchestrator. Master flow
    """
    logger.info("Running elt_flow()...")
    
    # Retrieve Bitcoin news sentiment from Alpha Vantage API
    df = get_sentinment_data("CRYPTO", "BTC")
    
    # Create Snowpark connection session to Snowflake
    session = create_snowflake_session()
    
    # Upsert raw data into Snowflake
    push_raw_data_to_snowflake(session, df, "ALPHAVANTAGE", "NEWS_SENTIMENT")
    
    # Close session
    logger.info(f"Closing Snowflake session, {session}")
    session.close()

    logger.info("ELT pipeline ran successfully with no errors!")

if __name__ == "__main__":
    # Global path variables
    PROJECT_PATH = os.getcwd()
    DATA_PATH = f"{PROJECT_PATH}\\data"
    CONFIG_PATH = f"{PROJECT_PATH}\\config"
    LOG_PATH = f"{PROJECT_PATH}\\logs"

    # Global API variables
    ALPHA_VANTAGE_API_URL = "https://www.alphavantage.co/query"
    API_KEY = get_api_key("Alpha Vantage")
    
    # Get configurations
    SNOWFLAKE_CONFIG = get_snowflake_config()
    
    # Initialize logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(f"{LOG_PATH}\\logfile.log")
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    # Call to main function
    elt_flow()