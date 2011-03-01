
class Header():
	name = ""
	value = ""

	def __init__(self, name :str , value :str):
		self.name = name
		self.value = value

	def __str__(self) -> str:
		return "{}: {}\r\n".format(self.name,self.value)

	def __repr__(self) -> str:
		return str(self)

class Headers():

	__headers = []

	@property
	def headers(self) -> str:
		return "\r\n".join(self.__headers)
	@headers.setter
	def setter(self,what):
		self.__headers.append(Header(what))

	def __add__(self,header :str) -> Headers:
		self.headers = header
		return self
	def __sub__(self,header :str) -> Headers:
		self.__headers.remove(Header(header)) #TODO: improve through methods
		return self

