{{
    config(
        materialized = 'table'
    )
}}

WITH stg_news_sentiment AS (
    SELECT
        title
        , url
        , to_timestamp(time_published, 'YYYYMMDD"T"HH24MISS')::date AS publish_date
        , to_timestamp(time_published, 'YYYYMMDD"T"HH24MISS')::time AS publish_time
        , to_array(parse_json(authors)) AS author
        , summary
        , source
        , CASE
            WHEN category_within_source = 'n/a' THEN NULL
            ELSE category_within_source
        END AS category_within_source
        , source_domain
        , topics
        , cast(overall_sentiment_score AS decimal(18,8)) AS overall_sentiment_score
        , overall_sentiment_label
        , ticker_sentiment

        -- Metadata
        , current_user() AS insert_user
        , insert_timestamp::datetime::date AS insert_date
        , insert_timestamp::datetime::time AS insert_time
    FROM
        {{ source('alphavantage', 'news_sentiment') }}
)

, add_primary_key AS (
    SELECT
        md5(to_json(object_construct(* exclude(insert_time)))) AS primary_key
        , *
    FROM
        stg_news_sentiment
)

, remove_duplicates AS (
    SELECT
        *
    FROM
        add_primary_key
    QUALIFY
        ROW_NUMBER() OVER (
            PARTITION BY PRIMARY_KEY
            ORDER BY INSERT_DATE DESC
        ) = 1
)

, final AS (
    SELECT
        *
    FROM
        remove_duplicates
)

SELECT * FROM final