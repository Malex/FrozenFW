from os import getenv
import sys
import urllib
from cgi import escape

def unquote(s):
	""" Converts string %xx (where xx is the hex value)
	into their respective chars. Besides it converts + with spaces """
	return urllib.unquote_plus(s)

def htmlspecialchars(s):
	""" Replace common special chars with their
	iso-8859-1 equivalent sequences """

	diz = { "\"" : "quot",
            "<" : "lt",
            ">" : "gt",
            "'" : "#039",
            "&" : "amp"
            }

	for i in diz.keys()[::-1]:
		s.replace(i,"&"+diz[i]+";")

	return s

def htmlentities(s):
	""" Replace ALL special chars with their equivalent """
	return escape(s,True)

def nl2br(s):
	""" Replace \n char with <br /> string """
	return s.replace("\n","<br />")


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
'HTTP_CONNECTION','HTTP_HOST','HTTP_REFERER']

	def rGET(self):
		""" This function insert GET values (if any)
		in GET dictionary """

		tmp = getenv("QUERY_STRING")

		if tmp:
			for i in tmp.split("&"):
				k,v = i.strip().split("=")
				self.GET[unquote(k)] = unquote(v)

	def rPOST(self):
		""" This function insert POST values (if any)
		in POST dictionary """

		tmp = int(getenv("CONTENT_LENGTH"))

		if tmp>=1:
			for i in sys.stdin.read()[:tmp].split("&"):
				k,v = i.strip().split("=")
				self.POST[unquote(k)] = unquote(v)

	def rCOOKIE(self):
		""" This function insert COOKIEs values (if any)
		in COOKIE dictionary """

		tmp = getenv("HTTP_COOKIE")

		if tmp:
			for i in tmp.split(";"):
				k,v = i.strip().split("=")
				self.COOKIE[unquote(k)] = unquote(v)

	def rSERVER(self):
		""" This function insert SERVER vars values (if any)
		in SERVER dictionary """

		for i in self.server_varList:
			k = getenv(i)
			self.SERVER[i] = k

	def __init__(self,conf=None):
		""" conf in your configuration file (if any).
		~ is a special character (accepted on Windows too)
		to indicate your home directory"""

		if self.conf:
			self.conf = conf

			if self.conf.query("query_string_enabled"):
				self.rGET()

			if self.conf.query("stdin_support_enabled"):
				self.rPOST()

			if self.conf.query("allow_cookies"):
				self.rCOOKIE()

			if self.conf.query("verbose_server"):
				self.rSERVER()
		else:
			self.rGET()
			self.rPOST()
			self.rCOOKIE()
			self.rSERVER()

del getenv
