#!/usr/bin/python3

from wsgiref.simple_server import make_server

def app(env,resp):
	response_body = ["{} => {}".format(k,v) for k,v in sorted(env.items())]
	response_body = "\n".join(response_body)
	resp("200 OK",[("Content-Type:"," text/plain")])
	return [response_body]

httpd = make_server(
		"localhost",
		80,
		app
		)

httpd.handle_request()
