"""covid_news_handling

This module contains code to handle and display information
about news articles that are related covid

It exports the following functions:
- news_API_request(covid_terms)
    - fetches news articles related to covid
- update_news()
    - updates the news articles list with new news articles using the
    news_API_request function
- schedule_news_updates(update_interval, update_name, repeat=False)
    - schedules an update to the news articles at a user given time"""

import datetime
import sched
import time
from newsapi import NewsApiClient
from datetime import date


news_articles = []
removed_articles = []
newsapi = NewsApiClient(api_key='0b07dcbb3d2e49feb1f6c7e311e3bfc5')
top_headlines = newsapi.get_top_headlines(q='covid',
                                          sources='bbc-news',
                                          language='en', )
today = date.today()
day_ago = today - datetime.timedelta(days=1)


def news_API_request(covid_terms: str = 'Covid' or 'COVID-19' or 'coronavirus'):
    """This function finds news articles related to covid-19 from
    the news API.
    This function returns the following variables:
    - list_head - a list of all the covid headlines
    - list_cont - a list of all the descriptions from the covid articles
    - list_url - a list of all the urls from the articles

    """
    top_headlines_covid = newsapi.get_everything(q=covid_terms,
                                                 sources='bbc-news,sky-news',
                                                 from_param=day_ago,
                                                 to=today,
                                                 language='en',
                                                 sort_by='relevancy',
                                                 page=1
                                                 )
    articles = (top_headlines_covid['articles'])
    list_head = []
    list_cont = []
    list_url = []
    for i in articles:
        headline = i['title']
        content = i['description']
        url = i['url']
        list_head.append(headline)
        list_cont.append(content)
        list_url.append(url)

    return list_head, list_cont, list_url


def update_news():
    """This function uses the sched module to update
    the news articles on the dashboard"""
    articles = news_API_request()
    new_articles = []
    for article in articles:
        if article not in removed_articles:
            new_articles.append(article)
    news_articles = new_articles
    list_headline = news[0]
    list_content = news[1]


def schedule_updates(update_interval: time, update_name: str, repeat=False):
    schedule = sched.scheduler(time.time, time.sleep)
    schedule.enter(update_interval, 1, update_news)
    print("start")
    schedule.run()
    print("end")


news = news_API_request()
update_news()
