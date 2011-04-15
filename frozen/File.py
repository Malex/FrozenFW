import glob

from os.path import expanduser,normcase,expandvars

class FileError(Exception):
	pass

class File():

	base_dir = ""

	valid_path = glob.glob("*")
	blacklist = []
	whitelist = []

	@classmethod
	def set_limits(cls,valid_path :str,blacklist :str,whitelist :str):
		""" Set limits for open function.
		Please note that hidden files must be like, for instance, path/to/.*rc"""
		cls.valid_path = set(glob.glob(File.parse(valid_path)))
		cls.blacklist = [set(glob.glob(File.parse(a))) for a in blacklist]
		cls.whitelist = [set(glob.glob(File.parse(b))) for b in whitelist]

	@classmethod
	def check(cls,filename :str) -> bool:
		""" Check if given filename is into limits. Used by open"""
		t = set(glob.glob(filename))
		if ( t <= cls.valid_path or any(t<=a for a in cls.whitelist)  ) and ( (not any(t<=a for a in cls.blacklist)) or any(t<=a for a in cls.whitelist)):
			return True
		else:
			return False

	@staticmethod
	def parse(f :str) -> str:
		""" Converts the File string. Replace ~ with Home Directory (use ~user for different user) and on Windows replace / with \\"""
		t = normcase(expandvars(expanduser(f)))
		return t if t.startswith('/') or t[1:3]==':\\' else "{}/{}".format(File.base_dir,t)

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
		raise FileError("File not in limits")

File.open = open
