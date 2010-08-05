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
		cls.vialid_path = re.compile(File.parse(valid_path))
		cls.blacklist = [re.compile(File.parse(a)) for a in blacklist]
		cls.whitelist = [re.compile(File.parse(b)) for b in whitelist]
	
	@classmethod
	def check(cls,filename):
		if ( not cls.valid_path.match(filename) and not any([a.match(filename) for a in cls.whitelist])  ) or any([a.match(filename) for a in cls.blacklist]):
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

class Output():

	rep = {}
	arg = []
	headers = ["Content-Type: text/html"]

	templ_reg = re.compile(r"@!([\w_]+)\s*#(.+?)#\s*(.+)@!end\s+\1\s*#\2#",re.S)
	f_hash = {}
	sep = '\n'

	def __init__(self,path="template.html"):
		try:
			Output.set_template(path)
		except FileError:
			raise FileError("Not Valid Template {}".format(path))
		self.f_hash['loop'] = self.loop_exec

	@classmethod
	def set_headers(cls, *args):
		for i in args:
			cls.headers.append(i)
	
	@classmethod
	def set_template(cls,path):
		cls.data = File.get_contents(path)

	def loop_exec(self,s,t):
		if not t:
			raise FileError("Fatal Error during templating")
		else:
			try:
				it = self.rep[t.group(2)]
			except KeyError:
				raise FileError("Template Var not found {}".format(t.group(2)))
			else:
				ret = [t.group(3)] * len(it)
				ret = [x.format(**{t.group(2) : y}) for x,y in zip(ret,it)] #tnx chuzz 
				s = s.replace(t.group(0),self.sep.join(ret))
				return s

	def templ_exec(self,s):
		t = self.templ_reg.search(s)
		while t:
			try:
				s = self.f_hash[t.group(1)](s,t)
			except KeyError:
				s = s.replace(t.group(0),t.group(0).replace('@','&at;'))
			t = self.templ_reg.search(s)
		return s	

	def write(self,*args,**kwargs):
		self.arg.extend(list(args))
		self.rep.update(kwargs)

	def exit(self):
		for i in self.headers:
			sys.__stdout__.write(i+"\r\n")
		sys.__stdout__.write("\r\n")
		self.data = self.templ_exec(self.data)
		sys.__stdout__.write(self.data.format(*tuple(self.arg),**self.rep))

def print(*args,**kwargs):
	sys.stdout.write(*args,**kwargs)

def open(filename,mode='r',*args,**kwargs):
	__doc__ = __builtins__['open'].__doc__
	filename = File.parse(filename)
	_handle = __builtins__['open'](filename,mode,*args,**kwargs)
	if File.check(filename):
		return _handle
	else:
		raise FileError("File not in limits")

File.open = open
