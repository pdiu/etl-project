select
    date_published
    , topic
    , avg(topic_relevance_score) as avg_topic_relevance_score
    , avg(overall_sentiment_score) as avg_overall_sentiment_score
    , avg(ticker_sentiment_score) as avg_ticker_sentiment_score
from marts.core.news_sentiment
group by 1, 2
order by 1 desc, 2