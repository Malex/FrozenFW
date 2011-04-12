
class Header():

	def __init__(self, name :str , value :str = False):
		if not value:
			self.name,self.value = [a.strip() for a in name.split(":")]
		else:
			self.name = name
			self.value = value

	def __str__(self) -> str:
		return "{}: {}\r\n".format(self.name,self.value)

	def __repr__(self) -> str:
		return str(self)

class Headers():

	@property
	def headers(self) -> list:
		return self.__headers
	@headers.setter
	def headers(self,what):
		self.__headers.append(Header(what))

	def __add__(self,header :str) -> object:
		self.headers = header
		return self
	def __sub__(self,header :str) -> object:
		self.__headers.remove(Header(header)) #TODO: improve through methods
		return self

	def __iter__(self):
		for i in self.headers:
			yield (i.name,i.value)

	def __init__(self,*args):
		self.__headers = []
		for i in args:
			self += i

	def get(self):
		return self.headers
