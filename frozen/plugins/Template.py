import html.parser

class _Parser(html.parser.HTMLParser):
	subs = []

	def handle_pi(self,data):
		data = data.strip()
		if data.startswith('?'):
			data = data[1:]
		if data.startswith("python "):
			self.subs.append(data[7:])

class Template(Output):

	rep = {}
	arg = []

	__s = ''

	def __init__(self,path :str="template.html"):
		try:
			self.set_template(path)
			self.parser = _Parser()
		except FileError as e:
			raise FileError("Not Valid Template {}".format(path)) from e

	def set_template(self,path :str):
		""" Set template file. This file must be in File limits (use whitelist if you need) """
		self.data = File.get_contents(path)

	def templ_exec(self,s :str) -> str:
		self.parser.feed(s)
		to_exec = self.parser.subs
		self.parser.subs = []
		for i in to_exec:
			t = self.exec(i)
			s = s.replace("<?python {}".format(i),s)
		return s

	def exec(self,s :str) -> str:
		exec(s,self.func_dict.update(**{'print' : self.print,'repl' : self.rep,"Template" : Template,}))
		t = self.__s
		self.__s = ''
		return t

	def print(self,*args,**kwargs):
		sep = kwargs['sep'] if 'sep' in kwargs.keys() else ''
		self.__s = sep.join(args)

	def write(self,*args,**kwargs):
		log.notice("I was called")
		self.arg.extend(list(args))
		self.rep.update(kwargs)

	def __add__(self,f):
		self.func_dict[f.__name__] = f
		return self

	def get_body(self) -> str:
		return self.templ_exec(self.data).format(*tuple(self.arg),**self.rep)

def ret(stat :str, head , body :str, filename :str):
	if not filename.endswith(".py") or (stat and stat[:3]!="200"):
		return Response(stat,head,body,filename)
	exec(File.get_contents(filename).replace("__builtins__",'') if conf.query("secure_lock") else File.get_contents(filename))
	log.notice(output.rep)
	return Response("200 OK",head,output.get_body(),filename,ready=True)

output = Template(conf.query("template_file"))

sandbox = Sandbox(sandbox.allowed_vars.append("Template"),sandbox.new_limits,log)

dispatch += ret

def print(*args,**kwargs):
	output.write(*args,**kwargs)
