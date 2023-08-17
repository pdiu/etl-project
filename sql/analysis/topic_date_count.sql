select
   date_published
   , topic
   , count(distinct title || topic) as articles_published
from marts.core.news_sentiment
group by 1, 2
having count(distinct title) > 2
order by 1