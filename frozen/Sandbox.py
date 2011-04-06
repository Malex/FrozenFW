import imp
from .File import File

IMPORT = 1
EXEC = 2

class Sandbox():
	__vars = []
	__new_limits = []

	def __init__(self,allowed_vars :list=None,new_limits :list=None,log=None):
		if allowed_vars:
			self.allowed_vars = allowed_vars
		if new_limits:
			self.new_limits = new_limits
		self.log = log

	@property
	def allowed_vars(self) -> list:
		return self.__vars
	@allowed_vars.setter
	def allowed_vars(self,lis :list):
		for i in lis:
			self.__vars.append(i)

	@property
	def new_limits(self) -> list:
		return self.__new_limits
	@new_limits.setter
	def new_limits(self,lis :list):
		self.__new_limits = lis

	def __call__(self,filename :str,mode = EXEC,glob :dict=globals()):
		if mode == EXEC:
			a,b,c = File.valid_path,File.blacklist,File.whitelist
			File.set_limits(*tuple(self.new_limits))
			p_dict = {}
			for i in self.__vars:
				p_dict[i] = glob[i]
			exec(File.get_contents(filename),p_dict)
			File.valid_path,File.blacklist,File.whitelist = a,b,c
			glob.update(p_dict)
			return
		elif mode == IMPORT:
			if self.log:
				self.log.notice("IMPORT not implemented yet. Skipping istruction")
			return
		else:
			raise ValueError("EXEC or IMPORT value expected")
