import pandas as pd
import streamlit as st
import altair as alt
import pdb
import os
import logging
import json
import plotly.express as px
from PIL import Image
from snowflake.snowpark.session import Session

def get_snowflake_config() -> dict:
    """
    Retrieves snowflake config from config file
    """
    with open(f"{CONFIG_PATH}/snowflake.json") as config_file:
        config = json.load(config_file)
        
    return config

def create_snowflake_session() -> Session:
    """
    Create a snowflake session
    """
    account = st.secrets.snowflake.account_id
    user = st.secrets.snowflake.username
    password = st.secrets.snowflake.password
    warehouse = st.secrets.snowflake.warehouse
    role = st.secrets.snowflake.role
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
    logger.info(f"Retrieving data from snowflake. Query used:\n{sql_str}")
    
    df = session.sql(sql_str).to_pandas()
    df = df.reset_index(drop = True)
    return df
    
def create_bar_chart(df: pd.DataFrame, x: str, y: str, color:str = None) -> None:
    logger.info("Creating bar chart")
    
    fig = px.bar(
        df
        , x = x
        , y = y
        , color = color
        , barmode = "relative"
    )
    fig.update_layout(showlegend=False)
    
    return fig
    
    
def format_df_colnames(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.lower()
    df = df.rename(columns = lambda x: x.replace("_", " ").title())
    
    return df

def main():
    session = create_snowflake_session()
    df = get_data(topic_sentiment_sql, session)
    df = format_df_colnames(df)
    
    st.title("Alphavantage ELT Project - Visualizations App")
    st.header("Bitcoin News Sentiment")
    st.markdown(
        " \
        News sentiment data is extracted from AlphaVantage API. You can refer to the documentation [here](https://www.alphavantage.co/documentation/#news-sentiment).  \
        Extraction and loading has been done via Python and transformations have been done with DBT. The raw data extract below is an analytical DBT model, it is not the \
        raw data from the API.\
        "
    )

    st.subheader("Raw data")
    st.dataframe(df, hide_index = True)

    # st.subheader("Average ticker sentiment by date")
    # st.plotly_chart(create_bar_chart(df, x="Date Published", y="Avg Ticker Sentiment Score"), use_container_width=True)

    st.subheader("Average ticker sentiment by topic")
    st.plotly_chart(create_bar_chart(df, x="Topic", y="Avg Ticker Sentiment Score", color="Topic"), use_container_width=True)

    logger.info(f"Closing Snowflake session, {session}")
    session.close()

if __name__ == "__main__":
    # Global path variables
    PROJECT_PATH = os.getcwd()
    CONFIG_PATH = f"{PROJECT_PATH}/config"
    LOG_PATH = f"{PROJECT_PATH}/logs"
    SQL_ANALYSIS_PATH = f"{PROJECT_PATH}/sql/analysis"
    IMAGE_PATH = f"{PROJECT_PATH}/images"
    
    # Initialize logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(f"{LOG_PATH}/streamlit.log")
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    
    # SQL Queries to visualize
    with open (f"{SQL_ANALYSIS_PATH}/topic_sentiment.sql", "r") as sql_file:
        topic_sentiment_sql  = sql_file.read()

    with open (f"{SQL_ANALYSIS_PATH}/topic_sentiment.sql", "r") as sql_file:
        daily_sentiment_sql  = sql_file.read()

    main()