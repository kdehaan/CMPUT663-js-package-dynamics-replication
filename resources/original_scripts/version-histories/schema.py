#!/usr/bin/env python
import sys

from db import DB

if __name__ == "__main__":
    if len(sys.argv) < 3 or (sys.argv[2] != "up" and sys.argv[2] != "down"):
        print("Usage: %s id {up,down}" % sys.argv[0])
        sys.exit(1)

    which = sys.argv[1]

    if sys.argv[2] == "down":
        src = "./sql/%s-down.sql" % which
    else:
        src = "./sql/%s-up.sql" % which

    print "Executing script: %s" % src

    with open(src) as fp:
        contents = fp.read()

    print ""
    print contents

    db = DB()
    db.cursor.execute(contents)

