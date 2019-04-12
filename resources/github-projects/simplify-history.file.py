import json
import sys

with open(sys.argv[1]) as hist_file:
    data = json.load(hist_file)

    simpler = {}

    simpler["repository"]  = data["repository"]
    simpler["_id"]         = data["_id"]
    simpler["json_errors"] = data["json_errors"]

    new_versions = {}

    for k,v in data["versions"].iteritems():
        new_v = {}

        if "dependencies" in v:
            new_v["dependencies"] = v["dependencies"]

        if "devDependencies" in v:
            new_v["devDependencies"] = v["devDependencies"]

        if new_v:
            new_versions[k] = new_v

    new_time = dict(filter(lambda p: p[0] in new_versions, list(data["time"].iteritems())))

    simpler["versions"] = new_versions
    simpler["time"] = new_time

    with open(sys.argv[2], 'w') as dest_file:
        dest_file.write(json.dumps(simpler, indent=2))

