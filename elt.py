import logging
import os
import json
import requests
from datetime import date, timedelta, datetime
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
import pdb
# import streamlit as st

@task()
def get_sentinment_data(time_from: str) -> pd.DataFrame:
    """
    EXTRACT
    Makes the API call to Alpha Vantage to retrieve data. The data we are retrieving is non-dynamic, in the sense
    that we specifically want news sentiment for bitcoin from yesterday T0000 till now with a 500 response item limit
    """
    logger.info("Running get_sentiment_data()...")
    
    function = "NEWS_SENTIMENT"
    tickers = "CRYPTO:BTC"
    url = f"{ALPHA_VANTAGE_API_URL}?function={function}&tickers={tickers}&time_from={time_from}&limit=500&apikey={API_KEY}"
    r = requests.get(url)
    data = r.json()
    df = pd.DataFrame(data["feed"])

    logger.info("Completed get_sentiment_data()...")
    
    return df

def retrieve_api_key(config_name:str) -> str:
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

@task()
def save_data_locally(df:pd.DataFrame, date: str, file_type: str) -> str:
    """
    Save API data locally. Has the ability to save as different file types as specified
    in the function arguments.
    """

    save_path = f"{DATA_PATH}\{date}\sentiment-data.csv"

    # Create directory locally if it does not exist
    if not os.path.exists(f"{DATA_PATH}\{date}"):
        os.makedirs(f"{DATA_PATH}\{date}")

    # Save file based on specified file type to save as
    if file_type == "csv":  
        df.to_csv(save_path, mode='w', index=False)
    elif file_type == "parquet":
        df.to_parquet(save_path, mode='w', index=False)
    
    return save_path

@task()
def write_data_to_gcs(file_path: str) -> None:
    """
    LOAD
    Utilize prefect GCP block and library to upload local data file to GCP storage.
    """

    gcp_storage_block = GcsBucket.load("etl-proj-gcsbucket-block")
    gcp_storage_block.upload_from_path(
        from_path = file_path
        , to_path = os.path.relpath(file_path, os.getcwd()).replace("\\", "/")
    )

    return

@flow()
def elt_flow() -> None:
    """
    ELT orchestrator
    """
    logger.info("Running elt_flow()...")
    current_date = datetime.now().date()
    yesterday_formatted_time = f"{(date.today() - timedelta(days=1)).strftime('%Y%m%d')}T0000"
    
    logger.info(f"Getting data from {yesterday_formatted_time} to now")
    # Retrieve data from Alpha Vantage API
    df = get_sentinment_data(yesterday_formatted_time)

    # Save data locally as csv file
    # saved_file_path = save_data_locally(df, current_date, "csv")

    # Upload data to GCS bucket, pre-configured in Prefect GCP storage block
    # write_data_to_gcs(saved_file_path)
    logger.info("Completed elt_flow()...")

if __name__ == "__main__":
    # Global path variables
    PROJECT_PATH = os.getcwd()
    DATA_PATH = f"{PROJECT_PATH}\\data"
    CONFIG_PATH = f"{PROJECT_PATH}\\config"
    LOG_PATH = f"{PROJECT_PATH}\\logs"

    # Global API variables
    ALPHA_VANTAGE_API_URL = "https://www.alphavantage.co/query"
    API_KEY = retrieve_api_key("Alpha Vantage")
    
    # Initialize logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(f"{LOG_PATH}\\logfile.log")
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    # Call to main function
    elt_flow()