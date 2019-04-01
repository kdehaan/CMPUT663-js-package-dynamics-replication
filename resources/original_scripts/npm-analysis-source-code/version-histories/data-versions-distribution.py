import re
import sys
import numpy

from db import DB

if __name__ == "__main__":
    output_file = sys.argv[0].replace(".py", ".dat")

    def semver(v):
        m = re.match("""([0-9]*)\.([0-9]*)\.([0-9]*)""", v)
        major = int(m.group(1))
        minor = int(m.group(2))
        patch = int(m.group(3))
        return (major, minor, patch)

    def triple_to_float(major, minor, patch):
        K = 0.5
        m = float(major)
        M = float(minor)
        p = float(patch)

        M_p = M + 1.0 - (1.0 / (K*p + 1.0))
        m_M_p = m + 1.0 - (1.0 / (K*M_p + 1.0))

        return m_M_p

    db = DB()

    all_semver = db.cursor.execute("""
        SELECT
            `version`, COUNT(*) AS `how_many` 
        FROM
            `package_versions`
        WHERE
            `version` REGEXP "^[0-9]+\\.[0-9]+\\.[0-9]+$"
        GROUP BY
            `version`
        ORDER BY
            `how_many` DESC
        ;
    """)

    all_triples = []
    all_major   = []
    all_minor   = []
    all_patch   = []

    triple_counts = {}

    for row in db.cursor.fetchall():
        version = row[0]
        count   = int(row[1])

        triple = semver(version)

        before = triple_counts.get(triple, 0)
        triple_counts[triple] = before + count

    print "Writing to %s..." % (output_file)
    with open(output_file, "w") as fp:
        fp.write("major,minor,patch,linearized,count\n")
        for triple,count in triple_counts.iteritems():
            (major, minor, patch) = triple
            linearized = triple_to_float(major, minor, patch)
            fp.write("%d, %d, %d, %f, %d\n" % (major, minor, patch, linearized, count))
