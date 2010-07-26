import re
import anydbm
import os
from .stdio import File, Errors

class ConfError(Exception):
	pass


class Conf:

	fconf = "~/.frozenrc"
	errors = Errors()
	conf = {}

	def __init__(self,conf="~/.frozenrc"):

		self.fconf = conf
		if os.access("conf.db",os.R_OK):
			if os.stat(File.parse(conf)).st_mtime > os.stat("conf.db").st_mtime:
				self.parse()
			else:
				f = anydbm.open("conf.db")
				for k,v in f.items():
					self.conf[k]=v
		else:
			self.parse()
			Conf.compile_dict(self.conf)

	def parse(self):
		""" Open the configuration file and save its values
		in a dictionary. It is run by the constructor, you
		don't need to call this method """
		with open(File.parse(self.fconf),"r") as f:
			C=0
			for i in f.readlines():
				C+=1
				if i[0] == '#' or i=="\n":
					continue
				t = re.match(r"(\w+?)\s*=\s*(.+?)\s*(?:#.*)?$",i)
				if not t:
					self.errors.write("Error on line {} : Not matched".format(C-1))
					continue
				else:
					self.to_diz(t)

	def to_diz(self,matchObj):
		""" It puts parsed values into conf dictionary.
		You should not use this method """
		if not matchObj:
			self.errors.write("Fatal error {to_diz}")
			return

		k,v = matchObj.groups()
		self.conf[k] = eval(v)

	@staticmethod
	def compile_dict(conf,filename="./conf.db"):
		"""Compiles the configuration hash into a
		fastest form for further uses """
		with anydbm.open(File.parse(filename),'n') as db:
			for i in conf.keys():
				db[i] = conf[i]

	def query(self,key):
		""" Returs a configuration value """
		try:
			return self.conf[key]
		except KeyError:
			raise ConfError("Incomplete configuration: {} key not found".format(key))
