#!/usr/bin/env python

#
# Script to generate a lit of new packages introduced into npm, by month
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
#
import sys
import json
import time
import datetime
import pytz
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from dateutil import rrule, parser


def visualize_newrepos(input_file):
  # create a date range:
  dates = get_date_range('10-01-2010', '04-01-2019', 'monthly')
  # localize:
  dates = map(lambda x: pytz.UTC.localize(x), dates)

  end_date = dates[-1]
  dates.pop()

  repos_at_date = {}
  for date in dates:
    repos_at_date[date.strftime('%Y-%m-%d')] = 0
  count = 0
  errors = 0
  
  with open(input_file) as data_file:    
    data = json.load(data_file)

  print 'loaded data.'

  for repo in data:
    count  += 1
    if count % 200 == 0:
      print '%s - %s' % (count, repo['name'])

    # iterate dates:
    if 'time' in repo:
      version_date = parser.parse(repo['time']['created'])
      try:
        if version_date < end_date:
          date_str = version_date.strftime('%Y-%m-01')
          repos_at_date[date_str] += 1
      except TypeError:
        errors += 1
        pass
      except KeyError:
        errors += 1
        pass

  print 'Had %d errors' % (errors)
  print 'Total num repos in buckets is %d against total processed %d' % (sum(repos_at_date.values()), count)

  df = pd.DataFrame(repos_at_date, index=[0]).T
  df.columns = ['newrepos']
  print df
  df.to_csv('npm_newpkgs_per_month.csv')



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
  if len(sys.argv) < 2:
      print 'usage: %s <input-data>' % (sys.argv[0])
      exit(-1)
  input_file = sys.argv[1]
  visualize_newrepos(input_file)
