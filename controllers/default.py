# -*- coding: utf-8 -*-
# TODO
# Add tutti tu the widget

import socket
import requests
import datetime

#@cache.action(time_expire=3600, cache_model=cache.ram)
def index():
    try:
        parks = __get_parks_info()
        return {'parks': parks}
    except socket.timeout:
        return 'Data not available, the frontEnd is currently unreachable'

# Return the template of the map, the map is populated by the geojson requested with ajax
def map():
    return {}
#    try:
        #parks = __get_parks_info()
        #return {'parks': parks}
#    except socket.timeout:
#        return 'Data not available, the frontEnd is currently unreachable'

# Return the geojson with the point of each parking area with the html of the specific tooltip
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

# Return the data of the parking freeslots prediction for the given parking area
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

#def widget():
#	try:
#		parks = __get_parks_info()
#		return {'parks': parks}
#	except socket.timeout:
#		return 'Data not available, the frontEnd is currently unreachable'
#	except Exception:
#		return 'Internal error'

# Return the number of freeslots for the given parking area
def freeslots():
    parking_id = _vars('parking_id')
    type_r = _vars('type', is_string=True) or 'free'
    period = _vars('period')
    params={'station':parking_id, 'type':type_r}
    if period:
        params['period'] = period
    r = requests.get("%s/%s" %(rest_url, "get-last-record"), params=params)
    json_response = {'freeslots':r.json()['value']}
    if 'exceptionMessage' in r.json():
        return r.json()
    if type_r != 'free':
        created_on = datetime.datetime.fromtimestamp(r.json()['created_on']/1e3)
        json_response['created_on'] = "%s:%s" %(created_on.hour, created_on.minute)
    return response.json(json_response)

# Return a list of available forecasts
def get_times():
    r = requests.get("%s/%s" %(rest_url, "get-data-types"))
    forecast_types = filter(lambda e: 'forecast' in e[0].lower() and len(e) > 3, r.json())
    forecast_types = filter(lambda f: int(f[3]) % 3600 == 0, forecast_types)
    forecast_types = sorted(forecast_types,key=lambda x: int(x[3]))
    forecast_types.insert(0, [None, None, None, None, T('adesso')])
    ul = UL([LI(A(("tra %s" % (("%s %s" % (int(f[3])/3600, T('hour'))) if f[3]=="3600" else ("%s %s" % (int(f[3])/3600, T('hours'))))) if f[3] else f[4] , **{'_data-type':f[0], '_data-period':f[3], '_data-default-msg': f[0]!=None}),  _class='') for f in forecast_types], _class="box round times")
    ul[0]['_class'] += 'current'
    span = SPAN(T('now'), _class="box round")
    return CAT(span, ul)

