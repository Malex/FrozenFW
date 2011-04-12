def loop(varname,string):
	if not varname in repl.keys():
		print("")
		return
	for i in repl[varname]:
		print(string.format(**{varname : i}))

output += loop
