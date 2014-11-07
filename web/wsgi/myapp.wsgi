import cgi

def application(environ, start_response):
    form = cgi.FieldStorage(fp=environ['wsgi.input'], 
                            environ=environ)	  
    status = '200 OK'
    output = "Hello Cruel World! <br/><br/> %s <br/><br/> %s "%(environ,form)
    #doubtput = ["<br/> %s, %s <br/>"%(x,form.getvalue(x)) for x in environ] 

    output = output + "<h1>yo!</h1>"
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]

    start_response(status, response_headers)

    #return [doubtput]
    return [output]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    #    server = make_server('localhost', 8081, application)
    server = make_server('ark.usc.edu', 8081, application)
    server.serve_forever()
