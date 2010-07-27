from os import getenv
import sys
import atexit
from __future__ import print_function

from .stdio import Errors, Output
from .functions import *
from .conf import Conf
from .stdio import File
from .database import *

conf = Conf("~/maCMS/.miaorc")

sys.stderr = Errors(conf.query("logfile"))

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
				self.GET[deBrand(k)] = deBrand(v)

	def rPOST(self):
		""" This function insert POST values (if any)
		in POST dictionary """

		tmp = int(getenv("CONTENT_LENGTH"))

		if tmp>=1:
			for i in sys.stdin.read()[:tmp].split("&"):
				k,v = i.strip().split("=")
				self.POST[deBrand(k)] = deBrand(v)

	def rCOOKIE(self):
		""" This function insert COOKIEs values (if any)
		in COOKIE dictionary """

		tmp = getenv("HTTP_COOKIE")

		if tmp:
			for i in tmp.split(";"):
				k,v = i.strip().split("=")
				self.COOKIE[deBrand(k)] = deBrand(v)

	def rSERVER(self):
		""" This function insert SERVER vars values (if any)
		in SERVER dictionary """

		for i in self.server_varList:
			k = getenv(i)
			self.SERVER[i] = k

	def __init__(self,conf = "~/.frozenrc"):
		""" conf in your configuration file (if any).
		~ is a special character (accepted on Windows too)
		to indicate your home directory"""

		if "conf" in globals().keys():
			self.conf = globals()['conf']
		else:
			self.conf = Conf(conf)

		if self.conf.query("query_string_enabled"):
			self.rGET()

		if self.conf.query("stdin_support_enabled"):
			self.rPOST()

		if self.conf.query("allow_cookies"):
			self.rCOOKIE()

		if self.conf.query("verbose_server"):
			self.rSERVER()

data = Data()

File.valid_path = conf.query("allowed_dir")
File.whitelist = conf.query("whitelist")
File.blacklist = conf.query("blacklist")

sys.stdout = Output(conf.query("template_file"))

if conf.query("use_db"):
	database = DB(conf.query("db_type"),conf.query("db_file"))

del getenv

def print(*args,**kwargs):
	sys.stdout.write(*args,**kwargs)

@atexit.register
def __do():
	try:
		sys.stdout.exit()
		sys.stderr.exit()
		database.exit()
	except:
		pass
