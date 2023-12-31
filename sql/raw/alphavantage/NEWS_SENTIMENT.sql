CREATE SCHEMA IF NOT EXISTS RAW.ALPHAVANTAGE;

CREATE TABLE IF NOT EXISTS RAW.ALPHAVANTAGE.NEWS_SENTIMENT(
    TITLE TEXT
    , URL TEXT
    , TIME_PUBLISHED TEXT
    , AUTHORS TEXT
    , SUMMARY TEXT
    , BANNER_IMAGE TEXT
    , SOURCE TEXT
    , CATEGORY_WITHIN_SOURCE TEXT
    , SOURCE_DOMAIN TEXT
    , TOPICS TEXT
    , OVERALL_SENTIMENT_SCORE TEXT
    , OVERALL_SENTIMENT_LABEL TEXT
    , TICKER_SENTIMENT TEXT
    , INSERT_TIMESTAMP TEXT
);
