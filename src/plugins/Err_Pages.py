
def state(stat :str,head :Headers,body :str, filename :str) -> list:
	if stat.startswith("200"):
		return Response(stat,head,body)
	else:
		body = File.get_contents(conf.query("{}-page".formar(stat[0:3])))
		return Response(stat,head,body,ready=True)

dispatch += state
