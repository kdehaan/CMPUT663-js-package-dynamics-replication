import json
import fileinput

from db import DB

def store_row(db, row):
    package_name   = row["p"]
    version_query  = row["vq"]
    result_version = row["vr"]
    started        = row["from"]
    ended          = row["to"]

    db.cursor.execute("""
        INSERT INTO `version_query_resolutions`
            (`package_id`, `version_query`, `result_version`, `started`, `ended`)
        SELECT
            `packages`.`id`, %s, `pv`.`id`, FROM_UNIXTIME(%s), FROM_UNIXTIME(%s)
        FROM
            `packages`, `package_versions` AS `pv`
        WHERE
            `packages`.`name`=%s AND
            `packages`.`id`=`pv`.`package_id` AND
            `pv`.`version`=%s;
    """, (version_query, started, ended, package_name, result_version))

if __name__ == "__main__":
    db = DB()

    for line in fileinput.input():
        data = json.loads(line)
        store_row(db, data)

    db.commit()
