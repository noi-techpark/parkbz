# -*- coding: utf-8 -*-
import socket
#@cache.action(time_expire=3600, cache_model=cache.ram)
def index():
    try:
        parks = __get_parks_info()
        return {'parks': parks}
    except socket.timeout:
        return 'Data not available, the frontEnd is currently unreachable'

#def test_1():
#    out = server.DataManager.getNumberOfFreeSlots(104)
#    return response.render('layout_ratchet.html', {})
    
#def test_2():    
#    out = server.DataManager.getParkingStation(104)
#    return out

def map():
    try:
        parks = __get_parks_info()
        #parks = []
        return {'parks': parks}
    except socket.timeout:
        return 'Data not available, the frontEnd is currently unreachable'

def get_geojson():
    try:
        parks = __get_parks_info()
        parking_id = int(request.vars.parking_id) if  request.vars.parking_id and  request.vars.parking_id.isdigit() else None
        features= [{"type": "Feature",
                    "properties": {
                        "popupContent": response.render('default/park_box.html', {'park':p, 'tooltip': True}),
                        "openPopup": True if parking_id == p['park_id'] else False
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [p['longitude'], p['latitude']]
                    },} for p in parks] 

        return response.json({"type": "FeatureCollection", 'features': features}) 
    except socket.timeout:
        return 'Data not available, the frontEnd is currently unreachable'
        
def prediction():
    parking_id = int(request.vars.parking_id) if  request.vars.parking_id and  request.vars.parking_id.isdigit() else None
    return response.json([[1990, 18.9], [1991, 18.7], [1992, 18.4], [1993, 30], [1994, 19.5], [1995, 19.3], [1996, 19.4], [1997, 20.2], [1998, 19.8]])
    
#def trend():
#	park_id = request.args(0) or 'index'
#	if not(park_id and park_id.isdigit()): raise HTTP(404)
#	parks = __get_parks_info()
#	return {'parks': parks, 'park_id':park_id}

#def parking():
#    response.files.append(URL('static','js/OpenLayers.js'))
#    park_id = request.args(0) or 'index'
#    if not(park_id and park_id.isdigit()): raise HTTP(404)
#    try:
#        park = __get_park_data(int(park_id))
#    except:
#        return 'Data not available, the frontEnd is currently unreachable'
#    response.title = "%s %s" %(T('Parking'), park['name'])
#    response.page_title = "%s %s, %s" % (T('Parking'), park['name'], T('Bolzano') )
#    response.subtitle = "%s, 39100 %s" % (park['address'], T('Bolzano'))
#    response.meta.description = "%s %s - 39100 %s" % (T('Map and number of free slots of the parking'), park['name'], T('Bolzano'))
#    return {'park': park, 'park_id':park_id}

def doc():
	methods = server.system.listMethods()
	methods.sort()
	return {'server':server, 'methods':methods}

def widget():
	try:
		parks = __get_parks_info()
		return {'parks': parks}
	except socket.timeout:
		return 'Data not available, the frontEnd is currently unreachable'
	except Exception:
		return 'Internal error'

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
	if data['freeslots'] == -1:
		json['plain_html'] = response.render('default/park_bar_error.html', park=data )
	elif not(freeslots and freeslots.isdigit()) or int(freeslots) != data['freeslots']:
		json['plain_html'] = response.render(render, park=data )

	extension = 'json' if request.extension != 'jsonp' else 'jsonp'
	return response.render('generic.%s' % extension, json)

#def search():
#	import re
#	if not (request.vars.query): return response.json([])
#	query = request.vars.query.lower()
#	parks = __get_parks_info(address_only=True)
#	json_l = []
#	for park in parks:
#		if query in park['name'].lower() or query in park['address'].lower():
#			cur_park = {'value':park['name'], 'name':park['name'], 'address':park['address'], 'tokens':[park['name'],park['address']] } 
#			cur_park['link'] = get_park_link(park)
#			json_l.append(cur_park)
#
#	return response.json(json_l)
