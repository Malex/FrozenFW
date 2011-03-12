import re

class Template(Output):

	rep = {}
	arg = []

	templ_reg = re.compile(r"@!([\w_]+)\s*#(.+?)#\s*(.+)@!end\s+\1\s*#\2#",re.S)
	f_hash = {}
	sep = '\n'

	def __init__(self,path :str="template.html"):
		try:
			self.set_template(path)
		except FileError as e:
			raise FileError("Not Valid Template {}".format(path)) from e

	def set_template(self,path :str):
		""" Set template file. This file must be in File limits (use whitelist if you need """
		self.data = File.get_contents(path)

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

	def get_body(self) -> str:
		return self.templ_exec(self.data).format(*tuple(self.arg),**self.rep)

	@property
	def stats(self) -> tuple:
		return self.f_hash.keys()
	@stats.setter
	def add_func(self,ref :object):
		self.f_hash[ref.__name__] = ref

	def ret(self,filename :str) -> tuple:
		if not filename.endswith(".py"):
			raise Exception
		exec(File.get_contents(filename))
		return Response("200 OK",self.headers,self.get_body())

sys.stdout = Template(conf.query("template_file"))

dispatch+=sys.stdout.ret
