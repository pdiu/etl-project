import pandas as pd
import streamlit as st
import altair as alt
import pdb
import os
import logging
import json
from snowflake.snowpark.session import Session

def get_snowflake_config() -> dict:
    """
    Retrieves snowflake config from config file
    """
    with open(f"{CONFIG_PATH}\snowflake.json") as config_file:
        config = json.load(config_file)
        
    return config

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

def get_data(sql_str: str, session) -> pd.DataFrame:
    logging.info(f"Retrieving data from snowflake. Query used:\n{sql_str}")
    
    df = session.sql(sql_str).to_pandas()
    df = df.reset_index(drop = True)
    return df

def create_bar_chart(df: pd.DataFrame, x: str, y: str, legend:str = None) -> None:
    logging.info(f"Creating bar chart")
    if legend is not None:
        bar_chart = alt.Chart(df).mark_bar().encode(
            x = x
            , y = y
            , color = legend
        ).interactive()
    else:
        bar_chart = alt.Chart(df).mark_bar().encode(
            x = x
            , y = y
        ).interactive()
        
    st.altair_chart(bar_chart, use_container_width=True)
    
def format_df_colnames(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.lower()
    df = df.rename(columns = lambda x: x.replace("_", " ").title())
    
    return df

def main():
    st.title("Alphavantage ELT Project - Visualizations App")
    st.header("Bitcoin News Sentiment")
    
    session = create_snowflake_session()
    df = get_data(SENTIMENT_SQL, session)
    df = format_df_colnames(df)
    
    st.subheader("Raw data")
    st.dataframe(df, hide_index = True)
    
    st.subheader("Average ticker sentiment by date")
    create_bar_chart(df = df, x="Date Published", y = "Avg Ticker Sentiment Score")
    
    st.subheader("Average ticker sentiment by topic")
    create_bar_chart(df = df, x = "Topic", y = "Avg Ticker Sentiment Score")
    
    logger.info(f"Closing Snowflake session, {session}")
    session.close()

if __name__ == "__main__":
    # Global path variables
    PROJECT_PATH = os.getcwd()
    CONFIG_PATH = f"{PROJECT_PATH}\\config"
    LOG_PATH = f"{PROJECT_PATH}\\logs"
    SQL_ANALYSIS_PATH = f"{PROJECT_PATH}\\sql\\analysis"
    
    # Get configurations
    SNOWFLAKE_CONFIG = get_snowflake_config()
    
    # Initialize logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(f"{LOG_PATH}\\streamlit.log")
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    
    # SQL Queries
    with open (f"{SQL_ANALYSIS_PATH}\\sentiment.sql", "r") as sql_file:
        SENTIMENT_SQL  = sql_file.read()

    main()