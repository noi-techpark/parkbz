from xmlrpclib import ServerProxy
from applications.parkbz.modules.utils import TimeoutTransport
import copy
server = ServerProxy("http://ipchannels.integreen-life.bz.it/parkingFrontEnd/xmlrpc", transport=TimeoutTransport())
### TODO XML_RPC requests must be migrated to REST webservices
###
def __get_park_data(park, address_only=False):
    data = cache.ram('park_%s' % park, lambda: server.DataManager.getParkingStation(park), time_expire=3600)
    if not(isinstance(data, dict)) or ('status' in data and data['status'] != 200): 
        cache.ram('park_%s' % park, lambda: None, time_expire=0)
        raise HTTP(404)
    data = copy.deepcopy(data)  # Due to language translations, we have to work with a fresh copy of the one in cache
    name = data['name']
    data['park_id']	= park
    try:
        data['name'] = name[name.index('-') + 1:].strip()
    except:
        data['name'] = name.strip()
    data['name'] = T(data['name'], language=None)
    data['address'] = T(data['address'], language=None)
    if not(address_only):
        params={'station':park, 'type':'free'}
        r = requests.get("%s/%s" %(rest_url, "get-last-record"), params=params)
        data['freeslots'] = r.json()['value']
        data['slots_taken'] = data['slots'] - data['freeslots']
        data['slots_taken_rate'] = (data['slots_taken'] * 100) / data['slots']
        data['freeslots_rate'] = 100 - data['slots_taken_rate']
    return data

def __get_parks_info(address_only=False):
    r = requests.get("%s/%s" %(rest_url, "get-station-details"))
    parks = r.json()
	# Backward compatibility
    for p in parks:
        p['park_id'] = p['id']
        p['address'] = T(p['mainaddress'])
        try:
            p['name'] = p['name'][p['name'].index('-') + 1:].strip()
        except:
            data['name'] = p['name'].strip()
        p['name'] = T(p['name'], language=None)
        p['phone'] = p['phonenumber']
        p['slots'] = p['capacity']
        if not(address_only):
            p['freeslots'] = __get_freeslots(p['id'])
    parks_ordered = sorted(parks, key=lambda p: p['name'])
    return parks_ordered

def __get_freeslots(park_id):
    type_r = _vars('type', is_string=True) or 'free'
    period = _vars('period')
    params={'station':park_id, 'type':type_r}
    if period:
        params['period'] = period
    r = requests.get("%s/%s" %(rest_url, "get-last-record"), params=params)
    freeslots = r.json()['value']
    return freeslots

def _vars(name, single=True, post=False, is_string=False):
    var_ = request.get_vars.__getitem__(name)[0] if isinstance(request.get_vars.__getitem__(name), list) and single else request.get_vars.__getitem__(name)
    if not(var_):
        var_ = request.post_vars.__getitem__(name)[0] if isinstance(request.post_vars.__getitem__(name), list) and single else request.post_vars.__getitem__(name)
    if is_string: return str(var_) if var_ else var_
    var_ = int(var_) if var_ else None
    return var_
