function_routes = { 
	"parcheggio": "parking",
	"Parcheggio": "parking",
	"parkplatz": "parking", 
	"Parkplatz": "parking", 
}
request.function = function_routes.get(request.function, request.function)
response.view = "%(controller)s/%(function)s.%(extension)s" % request

rest_url='http://ipchannels.integreen-life.bz.it/parkingFrontEnd/rest'
