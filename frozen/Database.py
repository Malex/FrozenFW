
class DB():

	def __init__(self,server :str="localhost", port :int=27107,db :str="test-database"):
		pass

	def create_table(self,name :str) -> object:
		""" Creates a table and return it """
		pass

	def insert(self,table :str,value :dict):
		""" Insert a value into a table """
		pass

	def remove(self,table :str,v_id :dict):
		""" Remove a line from a table """
		pass

	def find(self,table :str,value :dict,limit :int=1) -> object:
		""" Find objects and returns them """
		pass
