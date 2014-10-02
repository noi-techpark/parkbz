# -*- coding: utf-8 -*-
# TODO
# mostrare dati aggiornati solo se clicca
# language
# Add tutti tu the widget
rest_url='http://ipchannels.integreen-life.bz.it/parkingFrontEnd/rest'
import socket
import requests

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
    params={'station':parking_id}
    r = requests.get("%s/%s" %(rest_url, "get-data-types"), params=params)
    if r.status_code != 200: return response.json([])
    forecast_types = filter(lambda e: 'forecast' in e[0].lower() and len(e) > 3, r.json())
    forecast_types = sorted(forecast_types,key=lambda x: int(x[3]))
    output=[]
    for pos, f in enumerate(forecast_types):
        params['type'] = f[0]
        params['period'] = f[3]    
        r = requests.get("%s/%s" %(rest_url, "get-last-record"), params=params)
        data = r.json()
        output.insert(0, [int(data['timestamp']), int(data['value'])])
    return response.json(output)

    
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
    parking_id = _vars('parking_id')
    type_r = _vars('type', is_string=True) or 'free'
    period = _vars('period')
    params={'station':parking_id, 'type':type_r}
    if period:
        params['period'] = period
    r = requests.get("%s/%s" %(rest_url, "get-last-record"), params=params)
    return response.json({'freeslots':r.json()['value']})

def get_times():
    r = requests.get("%s/%s" %(rest_url, "get-data-types"))
    forecast_types = filter(lambda e: 'forecast' in e[0].lower() and len(e) > 3, r.json())
    forecast_types = filter(lambda f: int(f[3]) % 3600 == 0, forecast_types)
    forecast_types = sorted(forecast_types,key=lambda x: int(x[3]))
    forecast_types.insert(0, [None, None, None, None, T('adesso')])
    ul = UL([LI(A(("tra %s" % (("%s ora" % (int(f[3])/3600)) if f[3]=="3600" else ("%s ore" % (int(f[3])/3600)))) if f[3] else f[4] , **{'_data-type':f[0], '_data-period':f[3], '_data-default-msg': f[0]!=None}),  _class='') for f in forecast_types], _class="box round times")
    ul[0]['_class'] += 'current'
    span = SPAN(T('adesso'), _class="box round")
    return CAT(span, ul)
