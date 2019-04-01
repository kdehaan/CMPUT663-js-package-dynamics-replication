import itertools
import re
import sys

from db import DB

if __name__ == "__main__":
    try:
        package = sys.argv[1]
    except:
        print "You need to provide a package name."
        sys.exit(1)

    output_file = sys.argv[0].replace(".py", "-%s.dat" % package)

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

    print "Running query..."
    db.cursor.execute("""
        SELECT
            `packages`.`name` AS `package_name`,
            `package_versions`.`version` AS `version`,
            UNIX_TIMESTAMP(`package_versions`.`released`) AS `released`
        FROM
            `packages` JOIN `package_versions` ON `packages`.`id` = `package_versions`.`package_id`
        WHERE
            `packages`.`name`=%s AND
            `version` REGEXP "^[0-9]+\\.[0-9]+\\.[0-9]+$" AND
            `released` >= "2010-10-01" AND `released` < "2015-09-01"
        ORDER BY
            `released` ASC
    """, package)

    all_rows = []
    current_max = -1;
    for row in db.cursor.fetchall():
        (_, version, released) = row
        (major,minor,patch) = semver(version)
        linearized = triple_to_float(major,minor,patch)

        if linearized <= current_max:
            continue

        current_max = linearized

        all_rows.append((major,minor,patch,linearized,released))

    max_rows = []
    for (ts, rows) in itertools.groupby(all_rows, lambda t: t[4]):
        rows = sorted(list(rows), key=lambda t: -t[3])
        max_rows.append(rows[0]) 

    print "Writing to %s..." % (output_file)
    with open(output_file, "w") as fp:
        fp.write("major,minor,patch,linearized,released\n")
        for row in max_rows:
            (major,minor,patch,linearized,released) = row
            fp.write("%d, %d, %d, %f, %d\n" % row)
