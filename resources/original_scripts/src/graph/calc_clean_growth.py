#!/usr/bin/env python

#
# Script to calculate package growth over time considering only active packages.
# 
# Input: 
# - "npm_version_dates.json"
#    (which is an array of JSON objects describing each package in the following way:
#        {
#          "name": "...",
#          "time": {
#            "created": "2013-05-18T14:04:50.640Z",
#            "0.0.1": "2013-05-18T14:04:53.742Z",
#            ...
#          }
#        }
#    )
# - Number of days in which activity must have occurred for a package to be considered.
#
import sys
import json
import time
import datetime
import pytz
import pandas as pd

from dateutil import rrule, parser


def visualize_growth_clean(input_file, delta_value):
  # create a date range:
  dates = get_date_range('10-01-2010', '09-01-2015', 'weekly')
  # localize:
  dates = map(lambda x: pytz.UTC.localize(x), dates)

  repos_at_date = {}
  for date in dates:
    repos_at_date[str(date)] = 0  
  count = 0

  delta = datetime.timedelta(days=delta_value)

  with open(input_file) as data_file:    
    data = json.load(data_file)

  print 'loaded data.'

  for repo in data:
    count  += 1
    if count % 200 == 0:
      print '%s - %s' % (count, repo['name'])

    # iterate dates:
    if 'time' in repo:
      for date in dates:
        date_str = str(date)
        latest_version_date = pytz.UTC.localize(datetime.datetime(2010, 1, 1))
        latest_version = None

        for key, version in enumerate(repo['time']):
          version_date = parser.parse(repo['time'][version])
          try:
            if version_date < date and latest_version_date < version_date:
              latest_version_date = version_date
              latest_version = version
          except TypeError:
            pass
        if latest_version is not None and (date - latest_version_date) < delta:
          # print 'Latest version of "%s" (%s) is NEWER than %s at %s' % (repo['name'], latest_version, delta_value, date_str)
          repos_at_date[date_str] += 1
        else:
          # print 'Latest version of "%s" (%s) is OLDER than %s at %s' % (repo['name'], latest_version, delta_value, date_str)
          pass

  df = pd.DataFrame(repos_at_date, index=[0]).T
  df.columns = ['number repos']
  print df
  df.to_csv('repos_newer_' + str(delta_value) + '_days_at_date.csv')



#
# Creates a list of dates from the start date to the end date
# with the given interval
#
def get_date_range(start_date, end_date, interval):
  # create dates:
  rule = rrule.DAILY
  if interval == 'daily':
    rule = rrule.DAILY
  elif interval == 'weekly':
    rule = rrule.WEEKLY
  elif interval == 'monthly':
    rule = rrule.MONTHLY
  else:
    print 'Could not identify interval %s. Try daily, weekly, or monthly' % (interval)

  dates = list(rrule.rrule(rule,
            interval=1,
            dtstart=parser.parse(start_date),
            until=parser.parse(end_date)))
  return dates


if __name__=='__main__':
  if len(sys.argv) < 3:
      print 'usage: %s <input-data> <activity window [int]>' % (sys.argv[0])
      exit(-1)
  input_file = sys.argv[1]
  activity_window = int(sys.argv[2])
  visualize_growth_clean(input_file, activity_window)
  
