from .stdio import File
import re
from sqlobject import *

class SQL():
	"Parent Class for SQL common operations"
	
	tables = {}

	@staticmethod
	def addslashes(s):
		return re.sub("([\\\"\'\0)","\\\1",s)

	def createTable(self,table_name,*str_cols,**other_cols):
		self.tables[table_name] = type(table_name,(SQLObject,),zip(str_cols,(StringCol(),)*len(str_cols)).update(other_cols))
	
	def select(self,table_name,*args,**kwargs):
		"""*args could be empty, unless you know what you are doing.
		kwargs should contain the query column(s)"""
		return self.tables[table_name].selectBy(*args,**kwargs)

class XML():
	def __init__(self,filename):
		pass

class SQLite(SQL):
	def __init__(self,path):
		sqlhub.processConnection = connectionForURI("sqlite://"+path)

class MySQL(SQL):
	def __init__(self,path):
		sqlhub.processConnection = connectionForURI("mysql://"+path)


class DB:

	db_hash = {"SQLite" : SQLite, "MySQL" : MySQL, "XML" : XML}

	def __new__(cls,db_type,path):
		return type("DB",(cls.db_hash[db_type],),{}).__init__(path)
