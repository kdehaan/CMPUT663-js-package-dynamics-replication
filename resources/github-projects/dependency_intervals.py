import json
import sys
import dateutil.parser

"""This script takes as an input a package.json history file, and produces, for each dependency, an ordered list of requirement queries with begin and end time."""

HISTORYFILE=sys.argv[1]

with open(HISTORYFILE) as hf:
    data = json.load(hf)

    file_creation_time = dateutil.parser.parse(data["creation_time"])

    commits_to_time = map(lambda p : (p[0], dateutil.parser.parse(p[1])), list(data["time"].iteritems()))
    commits_to_time.sort(key=lambda p: p[1], reverse=True)

    # This is the "end of the universe" date for this particular history file.
    prev_date = file_creation_time

    bounds = {}
    devBounds = {}

    for (commit,ts) in commits_to_time:
        pkg_data = data["versions"][commit]

        deps = pkg_data.get("dependencies", {})
        devDeps = pkg_data.get("devDependencies", {})

        for (dep,query) in deps.iteritems():
            pair = (dep,query)
            if not pair in bounds:
                bounds[pair] = (ts,prev_date)
            else:
                before = bounds[pair]
                bounds[pair] = (ts,before[1])

        for (dep,query) in devDeps.iteritems():
            pair = (dep,query)
            if not pair in devBounds:
                devBounds[pair] = (ts,prev_date)
            else:
                before = devBounds[pair]
                devBounds[pair] = (ts,before[1])

        prev_date = ts

    final_object = {}
    final_object["_id"] = data["_id"]
    final_object["creation_time"] = data["creation_time"]

    intervals = {}
    devIntervals = {}

    for ((d,v),(s,e)) in bounds.iteritems():
        intervals["%s:%s" % (d,v)] = {
            "from" : s.isoformat(),
            "to"   : e.isoformat()
        }

    for ((d,v),(s,e)) in devBounds.iteritems():
        devIntervals["%s:%s" % (d,v)] = {
            "from" : s.isoformat(),
            "to"   : e.isoformat()
        }

    final_object["dependencies"] = intervals
    final_object["devDependencies"] = devIntervals

    print json.dumps(final_object, indent=2)
