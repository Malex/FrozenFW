import pymongo

class DB():

	__conn = None
	tables = {}

	def __init__(self,server :str="localhost", port :int=27107,db :str="test-database"):
		self.__conn = Connection(server,port)
		self.db = self.__conn[db]

	def create_table(self,name :str):
		""" Creates a table and return it """
		self.tables[name] = self.db[name]
		return self.tables[name]

	def insert(self,table :str,value :dict):
		""" Insert a value into a table """
		self.tables[table].insert(value)

	def remove(self,table :str,v_id :dict):
		""" Remove a line from a table """
		self.tables[table].remove(v_id)

	def find(self,table :str,value :dict,limit :int=1):
		""" Find objects and returns them """
		if limit == 1:
			return self.tables[table].find_one(value)
		else:
			return self.tables[table].find(value).limit(limit)
