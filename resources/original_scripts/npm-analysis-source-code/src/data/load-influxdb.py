#!/usr/bin/python
import json
import sys
import time
import requests
import cStringIO

#format is measurement[,tag_key1=tag_value1...] field_key=field_value[,field_key2=field_value2] [timestamp_in_nanosecs]

measurement='downloads'
tag='package'
key='value'
FILE=sys.argv[1]
count = 0
with open(FILE,'r') as fp:
    for line in fp:
        l = json.loads(line)
        if 'package' not in l  or 'downloads' not in l:
            continue
        package = l['package']
        downloads = l['downloads']
        body = cStringIO.StringIO()
        count = 0
        for day in downloads:
            value=day['downloads']
            ts=time.mktime(time.strptime(day['day'],'%Y-%m-%d'))
            print >>body, "%s,%s=%s %s=%d %d" % (measurement,tag,package,key,value,ts)
            count += 1

        r = requests.post('http://localhost:8086/write?db=npm&u=user&p=passw0rd&precision=s',
                          headers={'Content-Type': 'application/octet-stream'},
                          data = body.getvalue())
        body.close()
        print >>sys.stderr, 'posted %d measurements for package %s with status %d' % (count, package, r.status_code)
        sys.stderr.flush()

