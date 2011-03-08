import re
import sys

from .File import File,open,FileError
from .Headers import Headers

class Output():

	headers = Headers()

	def write(self,*args,**kwargs):
		self.data += " ".join(args)

	def get_body(self):
		return self.data

	def exit(self):
		for i in self.get_headers():
			sys.__stdout__.write(":".join(i)+"\r\n")
		sys.__stdout__.write("\r\n")
		sys.__stdout__.write(self.get_body())

def print(*args,**kwargs):
	sys.stdout.write(*args,**kwargs)
