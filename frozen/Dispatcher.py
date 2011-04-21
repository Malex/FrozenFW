from .Headers import Headers

class Response():

	def __init__(self, stat :str, head :Headers, body :str, filename :str, ready :bool=False):
		""" Use ready only if you are SURE your data are ready to be sent to client """
		self.__ready = False
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
		if type(value) is not bool:
			raise ValueError("Bool value needed")
		else:
			self.__ready = value

	def get(self) -> tuple:
		return (self.stat,self.head,self.body,self.filename)

	def __iter__(self):
		for i in self.get():
			yield i


class DispatcherError(Exception):
	def __init__(self,s,name,e):
		super().__init__(self,s.format(name,repr(e)))

class Dispatcher():

	def __init__(self,*args):
		self.__list = []
		self.reset()
		for i in args:
			setattr(self,self.lis,i)

	@property
	def lis(self):
		return self.__list
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
		return self

	def __call__(self,filename):
		self.reset()
		self.rep.filename = filename
		return self.check()

	def check(self):
		for i in self.__list:
			tmp = self.rep.get()
			try:
				t2 = i(*tmp)
			except BaseException as e:
				raise DispatcherError("In function {}: {}",i.__name__,e).with_traceback(None) from e.with_traceback(None)
			if t2.ready:
				return t2
			else:
				self.rep = Response(*t2.get())
				continue
		return self.rep

	def reset(self):
		self.rep = Response("",Headers(),"","")
