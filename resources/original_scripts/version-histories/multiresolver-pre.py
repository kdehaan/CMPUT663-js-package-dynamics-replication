import json
import subprocess

from loader import Loader

# This script is designed to feed into version-resolver.js, then into *-post.py.
class MultiResolverPre:
    @classmethod
    def resolve_all_queries(cls, db, package_name):
        (intervals, latest_ts) = cls.query_intervals(db, package_name)

        if latest_ts is None:
            return

        releases = cls.versions_earlier_than(db, package_name, latest_ts)

        if releases:
            (versions, release_dates) = zip(*releases)

            for (qs, start_ts, end_ts) in intervals:
                cls.resolve(package_name, qs, start_ts, end_ts, versions, release_dates)

    @classmethod
    def versions_earlier_than(cls, db, package_name, ts):
        versions = []

        db.cursor.execute("""
            SELECT
                `version`, `released`
            FROM
                `packages`,
                `package_versions`
            WHERE
                `packages`.`id`=`package_versions`.`package_id` AND
                `packages`.`name`=%s
            ORDER BY
                `released` ASC;""", package_name)

        for (version, released) in db.cursor.fetchall():
            versions.append((version, Loader.dt2ts(released)))

        return versions

    @classmethod
    def query_intervals(cls, db, package_name):
        
        # This will get you all the query strings ever used for that package,
        # together with first-seen and last-seen dates.
        db.cursor.execute("""
            SELECT
                `packages`.`id` AS `package_id`,
                `packages`.`name` AS `package_name`,
                `deps`.`version_query`,
                MIN(`deps`.`started`) AS `first_started`,
                MAX(`deps`.`ended`) AS `last_ended`
            FROM
                `packages`,
                `project_explicit_dependencies` AS `deps`
            WHERE
                `packages`.`id`=`deps`.`package_id` AND
                `packages`.`name`=%s
            GROUP BY
                `packages`.`id`,
                `deps`.`version_query`;""", package_name)

        stored_rows = []
        latest_ts = -1

        # Each row is a specific query string
        for row in db.cursor.fetchall():
            (pkg_id, pkg_name, qs, first_started, last_ended) = row
            first_ts = Loader.dt2ts(first_started)
            last_ts  = Loader.dt2ts(last_ended)
            stored_rows.append((qs, first_ts, last_ts))

            latest_ts = max(latest_ts, last_ts) 

        return (stored_rows, latest_ts if latest_ts != -1 else None)                

    @classmethod
    def resolve(cls, package_name, query, first_ts, last_ts, versions, release_dates):
        # Assumes versions is sorted by _._2
        l = 0
        u = -1
        for i in xrange(0, len(release_dates)):
            if release_dates[i] < first_ts:
                l = i
            if release_dates[i] > last_ts:
                u = i
                break

        if u == -1:
            u = len(release_dates)
        else:
            # We take one more, if we can, so that all queries fall in closed intervals.
            u = min(u+1, len(release_dates))

        for j in range(l+1,u+1):
            try:
                print json.dumps({
                    "p"  : package_name,
                    "vq" : query,
                    "at" : release_dates[j-1],
                    "vs" : versions[0:j]
                })
            except:
                pass

    @classmethod
    def all_declared_dependent_packages(cls, db):
        db.cursor.execute("""
            SELECT DISTINCT
                `packages`.`name`
            FROM
                `packages`, `project_explicit_dependencies` AS `deps`
            WHERE
                `packages`.`id`=`deps`.`package_id`;"""
        )

        packages = []
        for name in db.cursor.fetchall():
            packages.append(name[0])

        return packages

if __name__ == "__main__":
    import sys
    from db import DB

    db = DB()

    if len(sys.argv) > 1:    
        MultiResolverPre.resolve_all_queries(db, sys.argv[1])
    else:
        pkgs = MultiResolverPre.all_declared_dependent_packages(db)
        done = 0
        for pkg in pkgs:
            MultiResolverPre.resolve_all_queries(db, pkg)
            done += 1
            if done % 10 == 0:
                sys.stderr.write(".")
