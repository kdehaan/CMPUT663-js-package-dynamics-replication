#!/bin/bash
#/opt/influxdb/influx -execute="select sum(value) from downloads where time >= '2015-09-01T00:00:00Z' AND time < '2015-09-02T00:00:00Z' group by package" \
#	-database=npm -username=user -password=passw0rd -format='csv' >/tmp/a
/opt/influxdb/influx -execute="select sum(value) from downloads where time < '2015-09-02T00:00:00Z' group by package" \
	-database=npm -username=user -password=passw0rd -format='csv' >/tmp/a

grep 'downloads' /tmp/a |cut -d '=' -f2|cut -d ',' -f1,3|sort -g -r -t',' -k2 >/tmp/b
#python add-ranking-to-sortedlist.py /tmp/b >npm-downloads-ranking-2015-08-26-to-2015-09-01.csv
python add-ranking-to-sortedlist.py /tmp/b >npm-downloads-ranking-2010-01-01-to-2015-09-01.csv

