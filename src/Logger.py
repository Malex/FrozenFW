import datetime

NOTICE=0
WARNING=1
ERROR=2

class LoggerException(ValueError):
	pass

class Logger():
	__handle = ""

	def __init__(self,filename :str="",lv=WARNING):
		if filename:
			self.handle = filename
		self.level=lv

	@property
	def handle(self) -> str:
		return __handle
	@handle.setter
	def set_log(self,filename :str):
		with open(filename,'a'):
			pass
		self.__handle = filename

	@property
	def level(self) -> int:
		return self.__lv
	@level.setter
	def set_level(self,value :int):
		if NOTICE <= value <= ERROR:
			self.__lv = value
		else:
			raise LoggerException("Value must be NOTICE or WARNING or ERROR")

	@staticmethod
	def write_time(handle):
		handle.write(datetime.today().isoformat(' '))

	def write(exc :BaseException):
		warn = True if str(exc.__class__).find("Warning")!=-1 else False
		if self.level > WARNING and warn:
			return
		else:
			with open(self.handle,'a') as w:
				Logger.write_time(w)
				w.write(" File {module} Line {line} => {excp}: {mex}\n".format(**{
																					"line" : exc.__traceback__.tb_lineno,
																					"module" : exc.__traceback__.tb_frame.f_code.co_filename,
																					"mex" : str(exc),
																					"excp" : repr(exc).replace("(\"{}\",)".format(str(exc)),''),
																					}
																				))

	def notice(message :str):
		with open(self.handle,'a') as w:
			Logger.write_time(w)
			w.write(" {}\n".format(message))
