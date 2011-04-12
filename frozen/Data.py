import sys
from .functions import unquote,quote

class DataError(Exception):
	pass

class Data:

	server_varList = ['SERVER_NAME','GATEWAY_INTERFACE','SERVER_SOFTWARE',
'SERVER_PROTOCOL','SERVER_ADDR','REQUEST_METHOD', 'PATH_INFO',
'PATH_TRANSLATED','SCRIPT_NAME','REMOTE_HOST','REMOTE_ADDR',
'AUTH_TYPE','REMOTE_USER','REMOTE_IDENT','CONTENT_TYPE',
'HTTP_USER_AGENT','HTTP_ACCEPT','HTTP_ACCEPT_ENCODING',
'HTTP_ACCEPT_LANGUAGE','HTTP_USER_AGENT','HTTP_ACCEPT_CHARSET',
'HTTP_CONNECTION','HTTP_HOST','HTTP_REFERER', ]

	@property
	def GET(self) -> dict:
		return self.__get

	@property
	def POST(self) -> dict:
		return self.__post

	@property
	def SERVER(self) -> dict:
		return self.__server

	@property
	def COOKIE(self) -> dict:
		return self.__cookie

	def rGET(self):
		""" This function insert GET values (if any)
		in GET dictionary """

		tmp = self.env.get("QUERY_STRING",False)

		if tmp:
			for i in tmp.split("&"):
				k,v = i.strip().split("=")
				self.__get[unquote(k)] = unquote(v)

	def rPOST(self):
		""" This function insert POST values (if any)
		in POST dictionary """

		try:
			tmp = int(self.env.get("CONTENT_LENGTH",0))
		except ValueError as e: ##skip POST if there are no POST var
			return

		if tmp>=1:
			for i in self.env.get("wsgi.input").read(tmp).split("&"):
				k,v = i.strip().split("=")
				self.__post[unquote(k)] = unquote(v)

	def rCOOKIE(self):
		""" This function insert COOKIEs values (if any)
		in COOKIE dictionary """

		tmp = self.env.get("HTTP_COOKIE",False)

		if tmp:
			for i in tmp.split(";"):
				k,v = i.strip().split("=")
				self.__cookie[unquote(k)] = unquote(v)

	def rSERVER(self):
		""" This function insert SERVER vars values (if any)
		in SERVER dictionary """

		for i in self.server_varList:
			k = self.env.get(i,"Unknown")
			self.__server[i] = k

	def __init__(self,conf,env :dict={}):
		""" conf in your configuration file (if any).
		~ is a special character (accepted on Windows too)
		to indicate your home directory  """

		self.env = env
		self.conf = conf


		self.__get = {}
		self.__post = {}
		self.__cookie = {}
		self.__server = {}

		if self.conf.query("query_string_enabled"):
			self.rGET()

		if self.conf.query("stdin_support_enabled"):
			self.rPOST()

		if self.conf.query("allow_cookies"):
			self.rCOOKIE()

		if self.conf.query("verbose_server"):
			self.rSERVER()

	def update(self,env :dict):
		t = Data(self.conf,env)
		self.__get = t.GET
		self.__post = t.POST
		self.__cookie = t.COOKIE
		self.__server = t.SERVER

## I use property instead. But I leave it here since I'm not sure what to do.
#	def __setattr__(self,name,value):
#		if name in ("GET","POST","SERVER","COOKIE","SESSION"):
#			raise AttributeError("Assignement not allowed on read-only attributes")
#		else:
#			super().__setattr__(name,value)
