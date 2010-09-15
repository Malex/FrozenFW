import re
import sys

from .File import File,open,FileError


class Output():

	rep = {}
	arg = []
	headers = [("Content-Type","text/html")] ##TODO: use property .

	templ_reg = re.compile(r"@!([\w_]+)\s*#(.+?)#\s*(.+)@!end\s+\1\s*#\2#",re.S)
	f_hash = {}
	sep = '\n'

	def __init__(self,path :str="template.html"):
		try:
			self.set_template(path)
		except FileError as e:
			raise FileError("Not Valid Template {}".format(path)) from e
		self.f_hash['loop'] = self.loop_exec

	def set_headers(self, *args):
		""" Appends headers in args to the default headers list. """
		for k,v in (a.split(":") for a in args):
			self.headers.append(tuple(k.strip(),v.strip()))

	def set_template(self,path :str):
		""" Set template file. This file must be in File limits (use whitelist if you need """
		self.data = File.get_contents(path)

	def loop_exec(self,s :str,t) -> str:
		assert t, "loop_exec should not be called if match fails. Are you calling it directly? Tell me why..."

		try:
			it = self.rep[t.group(2)]
		except KeyError as e:
			raise FileError("Template Var not found {}".format(t.group(2))) from e
		else:
			ret = [t.group(3)] * len(it)
			ret = (x.format(**{t.group(2) : y}) for x,y in zip(ret,it)) #tnx chuzz 
			s = s.replace(t.group(0),self.sep.join(ret))
			return s

	def templ_exec(self,s :str) -> str:
		t = self.templ_reg.search(s)
		while t:
			try:
				s = self.f_hash[t.group(1)](s,t)
			except KeyError:
				s = s.replace(t.group(0),t.group(0).replace('@','&at;'))
			t = self.templ_reg.search(s)
		return s

	def write(self,*args,**kwargs):
		self.arg.extend(list(args))
		self.rep.update(kwargs)

	def get_headers(self):
		return self.headers

	def get_body(self):
		return self.templ_exec(self.data).format(*tuple(self.arg),**self.rep)

	def exit(self):
		for i in self.get_headers():
			sys.__stdout__.write(":".join(i)+"\r\n")
		sys.__stdout__.write("\r\n")
		sys.__stdout__.write(self.get_body())

def print(*args,**kwargs):
	sys.stdout.write(*args,**kwargs)

