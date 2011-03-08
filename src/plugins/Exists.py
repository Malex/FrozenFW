import os

def do(file):
	if not os.access(file,os.R_OK):
		return "404 Not Found",Headers("Content-Type: text/html"),"<h1>404 NOT FOUND</h1>"
	else:
		raise Exception

dispatch+=do
