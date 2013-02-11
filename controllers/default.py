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
		data = cache.ram('park_%s' % park, lambda: server.DataManager.getParkingStation(park), time_expire=3600)
		data['park_id']	= park
		data['freeslots']= server.DataManager.getNumberOfFreeSlots(park)
		data['slots_taken'] = data['slots'] - data['freeslots']
		data['slots_taken_rate'] = (data['slots_taken'] * 100) / data['slots']
		data['freeslots_rate'] = 100 - data['slots_taken_rate']
		parks.append( data )
	return {'parks': parks}
