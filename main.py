import os
import json
import requests
from datetime import date, timedelta, datetime
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
import pdb
# import streamlit as st

def etl_flow() -> None:
    """
    Description: ELT orchestrator
    """

    current_date = datetime.now().date()
    yesterday_formatted_time = f"{(date.today() - timedelta(days=1)).strftime('%Y%m%d')}T0000"
    
    # Retrieve data from Alpha Vantage API
    df = get_sentinment_data(yesterday_formatted_time)

    # Save data locally as csv file
    saved_file_path = save_data_locally(df, current_date, "csv")

    # Upload data to GCS bucket, pre-configured in Prefect GCP storage block
    write_data_to_gcs(saved_file_path)

def get_sentinment_data(time_from: str) -> pd.DataFrame:
    url = f"{ALPHA_VANTAGE_API_URL}?function=NEWS_SENTIMENT&tickers=CRYPTO:BTC&time_from={time_from}&limit=500&apikey={API_KEY}"
    r = requests.get(url)
    data = r.json()
    df = pd.DataFrame(data["feed"])

    return df

def retrieve_api_key(config_name:str) -> str:
    with open(f"{CONFIG_PATH}\secrets.json") as config_file:
        data = json.load(config_file)

    for config in data:
        if config["name"] == config_name:
            api_key = config["api_key"]
            return api_key
    
    return None

def save_data_locally(df:pd.DataFrame, date: str, file_type: str) -> str:
    save_path = f"{DATA_PATH}\{date}\sentiment-data.csv"
    if not os.path.exists(f"{DATA_PATH}\{date}"):
        os.makedirs(f"{DATA_PATH}\{date}")

    if file_type == "csv":  
        df.to_csv(save_path, mode='w', index=False)
    elif file_type == "parquet":
        df.to_parquet(save_path, mode='w', index=False)
    
    return save_path

def write_data_to_gcs(file_path: str) -> None:
    """
    Utilize prefect GCP block and library to upload local data file to GCP storage.
    """
    gcp_storage_block = GcsBucket.load("etl-proj-gcsbucket-block")
    gcp_storage_block.upload_from_path(
        from_path = file_path
        , to_path = os.path.relpath(file_path, os.getcwd()).replace("\\", "/")
    )

    return

if __name__ == "__main__":
    # Global path variables
    PROJECT_PATH = os.getcwd()
    DATA_PATH = f"{PROJECT_PATH}\data"
    CONFIG_PATH = f"{PROJECT_PATH}\config"

    # Global API variables
    ALPHA_VANTAGE_API_URL = "https://www.alphavantage.co/query"
    API_KEY = retrieve_api_key("Alpha Vantage")

    # Call to main function
    etl_flow()