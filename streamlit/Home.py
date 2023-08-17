import streamlit as st
import pandas as pd
from datetime import datetime
from snowflake.snowpark.session import Session

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
    
    return session

def get_data(sql_str: str, session) -> pd.DataFrame:   
    df = session.sql(sql_str).to_pandas()
    df = df.reset_index(drop = True)
    return df

def main():
    st.set_page_config(page_title="AV Visualizations App")

    # Title section
    st.title("Alphavantage ELT Project - Visualizations App")
    st.caption(f"Last updated: {TODAY_DATE}")
    st.caption("Author: Phillip Liu")
    st.caption("Please note that this app is by no means complete, the plan is to finish off the analytics engineering side of things first in DBT then propogate \
            the changes here.")

    # Overview section
    st.header("Overview")
    st.markdown(
        "This is a Streamlit application whose purpose is to visualize the data which I have captured in Snowflake and transformed with DBT \
        in a manner where you can derive insights about the sentiment of Bitcoin by different categories such as topic, date, etc. It is intended to be basic \
        as my primary focus has been on using Python, Snowflake, and DBT to nail down a solid ELT process. This is just the cherry on top to display the results \
        in a visual manner."
    )
    st.markdown(
        " \
        News sentiment data is extracted from AlphaVantage API. You can refer to the documentation [here](https://www.alphavantage.co/documentation/#news-sentiment).  \
        Extraction and loading has been done via Python and transformations have been done with DBT. The raw data extract below is an analytical DBT model, it is not the \
        raw data from the API.\
        "
    )

    # Scores section
    st.header("Scores")
    st.markdown(
        "You will find in the data a few *score* values which range from around -0.35 to 0.35. These scores reflect the sentiment of the attribute. \
        A description of the attributes is as follows:"
    )
    st.markdown(
        "\
            Let Sentiment score definition $= x$:\n\
            * $<= -0.35$ is **Bearish**\n\
            *  $-0.35 > x <= -0.15$ is **Somewhat Bearish**\n\
            * $-0.15 > x <= 0.15$ is **Neutral**\n\
            * $0.15 > x <= 0.35$ is **Somewhat Bullish**\n\
            * $x >= 0.35$ is **Bullish**\n\
        "
    )

    session = create_snowflake_session()
    df = get_data("SELECT * FROM MARTS.CORE.NEWS_SENTIMENT WHERE DATE_PUBLISHED > DATEADD(DAY, -14, DATE_PUBLISHED)", session)
    session.close()
    
    st.header("Raw data")
    st.markdown("Please click the button below to download the base data from Snowflake which was built with DBT and is represented as a core mart. \
                Data is limited to the last 14 days.")
    st.download_button(
        label = "Download raw data"
        , data = df.to_csv().encode('utf-8')
        , file_name = f"av_ns_data {TODAY_DATE}.csv"
        , mime = "text/csv"
    )

    # Contact section
    st.header("Contact")
    st.markdown("Please refer to my github for this project [here](https://github.com/pdiu/etl-project).")
    st.markdown("Any feedback is welcomed at phillipliuwr@gmail.com.")

if __name__ == "__main__":
    TODAY_DATE = datetime.today().strftime('%Y-%m-%d')
    main()