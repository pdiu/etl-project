{{
    config(
        materialized='table'
    )
}}

with final as (
    select
        title
        , url
        , to_timestamp(time_published, 'YYYYMMDD"T"HH24MISS')::date as date_published
        , to_timestamp(time_published, 'YYYYMMDD"T"HH24MISS')::time as time_published
        , authors
        , summary
        , source
        , case
            when category_within_source = 'n/a' then null
            else category_within_source
        end as category_within_source
        , source_domain
        , topics
        , cast(overall_sentiment_score as decimal(18,8)) as overall_sentiment_score
        , overall_sentiment_label
        , ticker_sentiment
    from raw.alphavantage.news_sentiment
)

select * from final;

