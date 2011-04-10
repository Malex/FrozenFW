import datetime
import traceback

NOTICE=0
WARNING=1
ERROR=2

class LoggerException(ValueError):
	pass

class Logger():
	__dir = ""
	verbose_f = ""

	@property
	def dir(self) -> str:
		return self.__dir
	@dir.setter
	def dir(self,dirname :str):
		with open("{}/{}".format(dirname,self.error_name),'a'):
			pass
		self.__dir = dirname

	def __init__(self, dirname :str="", lv=WARNING, verbose :bool=False, errorfile :str="errors", verbose_file :str="verbose"):
		self.error_name = errorfile
		if dirname:
			self.dir = dirname
		self.level = lv
		self.verbose = verbose
		if verbose:
			self.verbose_f = verbose_file


	@property
	def level(self) -> int:
		return self.__lv
	@level.setter
	def level(self, value :int):
		if NOTICE <= value <= ERROR:
			self.__lv = value
		else:
			raise LoggerException("Value must be NOTICE or WARNING or ERROR")

	@staticmethod
	def write_time(handle):
		handle.write(datetime.datetime.today().isoformat(' '))

	def write(self,exc :BaseException):
		warn = True if "Warning" in str(exc.__class__) else False
		if self.level > WARNING and warn:
			return
		else:
			with open("{}/{}".format(self.dir,self.error_name),'a') as w:
				Logger.write_time(w)
				w.write(" File {module} Line {line} => {excp}: {mex}\n".format(**{
																					"line" : exc.__traceback__.tb_lineno,
																					"module" : exc.__traceback__.tb_frame.f_code.co_filename,
																					"mex" : str(exc),
																					"excp" : repr(exc).replace("(\"{}\",)".format(str(exc)),''),
																					}
																				))
				if self.verbose and self.verbose_f:
					with open("{}/{}".format(self.dir,self.verbose_f),'a') as w:
						Logger.write_time(w)
						w.write('\n')
						traceback.print_tb(exc.__traceback__,file=w)

	def notice(self,message :str):
		with open(self.handle,'a') as w:
			Logger.write_time(w)
			w.write(" {}\n".format(message))
