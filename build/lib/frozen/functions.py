from urllib.parse import unquote_plus,quote_plus
from cgi import escape

def unquote(s :str) -> str:
	""" Converts string %xx (where xx is the hex value)
	into their respective chars. Besides it converts + into spaces """
	return unquote_plus(s)

def quote(s :str) -> str:
	""" Converts special chars into their respective
	hex values (%xx form). Besides it converts spaces into + """
	return quote_plus(s)

def htmlspecialchars(s :str) -> str:
	""" Replace common special chars with their
	iso-8859-1 equivalent sequences """

	diz = { "\"" : "quot",
            "<" : "lt",
            ">" : "gt",
            "'" : "#039",
            "&" : "amp"
            }

	for i in diz.keys()[::-1]:
		s.replace(i,"&"+diz[i]+";")

	return s

def htmlentities(s :str) -> str:
	""" Replace ALL special chars with their equivalent """
	return escape(s,True)

def nl2br(s :str) -> str:
	""" Replace \n char with <br /> string """
	return s.replace("\n","<br />")
