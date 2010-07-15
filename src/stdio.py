import os
import re
from platform import system
from datetime import date
from sys import stdout
import atexit

class File:

	### ???????????????????????
	def set_re(cls,limit="~/*"):
		cls.reg = re.compile(File.parse(limit).replace("*",".*"))
	### ???????????????????????

	def __init__(self,filename,mode):
		if mode not in ['r','w','a','rb','wb','ab','r+','w+','a+']:
			raise ValueError("Not supported filemode {}".format(mode))

		filename = File.parse(filename)
		if not os.access(filename,os.F_OK):
			raise IOError("{} : Not such file/Directory".format(filename))
		try:
			self._handle = open(filename,mode)
		except:
			raise IOError("{0} : Not correct privileges ({1})".format(filename,mode))
		self._mode = mode
		self._filename = filename

	@staticmethod
	def parse(f):
		""" Converts the File string. Replace ~ with Home Directory """
		if re.search(r"~/.*",f):
			folder = os.getenv("HOME")
			re.sub(r"~/(.*)",folder+"\1",f)
		if system() == "Windows":
			f.replace("/","\\")
		return f

	def read(self,size=-1):
		""" Read the file (if possible). Optional
		paramether chars specify how many characters read """
		if '+' in self._mode or self._mode == 'r':
			return self._handle.read(size)
		else:
			raise IOError("Reading not allowed")

	def write(self,data):
		if '+' in self._mode or self._mode in ['w','a','wb','ab']:
			self._handle.write(data)
		else:
			raise IOError("Writing not allowed")

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

	def __init__(self,path="/var/log/frozen"):
		if not os.access(path,os.F_OK):
			os.mkdir(path)
		self.path = path

		self.dt = date.today().ctime().replace(" ",".")
		if not os.access(self.dt+".log",os.F_OK):
			self._mode = 'w'
		else:
			self._mode = 'a'

	def __add__(self,s):
		self.log += (s+'\n')
		return self

	def write(self,s):
		self.log += (s+'\n')

	@atexit.register
	def do(self):
		self._handle = open(self.dt+".log",self._mode)
		self._handle.write(self.log)
		self._handle.close()

class Output(Output):

	rep = {}
	_handle = stdout

	def __init__(self,path="template.html"):
		if not os.access(path,os.R_OK):
			raise IOError("Not valid template")
		else:
			self.data = File.get_contents(path)

	def set_template(self,path):
		self.data = File.get_contents(path)

	def write(self,key,value):
		rep[key] = value

	@atexit.register
	def do(self):
		self._handle.write(self.data.format(**rep))


