import sys
import os

from .Data import Data
from .Cookie import Cookie
from .stdio import Output,print
from .functions import unquote,nl2br,htmlspecialchars,htmlentities
from .Conf import Conf,ConfError
from .File import File,open,FileError
from .Dispatcher import Dispatcher
from .Headers import Headers,Header

conf = Conf("/etc/frozenrc")

File.set_limits(conf.query("allowed_dir"),conf.query("blacklist"),conf.query("whitelist"))

sys.stdout = Output()
sys.stdout.headers = Headers(*tuple(conf.query("headers")))

dispatch = Dispatcher()

if conf.query("use_db"):
	from .database import *
	database = DB(conf.query("db_type"),conf.query("db_file"))

for pwd,cd,touch in os.walk(conf.query("plugin_dir")):
	for i in touch:
		if i.endswith(".py"):
			with open("/".join((pwd,i))) as plug:
				exec(plug.read())

