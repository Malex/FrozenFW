
class Sandbox():
	__vars = {}
	__new_limits = []

	def __init__(self,allowed_vars :list=None,new_limits :list=None):
		if allowed_vars:
			self.allowed_vars = allowed_vars
		if new_limits:
			self.new_limits = new_limits

	@property
	def allowed_vars(self) -> dict:
		return self.__vars
	@allowed_vars.setter
	def set_vars(self,lis :list):
		for i in lis:
			self.__vars.update(i,globals()[i])

	@property
	def new_limits(self) -> list:
		return self.__new_limits
	@new_limits.setter
	def set_limit(self,lis :list):
		self.__new_limits.append(*lis)

	def __call__(self,func :callable):
		pass ##TODO: I have to think about this.
