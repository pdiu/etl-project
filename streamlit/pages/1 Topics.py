import pandas as pd
import streamlit as st
import pdb
import os
import logging
import json
import plotly.express as px
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
    logger.info(f"Retrieving data from snowflake")
    
    df = session.sql(sql_str).to_pandas()
    df = df.reset_index(drop = True)
    
    logger.info(f"Retrieved {df.shape[0]} row(s) of data")
    return df
    
def create_bar_chart(df: pd.DataFrame, x: str, y: str, color:str = None) -> None:
    logger.info(f"Creating bar chart x-axis({x}), y-axis({y}), legend({color})")
    
    fig = px.bar(
        df
        , x = x
        , y = y
        , color = color
        , barmode = "relative"
    )
    fig.update_layout(showlegend=False)
    
    return fig
    
def create_line_chart(df: pd.DataFrame, x: str, y: str, color:str = None) -> None:
    logger.info(f"Creating bar chart x-axis({x}), y-axis({y}), legend({color})")
    
    fig = px.line(
        df
        , x = x
        , y = y
        , color = color
    )
    
    return fig
    
def format_df_colnames(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.lower()
    df = df.rename(columns = lambda x: x.replace("_", " ").title())
    
    return df

def main():
    # Create sesseion
    session = create_snowflake_session()
    
    # Get data
    topic_sentiment_df = get_data(topic_sentiment_sql, session)
    topic_sentiment_df = format_df_colnames(topic_sentiment_df)
    
    topic_date_count_df = get_data(topic_date_count_sql, session)
    topic_date_count_df = format_df_colnames(topic_date_count_df)

    st.header("Topics Sentiment")
    st.markdown("This page displays insights on Bitcoin news. Please see a series of graphs below and their descriptions for reference to the insights.")
    
    st.subheader("Articles published by date")
    st.plotly_chart(create_line_chart(topic_date_count_df, x="Date Published", y="Articles Published", color="Topic"), use_container_width=True)

    st.subheader("Average overall sentiment score by topic")
    st.plotly_chart(create_bar_chart(topic_sentiment_df, x="Topic", y="Avg Overall Sentiment Score", color="Topic"), use_container_width=True)
    
    st.subheader("Average ticker sentiment label by topic")
    st.plotly_chart(create_bar_chart(topic_sentiment_df, x="Topic", y="Avg Ticker Sentiment Score", color="Topic"), use_container_width=True)

    logger.info(f"losing Snowflake session, {session}")
    session.close()

if __name__ == "__main__":
    # Global path variables
    STREAMLIT_PATH = os.path.join(os.path.dirname(__file__), "..")
    PROJECT_PATH = os.path.join(os.path.dirname(__file__), "../..")
    CONFIG_PATH = f"{PROJECT_PATH}/config"
    LOG_PATH = f"{PROJECT_PATH}/logs"
    
    SQL_ANALYSIS_PATH = f"{PROJECT_PATH}/sql/analysis"
    
    # Initialize logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(f"{LOG_PATH}/streamlit.log")
    log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    
    # SQL Queries to visualize
    topic_sentiment_sql = open(f"{SQL_ANALYSIS_PATH}/topic_sentiment.sql", "r").read()
    topic_date_count_sql = open(f"{SQL_ANALYSIS_PATH}/topic_date_count.sql", "r").read()
    main()