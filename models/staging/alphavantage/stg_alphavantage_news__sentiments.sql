{{
    config(
        materialized = 'incremental'
        , unique_key = 'unique_str'
    )
}}

with stg_news_sentiment as (
    select
        title
        , url
        , to_timestamp(time_published, 'YYYYMMDD"T"HH24MISS')::date as date_published
        , to_timestamp(time_published, 'YYYYMMDD"T"HH24MISS')::time as time_published
        , to_array(parse_json(authors)) as author
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
        , insert_timestamp
    from {{ source('alphavantage', 'news_sentiment') }}
),

stg_news_sentiment_unique as (
    select
        distinct title || url || date_published as unique_str
    from stg_news_sentiment
),

final as (
    select
        stg.*
    from
        stg_news_sentiment as stg
    inner join
        stg_news_sentiment_unique as stg_unique
            on stg.title || stg.url || stg.date_published = stg_unique.unique_str
            
    {% if is_incremental() %}

    where
        stg.insert_timestamp > select(max(stg.insert_timestamp) from {{ this }})

    {% endif %}
)

select * from final

