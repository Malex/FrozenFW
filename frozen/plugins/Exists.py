import os

def do(stat :str, head , body :str, filename :str) -> list:
	if not os.access(File.parse(filename),os.R_OK):
		return Response("404 Not Found",Headers("Content-Type: text/html"),"<h1>404 NOT FOUND</h1>",filename)
	else:
		return Response(stat,head,body,filename)

dispatch += do
