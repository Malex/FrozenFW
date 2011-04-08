from .base import *

def app(environ,print_rep):
	try:
		data = Data(conf,environ)
		log.notice("here")
		rep_status,headers,body, filename = dispatch((conf.query("base_dir")+data.SERVER['PATH_INFO']).replace("//","/"))
		log.notice("here2")
		print_rep(rep_status,headers.get())
		log.notice("what the hell")
		return [body.encode("Latin-1")]
	except BaseException as e: #TODO: fix here to use other pages too
		log.write(e)
		print_rep("500 Internal Server Error",["Content-Type: text/html"])
		return ["<h1>Internal Server Error</h1>"]
