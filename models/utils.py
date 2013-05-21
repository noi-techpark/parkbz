from xmlrpclib import ServerProxy
from applications.parkbz.modules.utils import TimeoutTransport

server = ServerProxy("http://ipchannels.integreen-life.bz.it/parkingFrontEnd/xmlrpc", transport=TimeoutTransport())

def __get_park_data(park):
	data = cache.ram('park_%s' % park, lambda: server.DataManager.getParkingStation(park), time_expire=3600)
	print data
	if not(isinstance(data, dict)) or ('status' in data and data['status'] != 200): 
		cache.ram('park_%s' % park, lambda: None, time_expire=0)
		raise HTTP(404)	
	data['park_id']	= park
	data['freeslots'] = server.DataManager.getNumberOfFreeSlots(park)
	name = data['name']
	try:
		data['name'] = name[name.index('-') + 1:].strip()
	except:
		data['name'] = name.strip()
	data['slots_taken'] = data['slots'] - data['freeslots']
	data['slots_taken_rate'] = (data['slots_taken'] * 100) / data['slots']
	data['freeslots_rate'] = 100 - data['slots_taken_rate']
	return data

def __get_parks_info():
	parks_id = cache.ram('parkingIds', lambda: server.DataManager.getParkingIds(), time_expire=3600)
	if parks_id == -1:
		return 'errore'
	parks = []
	for park in parks_id:
		data = __get_park_data(park)
		parks.append( data )
	parks_ordered = sorted(parks, key=lambda p: p['name'])
	return parks_ordered
