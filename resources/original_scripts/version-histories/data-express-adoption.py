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
        
        # THIS IS SPECIFIC TO EXPRESS
        return m + M / 22.0 + p / (13.0 * 22.0)

        return m_M_p

    db = DB()

    db.cursor.execute("""
SELECT
    `rd`.`version`,
    `rd`.`released` AS `released`,
    UNIX_TIMESTAMP(`rd`.`released`) AS `ts`,
    `rd`.`resolvable_dependents` AS `resolvable`,
    `ad`.`resolved_dependents` AS `resolved`,
    `ad`.`resolved_dependents` / `rd`.`resolvable_dependents` AS `fraction`
FROM
    `resolvable_dependents` `rd`
        LEFT OUTER JOIN 
    `resolved_dependents` `ad`
        ON
    `rd`.`version` = `ad`.`version`
WHERE
    `rd`.`package_id` = `ad`.`package_id` AND
    `rd`.`version` = `ad`.`version` AND
    `rd`.`released` > "2012-10-15"
ORDER BY
    `released`
;
    """)

    all_triples = []
    all_major   = []
    all_minor   = []
    all_patch   = []

    triple_counts = {}

    print "Writing to %s..." % (output_file)
    with open(output_file, "w") as fp:
        fp.write("major,minor,patch,linearized,ts,frac\n")

        for row in db.cursor.fetchall():
            version = row[0]
            ts      = row[2]
            frac    = row[5]
            triple  = semver(version)
            (major,minor,patch) = triple
            linearized = triple_to_float(major, minor, patch)

            fp.write("%d, %d, %d, %f, %d, %f\n" % (major, minor, patch, linearized, ts, frac))
