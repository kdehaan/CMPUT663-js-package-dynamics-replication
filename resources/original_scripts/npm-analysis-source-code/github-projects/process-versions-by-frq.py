import re
import sys

standard = 0
non_standard = 0

with open(sys.argv[1]) as frq_file:
    for line in frq_file:

        line = line.strip()

        m = re.match("""^ *(\d)* (.*)$""", line)

        if m is None:
            print "Can't match: [%s]." % line
            sys.exit(1)

        count = int(m.group(1))

        vstr = m.group(2)

        m = re.match("""^(\d\d*)\.(\d\d*)\.(\d\d*)$""", vstr)

        if m is None:
            print vstr
            non_standard += count
        else:
            standard += count


print "Simple semver     : %d" % standard
print "Non-simple semver : %d  (%4f%%)" % (non_standard, 100.0 * float(non_standard) / float(non_standard + standard))
