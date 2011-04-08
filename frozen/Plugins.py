from .Sandbox import EXEC,IMPORT
from .File import File
import os

class PluginError(Exception):
	pass

class Plugin():

	def __init__(self,filename :str):
		if not os.access(File.parse(filename),os.R_OK):
			raise PluginError("Plugin {} does not exist".format(filename))
		self._file = filename

	def exec(self,sandbox,glob :dict):
		sandbox(self._filename,EXEC,glob)

class Plugins():

	def __init__(self,plugs :list=[]):
		self.__plugins = [Plugin(a) for a in plugs]

	def load_plugin(self,filename :str):
		self.__plugins.append(Plugin(filename))

	@property
	def plugins(self) -> list:
		return self.__plugins

	def exec(self,sandbox,glob :dict):
		for i in self.plugins:
			i.exec(sandbox,glob)
