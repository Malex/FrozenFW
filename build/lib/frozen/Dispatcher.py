from .Headers import Headers

class Response():
	__ready = False

	def __init__(stat :str, head :Headers, body :str, filename :str, ready :bool=False):
		""" Use ready only if you are SURE your data are ready to be sent to client """
		self.stat = stat
		self.head = head
		self.body = body
		self.filename = filename
		self.ready = ready

	@property
	def ready(self) -> bool:
		return self.__ready
	@ready.setter
	def ready(self, value :bool):
		if value!=True and value!=False:
			raise ValueError("Bool value needed")
		else:
			self.__ready = value

	def get(self) -> tuple:
		return self.stat,self.head,self.body,self.filename


class Dispatcher():
	__list = []

	def __init__(self,*args):
		self.rep = Response("",[],"","")
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

	def __add__(self,i):
		self.lis = i

	def __call__(self,filename):
		self.rep = Response("",[],"",filename)

	def check(self):
		for i in self.__list:
			tmp = self.rep.get()
			t2 = i(*tmp)
			if t2.ready:
				self.reset()
				return t2
			else:
				self.rep = Response(*t2.get())
				continue

	def reset(self):
		self.rep = Response("",[],"","")
