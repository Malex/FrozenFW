from frozen import *

def app(environ,print_rep):
	data = Data(conf,environ,True)
	try:
		with open((conf.query("base_dir")+data.SERVER['PATH_INFO']).replace("//","/")) as f:
			rep_status = "200 OK"
			exec(f.read())
			headers = output.get_headers()
			body = output.get_body()
	except (FileError,IOError):
		rep_status = "404 Not Found"
		headers = [("Content-Type: text/plain")]
	print_rep(rep_status,headers)
	return [body]


