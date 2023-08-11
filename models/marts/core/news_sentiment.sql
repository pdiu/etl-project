select
    *
from {{ ref('stg_alphavantage_news__sentiments')}}