import re
import shelve
import os
import sys
from .stdio import File

class ConfError(Exception):
	pass

class Conf:

	fconf = "/etc/frozenrc"
	conf = {}

	def __init__(self,conf="~/etc/frozenrc"):

		self.fconf = conf
		if os.access("conf.db",os.R_OK):
			if os.stat(File.parse(conf)).st_mtime > os.stat("conf.db").st_mtime:
				self.parse()
			else:
				f = shelve.open("conf.db")
				for i in f.keys():
					self.conf[i] = f[i]
		else:
			self.parse()
			
			try:
				self.update_conf(self.query("conf_chain"))
			except ConfError:
				pass

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
					sys.stderr.write("Error on line {} : Not matched".format(C-1))
					continue
				else:
					self.to_diz(t)

	def to_diz(self,matchObj):
		""" It puts parsed values into conf dictionary.
		You should not use this method """
		if not matchObj:
			sys.stderr.write("Fatal error {to_diz}")
			return

		k,v = matchObj.groups()
		self.conf[k] = v

	@staticmethod
	def compile_dict(conf :dict,filename :str ="./conf.db"):
		"""Compiles the configuration hash into a
		fastest form for further uses """
		db = shelve.open(File.parse(filename),writeback=True)
		for i in conf.keys():
			db[i] = conf[i]
		db.close()

	def query(self,key :str):
		""" Returs a configuration value """
		try:
			return eval(self.conf[key])
		except KeyError as e:
			raise ConfError("Incomplete configuration: {} key not found".format(key)) from e

	def update_conf(self,path :str):
		""" Add Conf values from another conf file. Note that values may be overridden """
		t = Conf(path)
		self.conf.update(t.conf)
		del t
