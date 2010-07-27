import os
import re
from platform import system
from datetime import date
import sys

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

	def __init__(self,filename,mode="r"):
		if mode not in ['r','w','a','rb','wb','ab','r+','w+','a+']:
			raise FileError("Not supported filemode \"{}\"".format(mode))

		filename = File.parse(filename)
		if not os.access(filename,os.F_OK):
			raise FileError("{} : Not such file/Directory".format(filename))

		if ( not re.match(self.valid_path,filename) and not any([re.match(a,filename) for a in self.whitelist])  ) or any([re.match(a,filename) for a in self.blacklist]):
			raise FileError("File out of limit")

		try:
			self._handle = open(filename,mode)
		except:
			raise FileError("{0} : Not correct privileges ({1})".format(filename,mode))
		self._mode = mode
		self._filename = filename

	@staticmethod
	def parse(f):
		""" Converts the File string. Replace ~ with Home Directory """
		if re.match(r"~/.*",f):
			folder = os.getenv("HOME")
			f = re.sub(r"~(/.*)",lambda m : folder+m.groups()[0],f)
		if system() == "Windows":
			f.replace("/","\\")
		return f

	def read(self,size=-1):
		""" Read the file (if possible). Optional
		paramether chars specify how many characters read """
		if '+' in self._mode or self._mode == 'r':
			return self._handle.read(size)
		else:
			raise FileError("Reading not allowed")

	def write(self,data):
		if '+' in self._mode or self._mode in ['w','a','wb','ab']:
			self._handle.write(data)
		else:
			raise FileError("Writing not allowed")

	@staticmethod
	def get_contents(path):
		""" Returns the file contents very fast """
		t = File(path)
		return t.read()

	##TO IMPROVE
	def __enter__(self):
		pass

	def __exit__(self):
		self._handle.close()


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
			sys.__stdout__.write(self.headers+"\r\n")
		sys.__stdout__.write("\r\n")
		sys.__stdout__.write(self.data.format(**self.rep))


