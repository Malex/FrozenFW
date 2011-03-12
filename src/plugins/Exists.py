import os

def do(stat :str, head :list, body :str, filename :str) -> list:
	if not os.access(filename,os.R_OK):
		return Response("404 Not Found",Headers("Content-Type: text/html"),"<h1>404 NOT FOUND</h1>")

dispatch+=do
