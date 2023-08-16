import streamlit as st
from datetime import datetime

st.set_page_config(page_title="AV Visualizations App")

# Title section
st.title("Alphavantage ELT Project - Visualizations App")
st.caption(f"Last updated: {datetime.today().strftime('%Y-%m-%d')}")
st.caption("Author: Phillip Liu")

# Overview section
st.header("Overview")
st.markdown(
    "This is a Streamlit application whose purpose is to visualize the data which I have captured in Snowflake and transformed with DBT \
    in a manner where you can derive insights about the sentiment of Bitcoin by different categories such as topic, date, etc."
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

# Contact section
st.header("Contact")
st.markdown("Please refer to my github for this project [here](https://github.com/pdiu/etl-project).")
st.markdown("Any feedback is welcomed at phillipliuwr@gmail.com.")
