"""
What I want to achieve from this:
- Create a data pipeline utilizing cloud (GCP)
- Use Prefect as the orchestration tool
- Create a Streamlit interactive dashboard for the data.

"""
import os
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
# from prefect.tasks import task_input_hash
import pdb
# import streamlit as st

@flow()
def etl_flow() -> None:
    """
    Calls all related tasks to the ETL flow.
    """
    # Read data file
    data_file = f"{DATA_DIR}\data.csv"
    df = pd.read_csv(data_file)

    # Clean df
    clean_df = clean_data(df)

    # Save cleaned df
    saved_data_dir = save_data_locally(clean_df)

    # Upload data to GCP storage bucket
    ## Ensure your Prefect GCS block and credentials is configured.
    write_data_to_gcs(saved_data_dir)

@task()
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df.drop(df.columns[0], axis=1, inplace=True)
    # Data record/instance must contain mileage information
    df.dropna(subset=["mileage_in_km"], inplace=True)
    return df

@task()
def save_data_locally(df:pd.DataFrame) -> str:
    # Save file, overwrite if exists
    save_path = f"{DATA_DIR}\processed_data.csv"
    df.to_csv(save_path, mode='w', index=False)
    return save_path

@task()
def write_data_to_gcs(file_path: str) -> None:
    gcp_storage_block = GcsBucket.load("etl-proj-gcsbucket-block")
    gcp_storage_block.upload_from_path(
        from_path = file_path
        , to_path = "data/data.csv"
    )
    return

if __name__ == "__main__":
    # Setting global variables
    PROJECT_DIR = os.getcwd()
    DATA_DIR = f"{PROJECT_DIR}\data"

    # Call to main function
    etl_flow()