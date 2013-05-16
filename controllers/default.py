# -*- coding: utf-8 -*-
import socket
@cache.action(time_expire=3600, cache_model=cache.ram)
def index():
	try:
		parks = __get_parks_info()
		parks_ordered = sorted(parks, key=lambda p: p['name'])
		return {'parks': parks_ordered}
	except socket.timeout:
		return 'Data not available, the frontEnd is currently unreachable'
	except Exception:
		return 'Internal error'

def trend():
	park_id = request.args(0) or 'index'
	if not(park_id and park_id.isdigit()): raise HTTP(404)
	parks = __get_parks_info()
	return {'parks': parks, 'park_id':park_id}

def parking():
	response.files.append(URL('static','js/OpenLayers.js'))
	park_id = request.args(0) or 'index'
	if not(park_id and park_id.isdigit()): raise HTTP(404)
	park = __get_park_data(int(park_id))
	response.title = "%s %s" %(T('Parking'), park['name'])
	response.page_title = "%s %s, %s" % (T('Parking'), park['name'], T('Bolzano') )
	response.subtitle = "%s, 39100 %s" % (park['address'], T('Bolzano'))
	response.meta.description = "%s %s - 39100 %s" % (T('Map and number of free slots of the parking'), park['name'], T('Bolzano'))
	response.menu.append( (T('Trend'), False, URL('default', 'trend', args=[park['park_id'], park['name']])))
	return {'park': park, 'park_id':park_id}

def doc():
	methods = server.system.listMethods()
	methods.sort()
	return {'server':server, 'methods':methods}

def widget():
	return {}

def get_history():
	from datetime import datetime
	if not(request.ajax): raise HTTP(403)
	park_id = request.args(0) or 'index'
	n_days = int(request.vars.interval) if request.vars.interval and request.vars.interval.isdigit() else 7
	if not(park_id and park_id.isdigit()): raise HTTP(404)
	data = server.DataManager.getFreeSlotsByTimeAndParkingArea(int(park_id), 24*60*n_days)
	output = []
	for element in data:
		epoch = (datetime.strptime(str(element[1]), "%Y%m%dT%H:%M:%S") - datetime(1970,1,1)).total_seconds() 
		milli_epoch = epoch * 1000
		output.append([milli_epoch,element[0]])
	return response.render('generic.json', {'park_%s' % park_id:{'data':output, 'park_id':park_id}})	
	
def freeslots():
	#if not(request.ajax): raise HTTP(403) #jsonp is not considered as ajax request
	park_id = request.args(0) or 'index'
	if not(park_id and park_id.isdigit()): raise HTTP(404)
	data = __get_park_data(int(park_id))	
	if request.extension == 'jsonp':
		json = {'data':data}
		render = 'default/single_view.html'		
	else:
		json = {'freeslots':data['freeslots']}	
		render = 'default/park_bar.html'
	freeslots = request.args(1) or 'index'
	if data['freeslots'] != -1 and (not(freeslots and freeslots.isdigit()) or int(freeslots) != data['freeslots']):
		json['plain_html'] = response.render(render, park=data )

	extension = 'json' if request.extension != 'jsonp' else 'jsonp'
	return response.render('generic.%s' % extension, json)
