from frozen import *

def app(environ,print_rep):
	data = Data(conf,environ,True)
	output = sys.stdout
	rep_status,headers,body = dispatch((conf.query("base_dir")+data.SERVER['PATH_INFO']).replace("//","/"))
	print_rep(rep_status,headers)
	return [body]


