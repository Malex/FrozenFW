
def include(filename):
	t = Template(filename)
	t.rep = repl
	output.print(t.get_body())

output += include
