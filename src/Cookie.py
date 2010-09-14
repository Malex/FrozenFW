from datetime import datetime

class CookieError(Exception):
	pass

class Cookie:
	domain = ""
	expiration = ""

	out_handle = None
	list = []

	@classmethod
	def set(cls,name :str,value :str="",expiration :int=0,restriction :str="/",domain :str="",secure :bool=False,httpOnly :bool=False):
		if not domain:
			domain = cls.domain
		else:
			domain = "domain={};".format(domain)

		if not expiration:
			expiration = cls.expiration
		else:
			try:
				if type(expiration) is int:
					expiration = "expires={:%a, %d-%b-%Y %H:%M:%S UTC};".format(datetime.utcfromtimestamp(expiration))
				elif type(expiration) is str:
					t = datetime.strptime(expiration,"%a, %d-%b-%Y %H:%M:%S UTC")
					expiration = "expires={:%a, %d-%b-%Y %H:%M:%S UTC};".format(t)
				else:
					raise CookieError("Not valid type for expiration: {!r}".format(expiration))
			except Exception as e:
				raise CookieError("An error has occured while processing expiration time") from e
		if secure:
			sec_str = "secure ;"
		else:
			sec_str = ""
		if httponly:
			hto_str = "HttpOnly ;"
		else:
			hto_str = ""

		out_handle.set_headers("Set-Cookie: {}={};{}path={};{}{}{}".format(quote(name),quote(value),expiration,path,domain,sec_str,hto_str))
		ret = Cookie(name,value,expiration,restriction,domain,secure,httpOnly)
		cls.list.append(ret)
		return ret

	def __init__(self,name :str, value :str, expiration :int=0, restriction :str="/", domain :str="", secure :bool=False, httpOnly :bool=False):
		self.name = name
		self.value = value
		self.exp = expiration
		self.path = restriction
		self.dom = domain
		self.https = secure
		self.no_client = httpOnly

	def __get__(self):
		return self.value

	def __getitem__(self,query :str):
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

		acc = ['name','value','https','no_client','exp','dom','path']
		if not query in acc:
			raise CookieError("Not such attribute for Cookies")
		else:
			return vars(self)[query]
