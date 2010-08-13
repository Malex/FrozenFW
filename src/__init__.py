import sys
import atexit

from .std import Data
from .stdio import Output
from .std import unquote,nl2br,htmlspecialchars,htmlentities
from .conf import Conf,ConfError
from .stdio import File,open,print,FileError
from .database import *

conf = Conf("~/.frozenrc")

data = Data(conf)

File.set_limits(conf.query("allowed_dir"),conf.query("blacklist"),conf.query("whitelist"))

Output.set_headers(*tuple(conf.query("headers")))
sys.stdout = Output(conf.query("template_file"))

if conf.query("use_db"):
	database = DB(conf.query("db_type"),conf.query("db_file"))

@atexit.register
def __do():
	try:
		sys.stdout.exit()
		database.exit()
	except:
		pass
