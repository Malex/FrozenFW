import random
from string import ascii_letters,digits

avaiable_chars = ascii_letters+digits

class Session(Cookie):

	def __init__(self, expires :int=60):
		self.__id = ""
		i = (random.randint(0,61) for a in range(0,62))
		for j in i:
			self.__id += str(avaiable_chars[j])
		super().__init__("pysessid",self.__id,expires,httpOnly=True)

	@property
	def id(self) -> str:
		return self.__id

	@staticmethod
	def find_session(cookies :dict) -> str:
		if "pysessid" in cookies.keys():
			return cookies['pysessid']
		else:
			return ''

## Line commented since changes in Data.Data
#super(Data,data).__setattr__('SESSION',Session.find_session(data.COOKIE))

old_init = Data.__init__
def new_init(self,*args,**kwargs):
	old_init(self,*args,**kwargs)
	if self.conf.query("allow_session"):
		self.SESSION = Session.find_session(self.COOKIE)
Data.__init__ = new_init

data = Data(data.conf,data.env)

sandbox = Sandbox(sandbox.allowed_vars.append("Session"),sandbox.new_limits,sandbox.log)
