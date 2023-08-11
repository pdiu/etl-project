select
    title
    , date_published
    , time_published
    , array_size(author) as author_count
    , array_slice(author, 0, 1)[0]::text as primary_author
    , case
        when array_size(author) = 2 then
            array_slice(author, 1, 2)[0]::text
        else
            null
    end as secondary_author
    , summary
    , source
    , category_within_source
    , source_domain
    , f_topics.value:topic::text as topic
    , f_topics.value:relevance_score::float as topic_relevance_score
    , overall_sentiment_score
    , overall_sentiment_label
    , f_ticker_sentiment.value:relevance_score::float as ticker_relevance_score
    , f_ticker_sentiment.value:ticker_sentiment_label::text as ticker_sentiment_label
    , f_ticker_sentiment.value:ticker_sentiment_score::float as ticker_sentiment_score
from {{ ref('stg_alphavantage_news__sentiments')}}
, lateral flatten(parse_json(topics)) as f_topics
, lateral flatten(parse_json(ticker_sentiment)) as f_ticker_sentiment
