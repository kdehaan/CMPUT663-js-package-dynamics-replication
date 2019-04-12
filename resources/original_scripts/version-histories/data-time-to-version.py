import re
import sys

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

    print "Running query..."
    db.cursor.execute("""
        SELECT
            `version`,
            COUNT(*) AS `count`,
            AVG(`time_diff`) AS `avg_time_to_version`,
            MIN(`time_diff`) AS `min_time_to_version`,
            MAX(`time_diff`) AS `max_time_to_version`
        FROM (
            SELECT
                `pv`.`package_id`,
                `pv`.`version`,
                `pv`.`released`,
                `sub`.`first_released`,
                TIMESTAMPDIFF(SECOND, `sub`.`first_released`, `pv`.`released`) AS `time_diff`
            FROM
                `package_versions` `pv`
                INNER JOIN
                (
                    SELECT
                        `package_id`,
                        MIN(`released`) AS `first_released`
                    FROM
                        `package_versions`
                    GROUP BY
                        `package_id`
                ) `sub`
                ON `pv`.`package_id` = `sub`.`package_id`
        ) `xxx`
        WHERE
            `version` REGEXP "^[0-9]+\\.[0-9]+\\.[0-9]+$"
        GROUP BY
            `version`;
    """)

    print "Writing to %s..." % (output_file)
    with open(output_file, "w") as fp:
        fp.write("major,minor,patch,linearized,count,avg_time,min_time,max_time\n")

        for row in db.cursor.fetchall():
            (version, count, avg_time, min_time, max_time) = row
            (major,minor,patch) = semver(version)
            linearized = triple_to_float(major,minor,patch)

            if count >= 100 and linearized <= 10.001:
                fp.write("%d,%d,%d,%f,%d,%f,%f,%f\n" % (major,minor,patch,linearized,count,avg_time,min_time,max_time))

