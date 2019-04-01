from datetime import datetime
from datetime import tzinfo
import dateutil.parser
import glob
import json
import pytz
import re

from db import DB
from datasources import DataSources

class Loader:
    @classmethod
    def dt2ts(cls, dt):
        if dt.tzinfo is not None:
            return long((dt - datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds())
        else:
            return long((dt - datetime(1970, 1, 1)).total_seconds())
        
    @classmethod
    def string2ts(cls, d):
        dt = dateutil.parser.parse(d)
        return cls.dt2ts(dt)

    @classmethod
    def load_package_names(cls, db):
        print "Loading package names..."
        print "  - loading JSON representation"
        with open(DataSources.npm_packages) as fp:
            data = json.load(fp)

        print "  - computing unique set"
        all_names = set([])
        for obj in data:
            name = obj.get("value", {}).get("name", None)
            if isinstance(name, basestring):
                all_names.add(name)

        print "  - inserting into database"
        for name in all_names:
            db.cursor.execute("INSERT INTO `packages` (`name`) VALUES(%s)", name)
        db.commit()

    @classmethod
    def load_package_versions(cls, db):
        print "Loading package versions..."
        print "  - inserting from JSON lines to DB"
        with open(DataSources.npm_full) as fp:
            for line in fp:
                data = json.loads(line)
                name = data.get("name", None)
                if not isinstance(name, basestring):
                    continue

                try:
                    versions = data.get("time", {})
                    if not isinstance(versions, dict):
                        continue

                    for v,d in versions.iteritems():
                        try:
                            ts = cls.utc2ts(d)
                        except:
                            print "  - couldn't parse/convert date value for %s-%s: %s" % (name, v, d)
                            continue

                        db.cursor.execute("INSERT INTO `package_versions` (`package_id`, `version`, `released`) SELECT `id`, %s, FROM_UNIXTIME(%s) FROM `packages` WHERE `packages`.`name`=%s", (v, ts, name))

                    db.commit()
                except Exception, e:
                    print "  - error when processing %s: %s" % (name, str(e))

        print "  - cleanup"
        db.cursor.execute("""DELETE FROM `package_versions` WHERE NOT (`released` BETWEEN "2007-01-01" AND NOW())""")
        db.cursor.execute("""DELETE FROM `package_versions` WHERE `version`="created" """)

    @classmethod
    def load_project_data(cls, db):
        from githubhistory import GitHubHistory

        print "Loading GitHub project data..."
        print "  - loading all names from files"
        for fn in glob.glob(DataSources.project_history_dir + "/*.json"):
            try:
                gh = GitHubHistory(fn)

                db.cursor.execute("INSERT INTO `projects` (`user`, `repo`) VALUES(%s, %s)", (gh.user, gh.repo))

                intervals = gh.get_intervals()

                for k in [ "dependencies", "devDependencies" ]:
                    for i in intervals.get(k, {}):
                        db.cursor.execute(
"""
INSERT INTO `project_explicit_dependencies`
    (`project_id`, `package_id`, `is_dev_dependency`, `version_query`, `started`, `ended`)
    SELECT
        `projects`.`id`, `packages`.`id`, %s, %s, FROM_UNIXTIME(%s), FROM_UNIXTIME(%s)
    FROM `projects`, `packages`
        WHERE
            `projects`.`user`=%s AND `projects`.`repo`=%s AND
            `packages`.`name`=%s 
""",
                            (
                                k != "dependencies",
                                i["version"],
                                cls.string2ts(i["from"]),
                                cls.string2ts(i["to"]),
                                gh.user,
                                gh.repo,
                                i["package"]
                            )
                        )

            except Exception, e:
                print "  - error when processing %s: %s" % (fn, str(e))

            db.commit()
    
if __name__ == "__main__":
    db = DB()

    # Loader.load_package_names(db)
    # Loader.load_package_versions(db)
    Loader.load_project_data(db)
