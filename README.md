# Covid-19 Dashboard 
## Introduction
This project creates a COVID-19 dashboard with up-to-date 
information of current covid levels and relevant news related to the pandemic. 
The numeric data shown on the dashboard will be the total 7-day cases in your local area along 
with a separate 7-day total for national data, the current hospital admissions and the total number
of deaths in your country. On the right-hand side of the dashboard will be a widget containing the 
latest news that relates to COVID-19; and on the left and lower centre there is a scheduling widget 
for you to create update schedules so that the data shown on the dashboard will update at a given interval.
## Prerequisites
* Python 3.7 or above
* Python sched module
* Python flask module
* Python time module
* Python json module
* Python logging module
* uk_covid19 module (information [here](https://publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/pages/getting_started.html))
* newsapi module (information [here](https://newsapi.org/docs/get-started))

## Installation
* pip install

## Getting Started
To run the application navigate to the installation 
location and execute the terminal command:
* python main.py

Now navigate to the webpage at http://127.0.0.1:5000/index

## Testing
* Enter a terminal
* Navigate to the folder containing this project
* Run pytest
## Developer documentation
The source code contains 4 python modules:
* main.py
* covid_data_handler.py
* covid_news_handling.py
* time_conversions.py

The source also includes:
* config.json (configuration file)
* index.html (Template for the dashboard)
* nation_2021-10-28.csv (csv file including covid data)

## Details
* Made by Ben Skudder
* Shared under [MIT](https://opensource.org/licenses/MIT)
* source code is hosted on GitHUb [here](https://github.com/skudz/Covid-dashboard)

