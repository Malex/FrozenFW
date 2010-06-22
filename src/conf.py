import re
from os import getenv
from platform import system
from datetime import date

def parse(f):
	""" Converts the File string. Replace ~ with Home Directory """
	if re.search(r".*/~/.*",f):
		folder = os.getenv("HOME")
		re.sub(r"(.*)/~/(.*)","\1"+folder+"\2",f)
		if system() == "Windows":
			f.replace("/","\\")
	return f

class Conf:

	fconf = "~/.frozenrc"
	errors = "Log of {}".format(date.today().isoformat())

	def __init__(self,conf="~/.frozenrc"):

		self.fconf = conf
		self.parse()

	def parse(self):
		""" Open the configuration file and save its values
		in a dictionary. It is run by the constructor, you
		don't need to call this method """
		with self.file = open(parse(self.fconf),"r"):
			C=0
			for i in self.file.readlines():
				C+=1
				if i[0] == '#':
					continue
				t = re.match(r"(\w)+\s*=\s*(\w)+?(?<=#).*",i)
				if not t:
					self.errors += "Error on line {} : Not matched".format(C-1)
					continue
				else:
					pass #//TODO

	def write_log(self):
		if len(self.errors.readlines())>1:
			a = open("/var/log/frozen.log",'a') #put choice capability
			a.write(self.errors)
			a.close()

