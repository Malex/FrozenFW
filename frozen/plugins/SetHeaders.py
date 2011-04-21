
def set_headers(stat,head,body,filename):
	for i,j in Headers(*conf.query("headers")):
		if i not in head:
			head += str(Header(i,j))
	for k,v in Cookie.out:
		head += str(Header(k,v))
	return Response(stat,head,body,filename)

dispatch += set_headers
