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

def print(*args,**kwargs):
	sys.stdout.write(*args,**kwargs)
