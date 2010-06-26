from os import getenv
from sys import stdin, stdout, stderr
from stdio import Errors, Output
import atexit

stderr = Errors()

from functions import *
from conf import Conf
from stdio import File

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
				GET[deBrand(k)] = deBrand(v) #//TODO : inserire deBrand in functions

	def rPOST(self):
		""" This function insert POST values (if any)
		in POST dictionary """

		tmp = int(getenv("CONTENT_LENGTH"))

		if tmp>=1:
			for i in stdin.read()[:tmp].split("&"):
				k,v = i.strip().split("=")
				POST[deBrand(k)] = deBrand(v)

	def rCOOKIE(self):
		""" This function insert COOKIEs values (if any)
		in COOKIE dictionary """

		tmp = getenv("HTTP_COOKIE")

		if tmp:
			for i in tmp.split(";"):
				k,v = i.strip().split("=")
				COOKIE[deBrand(k)] = deBrand(v)

	def rSERVER(self):
		""" This function insert SERVER vars values (if any)
		in SERVER dictionary """

		for i in self.server_varList:
			k = getenv(i)
			SERVER[i] = k

	def __init__(self,conf = "~/.frozenrc"):
		""" conf in your configuration file (if any).
		~ is a special character (accepted on Windows too)
		to indicate your home directory"""

		self.conf = Conf(conf)

		if self.conf.query("query_string_enabled"):
			self.rGET()

		if self.conf.query("stdin_support_enabled"):
			self.rPOST()

		if self.conf.query("allow_cookies"):
			self.rCOOKIE()

		if self.conf.query("verbose_server"):
			self.rSERVER()


class Output(Output):

	rep = {}
	_handle = stdout

	def __init__(self,path="template.html"):
		if not os.access(path,os.R_OK):
			raise IOError("Not valid template")
		else:
			self.data = File.get_contents(path)

	def write(self,key,value):
		rep[key] = value

	@atexit.register
	def do(self):
		self._handle.write(self.data.format(**rep)




stdout = Output()

del stdin
del getenv
