import json
import re
import dateutil.parser

class GitHubHistory:
    def __init__(self, json_file):
        with open(json_file) as fp:
            self.data = json.load(fp)

        m = re.match("""^github:([^:]+):([^:]+)$""", self.data["_id"])

        self.user = m.group(1)
        self.repo = m.group(2)

    def get_intervals(self):
        file_creation_time = dateutil.parser.parse(self.data["creation_time"])

        commits_to_time = map(lambda p : (p[0], dateutil.parser.parse(p[1])), list(self.data["time"].iteritems()))
        commits_to_time.sort(key=lambda p: p[1], reverse=True)

        # This is the "end of the universe" date for this particular history file.
        prev_date = file_creation_time

        bounds = {}
        devBounds = {}

        for (commit,ts) in commits_to_time:
            pkg_data = self.data["versions"][commit]

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
        # final_object["_id"] = self.data["_id"]
        # final_object["creation_time"] = self.data["creation_time"]

        intervals = []
        devIntervals = []

        for ((d,v),(s,e)) in bounds.iteritems():
            intervals.append({
                "package" : d,
                "version" : v,
                "from"    : s.isoformat(),
                "to"      : e.isoformat()
            })

        for ((d,v),(s,e)) in devBounds.iteritems():
            devIntervals.append({
                "package" : d,
                "version" : v,
                "from"    : s.isoformat(),
                "to"      : e.isoformat()
            })

        final_object["dependencies"] = intervals
        final_object["devDependencies"] = devIntervals

        return final_object
