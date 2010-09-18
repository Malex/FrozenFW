import re
import sys
from .File import File

class ConfError(Exception):
	pass

class Conf:

	conf = {}

	def __init__(self,file :str="~/etc/frozenrc"):
		self.conf = self.parse(file)
		try:
			self.update_conf(self.query("conf_chain"))
		except ConfError:
			pass

	def parse(self,file :str) -> dict:
		""" Open the configuration file and save its values
		in a dictionary. It is run by the constructor, you
		don't need to call this method """
		with open(File.parse(file),"r") as f:
			C=0
			tmp={}
			for i in f.readlines():
				C+=1
				if i[0] == '#' or i=="\n":
					continue
				t = re.match(r"(\w+?)\s*=\s*(.+?)\s*(?:#.*)?$",i)
				if not t:
					sys.stderr.write("Error on line {} : Not matched".format(C-1))
				else:
					try:
						self.to_diz(t,tmp)
					except AssertionError as e:
						sys.stderr.write(repr(e))
			return tmp

	def to_diz(self,matchObj,diz):
		""" It puts parsed values into conf dictionary.
		You should not use this method """
		assert matchObj,"Fatal error {to_diz}"
		k,v = matchObj.groups()
		diz[k] = v

	def query(self,key :str):
		""" Returs a configuration value """
		try:
			return eval(self.conf[key])
		except KeyError as e:
			raise ConfError("Incomplete configuration: {} key not found".format(key)) from e

	def update_conf(self,path :str):
		""" Add Conf values from another conf file. Note that values may be overridden """
		t = self.parse(path)
		self.conf.update(t)
