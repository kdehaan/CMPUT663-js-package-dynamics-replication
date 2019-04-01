import json
import subprocess

import fileinput
from loader import Loader

def emit_range(package_name, query_string, result, from_ts, to_ts):
    print json.dumps({
        "p"    : package_name,
        "vq"   : query_string,
        "vr"   : result,
        "from" : from_ts,
        "to"   : to_ts
    })

if __name__ == "__main__":
    prev_package = None
    prev_query   = None
    prev_result  = None
    start_ts     = -1
    end_ts       = -1

    emitted = 0

    for line in fileinput.input():
        data = json.loads(line)

        package = data["p"]
        query   = data["vq"]
        result  = data["vr"]
        ts      = data["at"]

        if package == prev_package and query == prev_query and result == prev_result:
            # When all it the same, we just skip over, but we widen the range.
            end_ts = ts
            continue

        if prev_package is not None and prev_result is not None:
            emit_range(prev_package, prev_query, prev_result, start_ts, end_ts)
            if prev_package != package:
                emitted += 1
                pass

        prev_package = package
        prev_query   = query
        prev_result  = result
        start_ts     = ts
        end_ts       = ts

        
