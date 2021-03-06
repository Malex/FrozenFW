
class Header():

	def __init__(self, name :str , value :str = False):
		if not value:
			self.name,self.value = tuple(a.strip() for a in name.split(":"))
		else:
			self.name = name
			self.value = value

	def __str__(self) -> str:
		return "{}: {}\r\n".format(self.name,self.value)

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
		self.remove(header)
		return self

	def __iter__(self):
		for i in self.headers:
			yield i.name,i.value

	def __contains__(self,w :str) -> bool:
		for k,v in self.__iter__():
			if k==w:
				return True
		return False

	def __init__(self,*args):
		self.__headers = []
		for i in args:
			self += i

	def get(self):
		return self.headers

	def remove(self,name):
		for i in self.__headers:
			if i.name == name:
				self.__headers.remove(i)
