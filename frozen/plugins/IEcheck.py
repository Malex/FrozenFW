
def check(stat,head,body,filename):
	if "MSIE" in data.SERVER['HTTP_USER_AGENT'] or 'application/xhtml+xml' not in data.SERVER['HTTP_ACCEPT']: ##FIXME: check wildcards too
		for k,v in head:
			if k=='Content-Type':
				if v=='application/xhtml+xml':
					head -= 'Content-Type'
					head += 'Content-Type: text/html'
	return Response(stat,head,body,filename)

dispatch += check
