import glob
import json
import sys

all_files = list(glob.glob("%s/*.json" % sys.argv[1]))

for file_name in all_files:
    with open(file_name) as fh:
        data = json.load(fh)

        for k,_ in data["devDependencies"].iteritems():
            print k.encode('utf-8')

        #for k,_ in data["dependencies"].iteritems():
        #    print k.encode('utf-8')

