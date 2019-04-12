#!/usr/bin/env python
from db import DB

if __name__ == "__main__":
    db = DB()

    query = """
        SELECT 
            `table_name`,
            ROUND(((data_length + index_length) / 1024 / 1024), 2)
            FROM information_schema.TABLES where `table_schema`="npmversions"
            ORDER BY (data_length + index_length) DESC;
     """

    db.cursor.execute(query)
    print "%-40s %10s" % ("Table name", "Size")
    print "%-40s-%10s" % ("-" * 40, "-" * 10)
    for row in db.cursor.fetchall():
        if row[1] is None:
            size = "%10s" % "----"
        else:
            size = "%7.2f MB" % row[1]

        print "%-40s %10s" % (row[0], size)
