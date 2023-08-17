select
   source
   , date_published
   , count(source) as count
   , avg(overall_sentiment_score) as avg_overall_sentiment_score
   , avg(ticker_relevance_score) as avg_ticker_relevance_score
   , avg(ticker_sentiment_score) as avg_ticker_sentiment_score
from marts.core.news_sentiment
group by 1, 2
order by 2 desc, 1