#!/usr/bin/python
import json
import sys

FILE = sys.argv[1]
DATE = sys.argv[2]

pdownloads = {}

with open(FILE, 'r') as f:
    for line in f:        
        l = json.loads(line)
        if 'package' not in l  or 'downloads' not in l:
            continue
#        print 'processing package %s' % l['package']
        for day in l['downloads']:
            if day['day'] == DATE:
                pdownloads[l['package']] = day['downloads']
                break

i = 0
prev = 0

for w in sorted(pdownloads, key=pdownloads.get, reverse=True):
    if prev != pdownloads[w]:
        i = i+1
        prev = pdownloads[w]

    print "%s,%d,%d" % (w, i, pdownloads[w])
