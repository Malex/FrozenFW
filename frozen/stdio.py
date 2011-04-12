import re

from .Headers import Headers

class Output():

	def __init__(self):
		self.data = ""

	def write(self,*args,**kwargs):
		self.data += " ".join(args)

	def get_body(self):
		return self.data

output = Output()

def print(*args,**kwargs):
	output.write(*args,**kwargs)
