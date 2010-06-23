import re
from os import getenv
from platform import system
from datetime import date
import anydbm

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
	errors = "Log of {}\n".format(date.today().ctime())
	conf = {}

	def __init__(self,conf="~/.frozenrc"):

		self.fconf = conf
		self.parse()

	def parse(self):
		""" Open the configuration file and save its values
		in a dictionary. It is run by the constructor, you
		don't need to call this method """
		with open(parse(self.fconf),"r") as f:
			C=0
			for i in f.readlines():
				C+=1
				if i[0] == '#':
					continue
				t = re.match(r"(\w)+\s*=\s*(\w)+?(?<=#).*",i)
				if not t:
					self.errors += "Error on line {} : Not matched".format(C-1)
					continue
				else:
					self.to_diz(t)

	def write_log(self):
		""" Write errors into log file """
		if len(self.errors.readlines())>1:
			with open("/var/log/frozen.log",'a') as a: #put choice capability
				a.write(self.errors)
				self.errors = "Log of {}\n".format(date.today().ctime())


	def to_diz(self,matchObj):
		""" It puts parsed values into conf dictionary.
		You should not use this method """
		if not matchObj:
			self.errors += "Fatal error {to_diz}"
			return

		k,v = matchObj.groups()
		self.conf[k] = eval(v)

	def compile_dict(self):
		pass
