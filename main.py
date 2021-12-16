"""main
This module is for interacting with the flask template
and scheduling updates.
"""
from flask import Flask, render_template, request
from time_conversions import hhmm_to_seconds
from datetime import datetime
import sched
import time
import covid_data_handler
import covid_news_handling
app = Flask(__name__)
s = sched.scheduler(time.time, time.sleep)
news = []
removed_news = []
updates = []

deaths = 'Total deaths in England: ' + str(covid_data_handler.death_total)
hospital_cases = 'Current Hospital cases in England: ' + str(covid_data_handler.hospital_cases)
weekly_cases = covid_data_handler.weekly_cases
national_weekly_cases = covid_data_handler.national_weekly_cases
now = datetime.now()


def add_news():
    """This function adds news articles to the dashboard
    It takes variables from the covid_news_handling module and adds
    them to a list of articles"""
    list_headline = covid_news_handling.news[0]
    list_head = len(covid_news_handling.news[0]) - 1
    list_cont = covid_news_handling.news[1]
    list_url = covid_news_handling.news[2]
    for i in range(0, 5):
        news.append({
            'title': list_headline[i],
            'content': list_cont[i],
        })


def schedule_add_news(up):
    """ This Function is supposed to schedule news updates"""
    e1 = s.enter(up, 1, add_news())


def remove_news(title: str):
    """This Function was intended to all the user to remove news articles when
    they clicked the close button on them"""
    article_title = request.args.get('notif')
    for i in news:
        if i['title'] == article_title:
            news.remove(i)
            removed_news.append(i)
            break


def add_updates():
    """This function adds updates to the widget on the left of the homepage
    It also schedules the updates to news and data"""
    alarm = request.args.get('update')
    name = request.args.get('two')
    covid_data = request.args.get('covid_data')
    news_update = request.args.get('news')
    repeat = request.args.get('repeat')
    content = 'Update will take place at: ' + str(alarm)
    set_time = 0

    if alarm != "":
        set_time = datetime.strptime(alarm, '%H:%M').time()
        today = datetime.today()
        current_time = today.time()

    if covid_data:
        covid_data_handler.schedule_covid_updates(set_time, name, repeat=repeat)

    if news_update:
        covid_news_handling.schedule_updates(set_time, name, repeat=repeat)
    updates.append(dict(title=request.args.get('two'), content=content))


def remove_updates():
    """This function was intended to remove updates when the user
     presses the close button on the notification"""
    name = request.args.get('alarm_item')
    cancelled = False
    for update in reversed(updates):
        if update['title'] == name:
            s.cancel(update['title'])
            updates.remove(name)


def current_time_hhmm():
    """This function returns the current time"""
    return str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min)


if __name__ == "__main__":
    @app.route('/index')
    def hello():
        add_news()
        s.run(blocking=False)
        text_field = request.args.get('two')
        print(text_field)
        if text_field:
            update_time = request.args.get('update')
            print(update_time)
            update_time_sec = hhmm_to_seconds(update_time)
            schedule_add_news(update_time_sec)
            add_updates()
            remove_updates()

        return render_template('index.html',
                               title='Daily COVID-19 Update',
                               news_articles=news,
                               updates=updates,
                               location='Exeter',
                               nation_location='England',
                               local_7day_infections=weekly_cases,
                               national_7day_infections=national_weekly_cases,
                               hospital_cases=hospital_cases,
                               deaths_total=deaths
                               )

if __name__ == '__main__':
    app.run()
    remove_news(request.args.get('notif'))
