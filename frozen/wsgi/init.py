from .base import *

def app(environ,print_rep):
	try:
		data.update(environ)
		rep_status,headers,body, filename = dispatch(data.SERVER['PATH_INFO'].replace("//","/")[1:])
		print_rep(rep_status,headers)
		return [body]
	except BaseException as e: #TODO: fix here to use other pages too
		log.write(e)
		print_rep("500 Internal Server Error",[("Content-Type", "text/html")])
		return ["<h1>Internal Server Error</h1>"]
