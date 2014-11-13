# Return basic info for all available parking lots
def __get_parks_info(address_only=False):
    r = requests.get("%s/%s" %(rest_url, "get-station-details"))
    if 'exceptionMessage' in r.json():
        return []
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
            value = __get_last_value(_parking_id = p['id'])
            p['freeslots'] = value['freeslots'] if 'freeslots' in value else -1
    parks_ordered = sorted(parks, key=lambda p: p['name'])
    return parks_ordered

# return the last available value if valid (not out-of-date)
def __get_last_value(_type=None, _period=None, _parking_id=None, _seconds=None, with_timestamp=False):
    params={}
    params['station'] = _parking_id or _vars('parking_id')
    params['name'] = _type or _vars('type', is_string=True) or 'free'
    params['seconds'] = _seconds or 1800
    period = _period or _vars('period')
    if period:
        params['period'] = period

    r = requests.get("%s/%s" %(rest_url, "get-records"), params=params)
    data=r.json()

    if 'exceptionMessage' in data or len(data) == 0:
        return r.json()

    obj=data[len(data)-1]
    t = datetime.datetime.fromtimestamp(obj['timestamp']/1e3) + datetime.timedelta(seconds=3600)
    if t < request.now:
        return response.json({})
    response = {'freeslots':obj['value']}
    if params['name'] != 'free':
        created_on = datetime.datetime.fromtimestamp(obj['created_on']/1e3)
        response['created_on'] = "%s:%s" %(created_on.hour, created_on.minute)

    if with_timestamp:
        response['timestamp'] = obj['timestamp']
    return response

def _vars(name, single=True, post=False, is_string=False):
    var_ = request.get_vars.__getitem__(name)[0] if isinstance(request.get_vars.__getitem__(name), list) and single else request.get_vars.__getitem__(name)
    if not(var_):
        var_ = request.post_vars.__getitem__(name)[0] if isinstance(request.post_vars.__getitem__(name), list) and single else request.post_vars.__getitem__(name)
    if is_string: return str(var_) if var_ else var_
    var_ = int(var_) if var_ else None
    return var_
