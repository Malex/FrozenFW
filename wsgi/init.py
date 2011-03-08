from frozen import *

def app(environ,print_rep):
	try:
		data = Data(conf,environ,True)
		output = sys.stdout
		rep_status,headers,body = dispatch((conf.query("base_dir")+data.SERVER['PATH_INFO']).replace("//","/"))
		print_rep(rep_status,headers)
		return [body]
	except BaseException as e:
		log.write(e)
		print_rep("500 Internal Server Error",["Content-Type: text/html"])
		return "<h1>Internal Server Error</h1>"
