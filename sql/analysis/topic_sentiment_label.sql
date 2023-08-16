select
    topic
    , case
        when avg(overall_sentiment_score) <= -0.35 then
            'Bearish'
        when avg(overall_sentiment_score) > -0.35 and avg(overall_sentiment_score) <= -0.15 then
            'Somewhat Bearish'
        when avg(overall_sentiment_score) > -0.15 and avg(overall_sentiment_score) <= 0.15 then
            'Neutral'
        when avg(overall_sentiment_score) > 0.15 and avg(overall_sentiment_score) <= 0.35 then
            'Somewhat Bullish'
        else
            'Bullish'
    end as avg_sentiment_label
from marts.core.news_sentiment
group by 1
order by 1