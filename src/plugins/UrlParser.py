import re

class RegDict(dict):
	regs = {}

	def __init__(self,regs :dict):
		self.regs = regs

	def parse(self,url :str) -> str:
		for i in self.regs.keys():
			if re.match(i,url):
				return re.sub(i,regs[i],url)

	def __add__(self,what :dict) -> RegDict:
		return self.regs.update(**what)
	def __sub__(self,reg :str) -> RegDict:
		return RegDict(self.regs.pop(reg))

class UrlParse():
	__re = None

	def __init__(self,replace :RegDict):
		self.re = replace

	@property
	def re(self) -> RegDict:
		return self.__re
	@re.setter
	def set_re(self,reg :str,rep :str):
		self.__re += {reg : rep}
	@re.deleter
	def del_re(self,reg):
		self.__re -= reg

	def get(self,url :str):
		return self.__re.parse(url)

url_dispatch = UrlParse(RegDict(conf.query("url_dispatch")))

dispatch += lambda s,h,b,f : Response(s,h,b,url_dispatch.get(f))
