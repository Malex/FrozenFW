import re

from os.path import expanduser,normcase

class FileError(Exception):
	pass

class File():

	valid_path = re.compile(r".+")
	blacklist = []
	whitelist = []

	@classmethod
	def set_limits(cls,valid_path :str,blacklist :str,whitelist :str):
	""" Set limits for open function """
		cls.valid_path = re.compile(File.parse(valid_path))
		cls.blacklist = [re.compile(File.parse(a)) for a in blacklist]
		cls.whitelist = [re.compile(File.parse(b)) for b in whitelist]

	@classmethod
	def check(cls,filename :str) -> bool:
	""" Check if given filename is into limits. Used by open"""
		if ( not cls.valid_path.match(filename) and not any([a.match(filename) for a in cls.whitelist])  ) or any([a.match(filename) for a in cls.blacklist]):
			return False
		else:
			return True

	@staticmethod
	def parse(f :str) -> str:
		""" Converts the File string. Replace ~ with Home Directory (use ~user for different user) and on Windows replace / with \\"""
		return normcase(expanduser(f))

	@staticmethod
	def get_contents(path :str) -> str:
		""" Returns the file contents very fast """
		with File.open(path) as t:
			return t.read()

def open(filename :str,mode :chr='r',*args,**kwargs):
	__doc__ = __builtins__['open'].__doc__
	filename = File.parse(filename)
	_handle = __builtins__['open'](filename,mode,*args,**kwargs)
	if File.check(filename):
		return _handle
	else:
		raise FileError("File not in limits")

File.open = open
