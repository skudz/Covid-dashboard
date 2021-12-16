"""Covid_data_handler

This module handles the fetching and processing of covid data.

It exports the following functions to other modules:
- parse_csv_data(csv_filename) - returns a list of strings
- process_csv_data(covid_csv_data)
    -returns cases from the last 7 days,current number of hospital cases
    and the total number of deaths.
-schedule_covid_updates(update_interval, update_name, repeat=False)
    - schedules an update for covid data at a user input time
"""

import sched
import time
from typing import Dict, Union, List
from requests import get
from json import dumps


def parse_csv_data(csv_filename: str):
    """Function to convert the csv file into a list of strings"""
    lines = open(csv_filename, 'r').readlines()
    return list(lines)


def find_first_entry(data: List[Dict], key: str):
    i = 0
    while i < len(data) and data[i][key] is None:
        i += 1
    return None if i == len(data) else i


def process_covid_csv_data(covid_csv_data: List[str]):
    """Function that returns 3 variables from the csv file
    variables returned:
        - last7days_cases - cumulative number of cases from the last 7 days
        - current_hospital_cases - number of current hospital covid-19 cases
        - total_deaths - cumulative number of deaths"""
    covid_csv_data_dict = []
    for line in covid_csv_data[1:]:
        covid_csv_data_dict.append(line.rstrip().split(","))
    last7days_cases = 0

    day1 = covid_csv_data_dict[0]
    day14 = covid_csv_data_dict[13]
    current_hospital_cases = day1[5]
    total_deaths = day14[4]

    for i in range(2, 9):
        day = covid_csv_data_dict[i]
        last7days_cases += int(day[6])

    return last7days_cases, current_hospital_cases, total_deaths


def covid_API_request(location="Exeter", location_type="ltla"):
    """This Function returns up to date covid data for a specified location,
        the function gathers this data from the news API

        This function returns the following variables:
        - daily_cases - daily total of new cases
        - daily_deaths - daily total of new deaths
        - cum_deaths - total number of deaths since the start of the pandemic
        - cases_7days- number of new cases from the last 7 days
        """
    filters = [
        f"areaType={location_type}",
        f"areaName={location}"
    ]
    structure_type = Dict[str, Union[dict, str]]
    structure = dict(date="date", name="areaName", code="areaCode", dailyCases="newCasesByPublishDate",
                     dailyDeaths="newDeaths28DaysByPublishDate", cumulativeDeaths="cumDeaths28DaysByPublishDate")
    api_params = {
        "filters": str.join(";", filters),
        "structure": dumps(structure, separators=(",", ":")),
        "format": "json"
    }
    endpoint = 'https://api.coronavirus.data.gov.uk/v1/data'

    response = get(endpoint, params=api_params, timeout=10)
    json_response = response.json()
    data = (json_response["data"])
    daily_data = data[0]
    daily_cases = (daily_data['dailyCases'])
    daily_deaths = (daily_data['dailyDeaths'])
    cum_deaths = (daily_data['cumulativeDeaths'])
    print(data)

    daily_cases_list = []
    for i in range(0, 6):
        daily_ex = (data[i])
        daily_cases_list.append(daily_ex['dailyCases'])
    cases_7days = sum(daily_cases_list)
    if response.status_code >= 400:
        raise RuntimeError(f'request failed:')
    return daily_cases, daily_deaths, cum_deaths, cases_7days


def schedule_covid_updates(update_interval: time, update_name: str, repeat=False):
    """This function schedules updates to the covid data
    the sched module is used to schedule updates to the covid data at
    a given time interval input by the user"""

    schedule = sched.scheduler(time.time, time.sleep)
    schedule.enter(update_interval, 1, covid_API_request)
    print("start")
    schedule.run()
    print("end")


covid_data = parse_csv_data('nation_2021-10-28.csv')
covid_data2 = process_covid_csv_data(covid_data)
api_run = covid_API_request()
national_data = covid_API_request('England', 'nation')
death_total = national_data[2]
weekly_cases = api_run[3]
national_weekly_cases = national_data[3]
hospital_cases = covid_data2[1]
