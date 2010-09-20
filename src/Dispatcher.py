class Dispatcher():
	__list = []

	def __init__(self,*args):
		for i in args:
			setattr(self,self.lis,i)
	
	@property
	def lis(self):
		raise AttributeError("Write-only attribute")
	@lis.setter
	def lis(self,i):
		try:
			i.__call__
		except AttributeError as e:
			raise ValueError("Not function/method interface found") from e
		self.__list.append(i)

#HOW TODO IT? (it should be runned by wsgi system to make a regular output
#	def check(self,filename):
#		for i in self.__list:
#			i(filename)
