import os.path

def do(stat :str, head , body :str, filename :str) -> list:
	if not os.path.exists(File.parse(filename)):
		return Response("404 Not Found",Headers("Content-Type: text/html"),"<h1>404 NOT FOUND</h1>",filename)
	else:
		try:
			File.get_contents(filename)
		except FileError as e:
			log.notice(e)
			return Response("403 Forbidden",Headers("Content-Type: text/hmtl"),"<h1>403 Forbiddden</h1>",filename)
		else:
			return Response(stat,head,body,filename)

dispatch += do
