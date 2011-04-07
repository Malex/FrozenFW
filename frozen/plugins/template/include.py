
def include(filename):
	t = Template(filename)
	t.rep = repl
	print(t.get_body())

output += include
