from datetime import datetime
from .functions import quote
from .Headers import Headers

class CookieError(Exception):
	pass

class Cookie:

	out = Headers()

	@classmethod
	def set(cls,name :str,value :str="",expiration :int=0,restriction :str="/",domain :str="",secure :bool=False,httpOnly :bool=False):
		if domain:
			domain = "domain={};".format(domain)
		if expiration:
			try:
				if type(expiration) is int:
					expiration = quote("expires={:%a, %d-%b-%Y %H:%M:%S UTC};".format(datetime.utcfromtimestamp(expiration)))
				elif type(expiration) is str:
					t = datetime.strptime(expiration,"%a, %d-%b-%Y %H:%M:%S UTC")
					expiration = quote("expires={:%a, %d-%b-%Y %H:%M:%S UTC};".format(t))
				else:
					raise CookieError("Not valid type for expiration: {!r}".format(expiration))
			except Exception as e:
				raise CookieError("An error has occured while processing expiration time") from e
		if secure:
			sec_str = "secure ;"
		else:
			sec_str = ""
		if httpOnly:
			hto_str = "HttpOnly ;"
		else:
			hto_str = ""

		cls.out += "Set-Cookie: {}={};{}path={};{}{}{}".format(quote(name),quote(value),expiration,quote(restriction),quote(domain),sec_str,hto_str)

	def __init__(self,name :str, value :str, expiration :int=0, restriction :str="/", domain :str="", secure :bool=False, httpOnly :bool=False):
		self.name = name
		self.value = value
		self.exp = expiration
		self.path = restriction
		self.dom = domain
		self.https = secure
		self.no_client = httpOnly

	def send(self):
		self.set(self.name,self.value,self.exp,self.path,self.dom,self.https,self.no_client)

	def __get__(self) -> str:
		return self.value

	def __getitem__(self,query :str) -> object:
		c_dict = { "restriction" : "path",
				"expiration" : "exp",
				"dom" : "domain",
				"secure" : "https",
				"httpOnly" : "no_client",
				}
		try:
			query = c_dict[query]
		except KeyError:
			pass

		return vars(self)[query]
