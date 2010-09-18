import re
import sys

from .File import File,open,FileError


class Output():

	__headers = [("Content-Type","text/html")]

	def write(self,*args,**kwargs):
		self.data += " ".join(args)

	@property
	def headers(self): ##TODO: improve by creating and headers class
		return self.__headers

	@headers.setter
	def headers(self, args :tuple):
		""" Appends headers in args to the default headers list. """
		for k,v in (a.split(":") for a in args):
			self.__headers.append((k.strip(),v.strip()))

	def get_body(self):
		return self.data

	def exit(self):
		for i in self.get_headers():
			sys.__stdout__.write(":".join(i)+"\r\n")
		sys.__stdout__.write("\r\n")
		sys.__stdout__.write(self.get_body())

def print(*args,**kwargs):
	sys.stdout.write(*args,**kwargs)

