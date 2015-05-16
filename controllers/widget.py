import requests
import datetime

response.headers['access-control-allow-headers'] = 'x-requested-with'
response.headers['access-control-allow-methods'] = 'GET'
response.headers['access-control-allow-origin'] = '*'
response.headers['access-control-max-age'] = 900

def index():
    parking_id =  request.args[0] if  len(request.args) != 0 and request.args[0].isdigit() else None
    if parking_id is None:
        raise HTTP(404)
    parks = __get_parks_info()
    park = None
    for p in parks:
        if p['park_id']==parking_id:
            park = p
            break
    if park is None:
        raise HTTP(404)
        
    html = response.render('default/park_box.html', {'park':park, 'url_base':True, 'widget':True})
    script = """
        var free_slot_text = '%s';
        var capacity = '%s';
        var appName = '%s';
        var data_not_available_str = '%s';
    """ % ("Free slots", "Capacity", request.application, "Predictions currently unavailable")
    return response.json({'plain_html':html, 'plain_script':script})
