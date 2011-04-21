
def state(stat :str,head ,body :str, filename :str) -> list:
	if stat.startswith("200") or stat=='':
		return Response(stat,head,body,filename)
	else:
		try:
			body = File.get_contents(conf.query("Err_pages")[stat[0:3]])
		except KeyError:
			pass
		return Response(stat,head,body,filename,ready=True)

dispatch += state
