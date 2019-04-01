# !/usr/bin/env python

#
# Reads npm-metadata and creates a leaner output, containing only the package name,
# version times, and dependency history.
# 
# Input is "npm_repos-09_22-15.txt" (Who named that file???)
#
import json
import sys

FILE = sys.argv[1]

with open(FILE) as lines:
  for line in lines:
    d = json.loads(line)

    nd = {}

    nd["name"] = d["name"]

    if "time" in d:
      nd["time"] = d["time"]

      # Actually useful
      # del nd["time"]["created"]
      del nd["time"]["modified"]

    if "versions" in d:
      nv = {}

      for v,vd in d["versions"].iteritems():
        nv[v] = {}

        if "dependencies" in vd:
          nv[v]["dependencies"] = vd["dependencies"]
        
        if "devDependencies" in vd:
          nv[v]["devDependencies"] = vd["devDependencies"]

      nd["versions"] = nv

    print json.dumps(nd)
