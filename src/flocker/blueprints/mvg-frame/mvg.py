import requests
import time

class ApiError(Exception):
    def __init__(self, code, reason):
        self.code = code
        self.reason = reason

    def __str__(self):
        out = "Got status code {}".format(self.code)
        if self.reason:
            out += " with response {}".format(self.reason)
        return out

_API_URL = "https://www.mvg.de/api/fahrinfo"
_API_KEY = "5af1beca494712ed38d313714d4caff6"

_station_name = '/location/queryWeb?q={name}' # Leave empty for all stations
_departure = '/departure/{id}?footway={offset}'
_nearby = '/location/nearby?latitude={lat}&longitude={lon}'
_routing = '/routing/?'

_interruptions = 'https://www.mvg.de/.rest/betriebsaenderungen/api/interruptions'

def _perform_api_request(url):
    resp = requests.get(
            url,
            headers={
                'X-MVG-Authorization-Key': _API_KEY,
                'Accept': 'application/json'
                }
            )
    if not resp.ok:
        try:
            raise ApiError(resp.status_code, resp.json())
        except ValueError:
            raise ApiError(resp.status_code)
    return resp.json()

def get_name_for_id(station_id):
    all_stations = get_ids_for_satation("")
    if station_id not in all_stations.keys():
        return None
    return all_stations[station_id]

def get_ids_for_satation(name):
    """
    Queries the API for all possible stations (not addresses) that
    match the name.\n
    :ivar name: the name of the station or stop (e.g. "Trudering Bahnhof")\n
    :return: List of found IDs
    """
    # Query all names
    locations = _perform_api_request(_API_URL + _station_name.format(name=name))
    # Return if no locations have been found
    if len(locations) == 0 or 'locations' not in locations.keys():
        return {}
    # Return IDs of locations after removing all addresses
    station_ids = [l['id'] for l in locations['locations'] if l['type'] == 'station']
    station_names = ["{}, {}".format(l['name'], l['place']) for l in locations['locations'] if l['type'] == 'station']
    return dict(zip(station_ids, station_names))

def get_departures_for_id(id, limit=None):
    # Querying departures
    departures = _perform_api_request(_API_URL + _departure.format(id=id, offset=0))
    if len(departures) == 0 or 'departures' not in departures.keys():
        return []
    
    r = []
    for d in departures['departures']:
        if d['cancelled']:
            continue
        
        # Calculate departure time (value is epoch in ms) by including delay (in minutes)
        delay = int(d['delay']) * 60 if 'delay' in d.keys() else 0
        departure_time = time.localtime(int(d['departureTime']) // 1000 + delay)
        if time.mktime(departure_time) < time.time():
            continue
        r.append({
            'service': d['label'],
            'destination': d['destination'].replace(' U', '').replace(' S', ''),
            'departure': departure_time
        })

    r.sort(key=lambda d: d['departure'])

    if isinstance(limit, int) and limit > 0 and len(r) > limit:
        return r[:limit]
    return r

def get_timetable_for_station_name(name):
    station_ids = get_ids_for_satation(name)
    r = '\n'
    for station_id, station_name in station_ids.items():
        r += '{:^86s}\n'.format(station_name)
        r += get_timetable_for_station_id(station_id)
    return r

def get_timetable_for_station_id(station_id, show_id=False):
    r = ''
    if show_id:
        r = '{:^86s}\n'.format(station_id)
    r += '/' + ('-'*9) + '+' + ('-'*7) + '+' + ('-'*66) + '\\\n'
    r += '|{:^9s}|{:^7s}| {:<65s}|\n'.format("Abfahrt", "Linie", "Endstation/-haltestelle")
    r += '|' + ('-'*9) + '+' + ('-'*7) + '+' + ('-'*66) + '|\n'
    departures = get_departures_for_id(station_id)
    for d in departures:
        r += '|{departure:^9s}|{service:^7s}| {destination:<65s}|\n'.format(
            departure=time.strftime('%H:%M', d['departure']),
            service=d['service'],
            destination=d['destination']
            )
    r += '\\' + ('-'*9) + '+' + ('-'*7) + '+' + ('-'*66) + '/\n'
    return r