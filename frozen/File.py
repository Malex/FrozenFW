import fnmatch
import os

from os.path import expanduser,normcase,expandvars,isfile,join

class FileError(Exception):
	pass

class File():

	base_dir = ""

	valid_path = ""
	blacklist = []
	whitelist = []

	@classmethod
	def inlist(cls, f :str) -> list:
		if isfile(f):
			return [f]
		else:
			to_ret = []
			for curdir,subdir,files in os.walk(cls.base_dir):
				for i in files:
					if fnmatch.fnmatch(join(curdir,i),f):
						to_ret.append(join(curdir,i))
			return to_ret

	@classmethod
	def set_limits(cls,valid_path :str,blacklist :str,whitelist :str):
		""" Set limits for open function.
		Please note that hidden files must be like, for instance, path/to/.*rc"""
		cls.valid_path = set(cls.inlist(File.parse(valid_path)))
		cls.blacklist = [set(cls.inlist(File.parse(a))) for a in blacklist]
		cls.whitelist = [set(cls.inlist(File.parse(b))) for b in whitelist]

	@classmethod
	def check(cls,filename :str) -> bool:
		""" Check if given filename is into limits. Used by open"""
		t = set(cls.inlist(filename))
		if ( t <= cls.valid_path or any(t<=a for a in cls.whitelist)  ) and ( (not any(t<=a for a in cls.blacklist)) or any(t<=a for a in cls.whitelist)):
			return True
		else:
			return False

	@staticmethod
	def parse(f :str) -> str:
		""" Converts the File string. Replace ~ with Home Directory (use ~user for different user) and on Windows replace / with \\"""
		t = normcase(expandvars(expanduser(f)))
		return t if t.startswith('/') or t[1:3]==':\\' else join(File.base_dir,t)

	@staticmethod
	def get_contents(path :str) -> str:
		""" Returns the file contents very fast """
		with File.open(path) as t:
			return t.read()

def open(filename :str,mode :chr='r',*args,**kwargs):
	__doc__ = __builtins__['open'].__doc__
	filename = File.parse(filename)
	if File.check(filename):
		return __builtins__['open'](filename,mode,*args,**kwargs)
	else:
		raise FileError("{}: File not in limits".format(filename))

File.open = open
