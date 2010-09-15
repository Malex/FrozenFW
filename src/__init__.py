import sys

from .Data import Data
from .Cookie import Cookie
from .stdio import Output,print
from .functions import unquote,nl2br,htmlspecialchars,htmlentities
from .conf import Conf,ConfError
from .File import File,open,FileError

conf = Conf("/etc/frozenrc")

File.set_limits(conf.query("allowed_dir"),conf.query("blacklist"),conf.query("whitelist"))

sys.stdout = Output(conf.query("template_file"))
sys.stdout.set_headers(*tuple(conf.query("headers")))

Cookie.out_handle = sys.stdout

if conf.query("use_db"):
	from .database import *
	database = DB(conf.query("db_type"),conf.query("db_file"))
