import os
import sys
from .functions import unquote,quote
from datetime import datetime

class CookieError(Exception):
	pass

class COOKIE:
	domain = ""
	expiration = ""

	out_handle = None

	@classmethod
	def set(cls,name :str,value :str="",expiration :int=0,restriction :str="/",domain :str="",secure :bool=False,httponly :bool=False):
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


class Data:

	GET = {}
	POST = {}
	COOKIE = {}
	SERVER = {}

	server_varList = ['SERVER_NAME','GATEWAY_INTERFACE','SERVER_SOFTWARE',
'SERVER_PROTOCOL','SERVER_ADDR','REQUEST_METHOD', 'PATH_INFO',
'PATH_TRANSLATED','SCRIPT_NAME','REMOTE_HOST','REMOTE_ADDR',
'AUTH_TYPE','REMOTE_USER','REMOTE_IDENT','CONTENT_TYPE',
'HTTP_USER_AGENT','HTTP_ACCEPT','HTTP_ACCEPT_ENCODING',
'HTTP_ACCEPT_LANGUAGE','HTTP_USER_AGENT','HTTP_ACCEPT_CHARSET',
'HTTP_CONNECTION','HTTP_HOST','HTTP_REFERER', ]

	def rGET(self):
		""" This function insert GET values (if any)
		in GET dictionary """

		tmp = os.getenv("QUERY_STRING")

		if tmp:
			for i in tmp.split("&"):
				k,v = i.strip().split("=")
				self.GET[unquote(k)] = unquote(v)

	def rPOST(self):
		""" This function insert POST values (if any)
		in POST dictionary """

		try:
			tmp = int(os.getenv("CONTENT_LENGTH",0))
		except ValueError: #to prevent bad headers
			tmp = 0

		if tmp>=1:
			if self.wsgi:
				buf = os.getenv("wsgi.input")
			else:
				buf = sys.stdin

			for i in sys.stdin.read(tmp).split("&"):
				k,v = i.strip().split("=")
				self.POST[unquote(k)] = unquote(v)

	def rCOOKIE(self):
		""" This function insert COOKIEs values (if any)
		in COOKIE dictionary """

		tmp = os.getenv("HTTP_COOKIE")

		if tmp:
			for i in tmp.split(";"):
				k,v = i.strip().split("=")
				self.COOKIE[unquote(k)] = unquote(v)

	def rSERVER(self):
		""" This function insert SERVER vars values (if any)
		in SERVER dictionary """

		for i in self.server_varList:
			k = os.getenv(i)
			self.SERVER[i] = k

	def __init__(self,conf,env :dict={}, wsgi :bool=False):
		""" conf in your configuration file (if any).
		~ is a special character (accepted on Windows too)
		to indicate your home directory  """
		
		self.wsgi = wsgi
		if env:
			os.environ = env

		self.conf = conf

		if self.conf.query("query_string_enabled"):
			self.rGET()

		if self.conf.query("stdin_support_enabled"):
			self.rPOST()

		if self.conf.query("allow_cookies"):
			self.rCOOKIE()

		if self.conf.query("verbose_server"):
			self.rSERVER()
