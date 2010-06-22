import re

def deBrand(s):
	""" Converts string %xx (where xx is the hex value)
	into their respective chars """
	return re.sub(r"%([0-9A-F]{2})",lambda mat : chr(int(mat.groups()[0],16)),s.strip())


def htmlspecialchars(s):
	""" Replace common special chars with their
	iso-8859-1 equivalent sequences """

	diz = { "\"" : "quot",
            "<" : "lt",
            ">" : "gt",
            "'" : "#039"
            "&" : "amp",
            }

	for i in diz.keys()[::-1]:
		s.replace(i,"&"+diz[i]+";")

	return s

def htmlentities(s):
	""" Replace ALL special chars with their equivalent """

	tmp = __import__("string")
	tmp2 = s[:]

	for i in tmp2:
		if i not in tmp.letters+tmp.digits:
			s.replace(i,"&#"+ord(i)+";")
	del tmp
	return s

def nl2br(s):
	return s.replace("\n","<br />")

