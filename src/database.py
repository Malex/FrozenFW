from stdio import File
import sqlite3
import atexit
import re

class SQL:
	""" Parent class for generic SQL support """

	@staticmethod
	def addslashes(s):
		return re.sub("([\\\"\'\0)","\\\1",s)


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

	def raw_query(self,q):
		self.db.execute(SQL.addslashes(q))
		return self.db

	@atexit
	def do(self):
		self._conn.commit()
		self.db.close()

"""class Query:

	def __init__(self,db_driver):
		self.query =
"""

class DB:

	self.db_hash = {}

	def raw_query(self,string):
		self.driver.query(string)

	def __init__(self,db_type,filename="./data.db"):
		self.driver = globals()[db_type](File.parse(filename))

"""	def __getitem__(self,*args):
		i = 0
		tmp =self.db_hash
		while i<len(args):
			try:
				old = tmp
				tmp = tmp[args[i]]
			except IndexError:
				raise IOError("Key not in database")
			if type(tmp)==str or type(tmp)==list:
				return tmp
			elif type(tmp)==dict:
				i+=1
			else:
				try:
					if tmp.__name__ == "Query":
						old[args[i]] = tmp.do_query()
				except:
					raise TypeError("not valid type in class")


"""
