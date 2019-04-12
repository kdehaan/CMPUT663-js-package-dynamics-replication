#!/usr/bin/python

##input: developer_activity.py 2015-11-01_npm_skim.json npm_version_dates.json

import json
import sys
import math
import datetime
import pytz
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
from dateutil import rrule, parser

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

def packages_devs_per_month(skim_file, versions_file):
    packages = {}
    versions = {}
    
    with open(skim_file) as fp:
        packages = json.load(fp)

    with open(versions_file) as fp:
        tempversions = json.load(fp)

    for p in tempversions:
        try:
            versions[p['name']] = p['time']
        except KeyError:
            pass

    dates = get_date_range('10-01-2010', '09-01-2015', 'monthly')
    # localize:
    dates = map(lambda x: pytz.UTC.localize(x), dates)

    start_date = dates[0]
    end_date = dates[-1]
    dates.pop()

    p_other = {}
    repos_at_date = {}
    all_maintainers = {}
    total_devs = 0
    for date in dates:
        repos_at_date[date.strftime('%Y-%m-%d')] = {"Packages": 0, "Developers" : 0}

    for p in packages:
      try:
        name = p['value']['name']
        vcount = len(versions[name]) - 1
        created = parser.parse(versions[name]['created'])
        created_str = created.strftime('%Y-%m-01')
        license = p['value']['license']
        for m in p['value']['maintainers']:
          if m['email'] in all_maintainers:
            all_maintainers[m['email']]['Packages'] += 1
          else:
            all_maintainers[m['email']] = {"Packages" : 1}

            #        print "%s,%s,%d,%s,%s, %d, %d" % (name, created_str, vcount, license, len(p['value']['maintainers']), created.year, created.month) #m['name'],m['email'])
        if created.year < end_date.year or created.month < end_date.month:
          p_other[name] = {"Developers": len(p['value']['maintainers']), "Versions": vcount}
          repos_at_date[created_str]["Packages"] += 1
          total_devs += 1
          repos_at_date[created_str]["Developers"] += len(p['value']['maintainers'])
      except KeyError:
        pass
      except UnicodeEncodeError:
        pass

    print 'There were %d unique devs out of %d devs' % (len(all_maintainers), total_devs)
    df = pd.DataFrame(data=repos_at_date)
    df.to_csv('repos_and_devs_per_month.csv')

    df = pd.DataFrame(data=p_other)
    df.to_csv('devs_versions_per_repo_hist.csv')

    count = 1
    print ", Packages"
    for m in all_maintainers:
      print "%d,%d" % (count, all_maintainers[m]['Packages'])
      count += 1
    #df  = pd.DataFrame(data=all_maintainers)
    #df.to_csv('repos_per_dev_hist.csv', encoding='utf-8')

if __name__ == '__main__':
  if len(sys.argv) < 3:
      print 'usage: developers.py 2015-11-01_npm_skim.json npm_version_dates.json >repos_per_dev_hist.csv'
      exit(-1)
  skim_file = sys.argv[1]
  versions_file = sys.argv[2]
  packages_devs_per_month(skim_file, versions_file)
