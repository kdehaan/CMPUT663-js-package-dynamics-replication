import sys
import MySQLdb

class DB:
    def __init__(self):
        self.db = MySQLdb.connect(host="localhost", user="npmversions", passwd="password", db="npmversions")
        self.cursor = self.db.cursor()

    def commit(self):
        self.db.commit()
