from stdio import File
import sqlite3
import atexit

class SQL:
	""" Parent class for generic SQL support """

	@staticmethod
	def addslashes(s):
		return s.replace("\"","\\\"")


class MySQL(SQL):
	def __init__(self,filename):
		pass

class XML:
	def __init__(self,filename):
		pass

class SQLite(SQL):

	def __init__(self,filename):
		self._conn = sqlite3.connect(filename)
		self.db = self._conn.cursor()

	def query(self,q):
		self.db.execute(SQL.addslashes(q))
		return self.db

	@atexit
	def do(self):
		self._conn.commit()
		self.db.close()


class DB:

	self.db_hash

	def query(self,string):
		self.driver.query(string)

	def __init__(self,db_type,filename="./data.db"):
		self.driver = globals()[self.db_hash[db_type]](File.parse(filename))
