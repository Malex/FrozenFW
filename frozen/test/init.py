from wsgiref.simple_server import make_server
from frozen import *

def app(environ,print_rep):
	data = Data(conf,environ,True)
	output = sys.stdout
	try:
		with open((conf.query("base_dir")+data.SERVER['PATH_INFO']).replace("//","/")) as f:
			rep_status = "200 OK"
			exec(f.read())
			headers = sys.stdout.get_headers()
			body = sys.stdout.get_body()
	except (FileError,IOError) as e:
		__builtins__.print(e)
		rep_status = "404 Not Found"
		headers = [("Content-Type:","text/plain")]
	sys.stdout = sys.__stdout__
	print_rep(rep_status,headers)
	return [body]

h = make_server (
		"localhost",
		80,
		app)
h.handle_request()
