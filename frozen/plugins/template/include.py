
def include(filename):
	t = Template(filename)
	t.rep = repl
	for i in output.func_dict.keys():
		if not i == 'include':
			t.func_dict[i] = output.func_dict[i]
	output.print(t.get_body())

output += include
