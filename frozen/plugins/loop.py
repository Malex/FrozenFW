def loop(varname,string):
	if not varname in output.rep.keys():
		output.print("")
		return
	for i in output.rep[varname]:
		output.print(string.format(**{varname : i}))

output += loop
