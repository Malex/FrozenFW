import os

from .Data import Data,DataError
from .Cookie import Cookie,CookieError
from .stdio import Output,print,output
from .functions import unquote,nl2br,htmlspecialchars,htmlentities
from .Conf import Conf,ConfError
from .File import File,open,FileError
from .Dispatcher import Dispatcher,Response
from .Headers import Headers,Header
from .Logger import Logger,NOTICE,WARNING,ERROR,LoggerException
from .Sandbox import Sandbox,EXEC,IMPORT
from .Plugins import Plugins

conf = Conf("/etc/frozenrc")

log = Logger(conf.query("log_file"),eval(conf.query("log_level")))

try:
	File.set_limits(conf.query("allowed_dir"),conf.query("blacklist"),conf.query("whitelist"))

	output.headers = Headers(*tuple(conf.query("headers")))

	dispatch = Dispatcher()

	sandbox = Sandbox(conf.query("sand_vars"),conf.query("sand_limits"),log)

	plugins = Plugins()
	for pwd,cd,touch in os.walk(conf.query("plugin_dir")):
		for i in touch:
			if i.endswith(".py") and i[:-3] in conf.query("load_plugins"):
				plugins.load_plugin(i)
	plugins.exec(sandox,globals())

except BaseException as e:
	log.write(e)

