import os
import re
from platform import system

class File:

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
		if re.search(r".*/~/.*",f):
			folder = os.getenv("HOME")
			re.sub(r"(.*)/~/(.*)","\1"+folder+"\2",f)
		if system() == "Windows":
			f.replace("/","\\")
		return f

	def read(self,size=-1):
		""" Read the file (if possible). Optional paramether chars specify how many characters read """
		if '+' in self._mode or self._mode == 'r':
			return self._handle.read(size)
		else:
			raise IOError("Reading not allowed")






