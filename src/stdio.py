from __future__ import print_function
import os
import re
from datetime import date
import sys
from os.path import expanduser,normcase

class FileError(Exception):
	pass

class File():

	valid_path = re.compile(r"\./") 
	blacklist = []
	whitelist = []

	@classmethod
	def set_limits(cls,valid_path,blacklist,whitelist):
		cls.valid_path = re.compile(valid_path)
		cls.blacklist = [re.compile(a) for a in blacklist]
		cls.whitelist = [re.compile(b) for b in whitelist]
	
	@staticmethod
	def check(filename):
		if ( not self.valid_path.match(filename) and not any([a.match(filename) for a in self.whitelist])  ) or any([a.match(filename) for a in self.blacklist]):
			return False
		else:
			return True

	@staticmethod
	def parse(f):
		""" Converts the File string. Replace ~ with Home Directory (use ~user for different user) and on Windows replace / with \\"""
		return normcase(expanduser(f))

	@staticmethod
	def get_contents(path):
		""" Returns the file contents very fast """
		t = File.open(path)
		return t.read()

class Errors():

	path = ""
	log = ""

	def __init__(self,path="./conf.log"):
		path = File.parse(path)
		if not os.access(path,os.F_OK):
			os.mkdir(path)
		self.path = path

		self.dt = date.today().ctime().replace(" ",".")
		if not os.access(os.path.join(path,self.dt+".log"),os.F_OK):
			self._mode = 'w'
		else:
			self._mode = 'a'

	def write(self,s):
		self.log += (s+'\n')

	def flush(self):
		pass #trying to fix

	def writelines(self,s):
		self.write("\n".join(s)) #implementation suggested

	def exit(self):
		self._handle = open(os.path.join(self.path,self.dt+".log"),self._mode)
		self._handle.write(self.log)
		self._handle.close()

class Output():

	rep = {}
	arg = []
	headers = ["Content-Type: text/html"]

	def __init__(self,path="template.html"):
		try:
			Output.set_template(path)
		except FileError:
			raise FileError("Not Valid Template {}".format(path))

	@classmethod
	def set_headers(cls, *args):
		for i in args:
			cls.headers.append(i)
	
	@classmethod
	def set_template(cls,path):
		cls.data = File.get_contents(path)

	def write(self,*args,**kwargs):
		self.arg.extend(list(args))
		self.rep.update(kwargs)

	def exit(self):
		for i in self.headers:
			sys.__stdout__.write(self.i+"\r\n")
		sys.__stdout__.write("\r\n")
		sys.__stdout__.write(self.data.format(*tuple(self.arg),**self.rep))

def print(*args,**kwargs):
	sys.stdout.write(*args,**kwargs)

def open(filename,mode='r',*args,**kwargs):
	__doc__ = __builtin__.open.__doc__
	filename = File.parse(filename)
	_handle = __builtin__.open(filename,mode,*args,**kwargs)
	if File.check(filename):
		return _handle
	else:
		raise FileError("File not in limits")

File.open = open
