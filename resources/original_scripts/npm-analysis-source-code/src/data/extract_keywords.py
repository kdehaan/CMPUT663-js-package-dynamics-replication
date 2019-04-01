#!/usr/bin/env python

#
# Goes through the npm metadata and extracts per package the keywords (if available).
# 
# Input: npm "skim", e.g., npm_skim_09-22-15.json
#
import json
import sys

npm_data = json.load(open('../../data/npm_skim_09-22-15.json'))

print 'package,keywords'

for repo in npm_data:
  try:
    name = repo['key']
    if 'value' in repo and 'keywords' in repo['value']:
      keyword_list = repo['value']['keywords']
      keywords = ';'.join(keyword_list)
      keywords = keywords.replace(',', '')
      print '%s,%s' % (name, keywords)
    else:
      print '%s,' % (name)
  except UnicodeEncodeError, e:
    pass
