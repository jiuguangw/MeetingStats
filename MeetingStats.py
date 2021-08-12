#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2021 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is released under the  MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.


import sys
from icalendar import Calendar
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters


# Parameters
start_date = dt.datetime(2020, 11, 16)
end_date = dt.datetime(2021, 8, 10)
PTO_list = ["Company Holiday", "JW - PTO", "BIP JIRA Sync", "Flight",
            "People Ops/Finance Office Hours", "P&C Planning Meeting Pre-Read",
            "Office Hours", "Part Time Approval", "Busy", "NO MEETING BLOCK",
            "Hold for Eng Leads", "People Ops/Finance/Exec Office Hours"]


class CalendarEvent:
    summary = ''
    uid = ''
    description = ''
    location = ''
    start = ''
    end = ''
    url = ''

    def __init__(self, name):
        self.name = name


def workdays(start, end, excluded=(6, 7)):
    days = []
    while start.date() <= end.date():
        if start.isoweekday() not in excluded:
            days.append(start)
        start += dt.timedelta(days=1)
    return days


def export_figure(figure, dim_x, dim_y, output_filename):
    # Export
    figure.set_size_inches(dim_x, dim_y)
    figure.savefig(output_filename, bbox_inches='tight')
    figure.clf()


def plot_results(result):
    # Matplotlib converters
    register_matplotlib_converters()

    # Style
    sns.set(style="darkgrid")

    # Plot daily
    f, axarr = plt.subplots(2, 1)
    axarr[0].plot(result['Date'],
                  result['Duration'])
    axarr[0].set_title('Meeting Duration (Daily)')
    axarr[0].set_xlabel('Date')
    axarr[0].set_ylabel('Duration (Hours)')

    # Plot weekly
    result = result.set_index(result['Date'])
    weekly = result['Duration'].resample('W').sum()
    axarr[1].plot(weekly.index, weekly)
    axarr[1].set_title('Meeting Duration (Weekly)')
    axarr[1].set_xlabel('Date')
    axarr[1].set_ylabel('Duration (Hours)')

    # Save
    export_figure(f, 17, 11, 'MeetingStats.pdf')


def parse_ics(filename):
    f = open(filename, 'rb')

    # Stole most of this stuff from:
    # https://github.com/erikcox/ical2csv/blob/master/ical2csv.py

    gcal = Calendar.from_ical(f.read())

    events = []

    for component in gcal.walk():
        event = CalendarEvent("event")
        if component.get('TRANSP') == 'TRANSPARENT':
            continue  # skip event that have not been accepted
        if component.get('SUMMARY') is None:
            continue  # skip blank items
        event.summary = component.get('SUMMARY')
        event.uid = component.get('UID')
        if component.get('DESCRIPTION') is None:
            continue  # skip blank items
        event.description = component.get('DESCRIPTION')
        event.location = component.get('LOCATION')
        if hasattr(component.get('dtstart'), 'dt'):
            event.start = component.get('dtstart').dt
        if hasattr(component.get('dtend'), 'dt'):
            event.end = component.get('dtend').dt

        event.url = component.get('URL')
        events.append(event)
    f.close()

    # Needed to sort events
    # They are not fully chronological in a Google Calendar export
    sortedevents = sorted(events, key=lambda obj: obj.start)

    return sortedevents


def main():
    # Parse the ICS file
    calendar_events = parse_ics(sys.argv[1])

    # Construct the dataframe
    headers = ['Title', 'Start Time', 'End Time']
    data = pd.DataFrame(columns=headers)

    for event in calendar_events:
        title = event.summary.encode('utf8').decode()

        # Skip the PTOs
        if (title in PTO_list):
            continue

        # Combine data into a row and append
        row = {'Title': title,
               'Date': event.start.date(),
               'Start Time': event.start,
               'End Time': event.end}
        data = data.append(row, ignore_index=True)

    # Compute meeting duration in hours
    data["Duration"] = (data["End Time"] - data["Start Time"]
                        ).dt.total_seconds() / 3600

    # Get a list of workdays and add up meeting duration
    result = pd.DataFrame(columns=['Date', 'Duration'])
    for date in workdays(start_date, end_date):
        meetings = data.loc[data['Date'] == date.date()]
        time_total = meetings['Duration'].sum()
        row = {'Date': date, 'Duration': time_total}
        result = result.append(row, ignore_index=True)

    # Plot the results
    plot_results(result)


main()
