"""
What I want to achieve from this:
- Create a data pipeline utilizing cloud (GCP)
- Use Prefect as the orchestration tool
- Create a Streamlit interactive dashboard for the data.

"""
import os
import json
import requests
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
# from prefect.tasks import task_input_hash
import pdb
# import streamlit as st

def etl_flow() -> None:
    """
    Calls all related tasks to the ETL flow.
    """
    df = get_sentinment_data()
    print(df.head())

def get_sentinment_data() -> pd.DataFrame:
    url = f"{ALPHA_VANTAGE_API_URL}?function=NEWS_SENTIMENT&tickers=CRYPTO:BTC&apikey={API_KEY}"
    r = requests.get(url)
    data = r.json()
    df = pd.DataFrame(data)
    return df

def retrieve_api_key(secret_id:str) -> str:
    with open(f"{CONFIG_PATH}\secrets.json") as config_file:
        data = json.load(config_file)

    for config in data:
        if config["name"] == secret_id:
            api_key = config["api_key"]
            return api_key
    
    return None

@task()
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic dataframe clean.
    """
    df.drop(df.columns[0], axis=1, inplace=True)
    # Data record/instance must contain mileage information
    df.dropna(subset=["mileage_in_km"], inplace=True)
    return df

@task()
def save_data_locally(df:pd.DataFrame) -> str:
    # Save file, overwrite if exists
    save_path = f"{DATA_PATH}\processed_data.csv"
    df.to_csv(save_path, mode='w', index=False)
    return save_path

@task()
def write_data_to_gcs(file_path: str) -> None:
    """
    Utilize prefect GCP block and library to upload local data file to GCP storage.
    """
    gcp_storage_block = GcsBucket.load("etl-proj-gcsbucket-block")
    gcp_storage_block.upload_from_path(
        from_path = file_path
        , to_path = "data/data.csv"
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