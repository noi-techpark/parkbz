# -*- coding: utf-8 -*-
from xmlrpclib import ServerProxy
server = ServerProxy("http://ipchannels-frontend.integreen-life.bz.it/xmlRpcFrontEnd/xmlrpc")

def user(): return dict(form=auth())

def index():
	parks_id = cache.ram('parkingIds', lambda: server.DataManager.getParkingIds(), time_expire=3600)
	if parks_id == -1:
		return 'errore'
	parks = []
	for park in parks_id:
		data = __get_park_data(park)
		parks.append( data )
	return {'parks': parks}

def freeslots():
	if not(request.ajax): raise HTTP(403)
	park_id = request.args(0) or 'index'
	if not(park_id and park_id.isdigit()): raise HTTP(404)
	data = __get_park_data(int(park_id))	
	json = {'freeslots':data['freeslots']}	

	freeslots = request.args(1) or 'index'
	if data['freeslots'] != -1 and (not(freeslots and freeslots.isdigit()) or int(freeslots) != data['freeslots']):
		json['plain_html'] = response.render('default/park_bar.html', park=data )

	return response.render('generic.json', json)

def __get_park_data(park):
	data = cache.ram('park_%s' % park, lambda: server.DataManager.getParkingStation(park), time_expire=3600)
	data['park_id']	= park
	data['freeslots'] = server.DataManager.getNumberOfFreeSlots(park)
	data['slots_taken'] = data['slots'] - data['freeslots']
	data['slots_taken_rate'] = (data['slots_taken'] * 100) / data['slots']
	data['freeslots_rate'] = 100 - data['slots_taken_rate']
	return data
