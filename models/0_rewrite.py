function_routes = { 
	"parcheggio": "parking" 
}
request.function = function_routes.get(request.function, request.function)
response.view = "%(controller)s/%(function)s.%(extension)s" % request
