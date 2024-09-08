{{
    config(
        materialized = 'incremental'
        , unique_key = 'primary_key'
    )
}}

with stg_news_sentiment as (
    select
        title
        , url
        , to_timestamp(time_published, 'YYYYMMDD"T"HH24MISS')::date as publish_date
        , to_timestamp(time_published, 'YYYYMMDD"T"HH24MISS')::time as publish_time
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
        , insert_timestamp::datetime::date as insert_date
        , insert_timestamp::datetime::time as insert_time
    from
        {{ source('alphavantage', 'news_sentiment') }}
)

, add_primary_key as (
    select
        md5(to_json(object_construct(* exclude(insert_time)))) as primary_key
        , *
    from
        stg_news_sentiment
)

, remove_duplicates as (
    select
        *
    from
        add_primary_key
    qualify
        row_number() over (
            partition by primary_key
            order by insert_date desc
        ) = 1
)

, final as (
    select
        *
    from
        remove_duplicates
)

select * from final