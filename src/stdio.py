import os
import re
from platform import system
from datetime import date
import sys
from __future__ import print_function

class FileError(Exception):
	pass

class File:

	valid_path = None
	blacklist = []
	whitelist = []

	@classmethod
	def set_limits(cls,valid_path,blacklist,whitelist):
		cls.valid_path = valid_path
		cls.blacklist = blacklist
		cls.whitelist = whitelist
	
	@staticmethod
	def check(filename):
		if ( not re.match(self.valid_path,filename) and not any([re.match(a,filename) for a in self.whitelist])  ) or any([re.match(a,filename) for a in self.blacklist]):
			return False
		else:
			return True

	@staticmethod
	def parse(f):
		""" Converts the File string. Replace ~ with Home Directory """
		if re.match(r"~/.*",f):
			folder = os.getenv("HOME")
			f = re.sub(r"~(/.*)",lambda m : folder+m.groups()[0],f)
		if system() == "Windows":
			f.replace("/","\\")
		return f

	@staticmethod
	def get_contents(path):
		""" Returns the file contents very fast """
		t = File.open(path)
		return t.read()

class Errors:

	path = ""
	log = ""

	def __init__(self,path="./conf.log"):
		if not os.access(path,os.F_OK):
			os.mkdir(path)
		self.path = path

		self.dt = date.today().ctime().replace(" ",".")
		if not os.access(self.dt+".log",os.F_OK):
			self._mode = 'w'
		else:
			self._mode = 'a'

	def write(self,s):
		self.log += (s+'\n')

	def exit(self):
		self._handle = open(self.dt+".log",self._mode)
		self._handle.write(self.log)
		self._handle.close()

class Output():

	rep = {}
	headers = ["Content-Type: text/html"]

	def __init__(self,path="template.html"):
		try:
			self.data = File.get_contents(path)
		except FileError:
			raise FileError("Not Valid Template {}".format(path))

	@classmethod
	def set_headers(cls, *args):
		for i in args:
			cls.headers.append(i)

	def set_template(self,path):
		self.data = File.get_contents(path)

	def write(self,*args,**kwargs):
		self.rep.update(**kwargs)

	def exit(self):
		for i in self.headers:
			sys.__stdout__.write(self.i+"\r\n")
		sys.__stdout__.write("\r\n")
		sys.__stdout__.write(self.data.format(**self.rep))

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
