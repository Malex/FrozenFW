import mimetypes

def getfile(stat,head,body,filename):
	if filename.endswith(".py"):
		return Response(stat,head,body,filename)
	elif stat!='':
		return Response(stat,head,body,filename)
	else:
		with open(File.parse(filename),'rb') as r:
			ctype,cenc = mimetypes.guess_type(File.parse(filename))
			return Response("200 OK",Headers("Content-Type: {}".format(ctype),"Content-Encoding: {}".format(cenc)),r.read(),filename,)

dispatch += getfile
