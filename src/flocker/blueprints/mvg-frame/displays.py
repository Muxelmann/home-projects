import pickle
import os

DATASTORE = {}
DATASTORE_PATH = None

def init(app):
    global DATASTORE_PATH, DATASTORE
    if DATASTORE_PATH is None:
        DATASTORE_PATH = os.path.join(app.instance_path, 'mvg-display-data.pkl')

    if not os.path.exists(DATASTORE_PATH):
        with open(DATASTORE_PATH, 'wb') as f:
            pickle.dump(DATASTORE, f)
    else:
        with open(DATASTORE_PATH, 'rb') as f:
            DATASTORE = pickle.load(f)

def _set_data(mac, data={}):
    global DATASTORE

    # Check if an entry exists and set default if not
    if mac not in DATASTORE.keys():
        DATASTORE[mac] = {
            'station_name': "Trudering, München",
            'station_id': None,
            'width': 640,
            'height': 384,
            'offset_top': 0,
            'offset_bottom': 0,
            'offset_left': 0,
            'offset_right': 0
        }
    
    # Update entry with the new data
    for key, value in data.items():
        if key in DATASTORE[mac].keys():
            DATASTORE[mac][key] = value

    # Save the updated datastore
    with open(DATASTORE_PATH, 'wb') as f:
        pickle.dump(DATASTORE, f)
    
    return DATASTORE[mac]

def _get_data(mac):
    # Check if an entry exists and get default if not
    if mac not in DATASTORE.keys():
        return _set_data(mac)
    elif len(DATASTORE) == 0:
        return None
    return DATASTORE[mac]

def update(mac, data):
    _set_data(mac, data)

# def update(mac, station=None, offset_top=None, offset_bottom=None, offset_left=None, offset_right=None):
#     data = {}
#     if station is not None and isinstance(station, str):
#         data['station'] = station
#     if offset_top is not None and isinstance(offset_top, int):
#         data['offset_top'] = offset_top
#     if offset_bottom is not None and isinstance(offset_bottom, int):
#         data['offset_bottom'] = offset_bottom
#     if offset_left is not None and isinstance(offset_left, int):
#         data['offset_left'] = offset_left
#     if offset_right is not None and isinstance(offset_right, int):
#         data['offset_right'] = offset_right
#     _set_data(mac, data)

def data():
    """
    Returns the datastore
    """
    return DATASTORE

def station_for(mac):
    """
    Returns the station-tuple (id, name) associated to a mac address
    """
    d = _get_data(mac)
    return (d['station_id'], d['station_name'])

def size_for(mac):
    """
    Returns the size (width, height) associated to a mac address
    """
    d = _get_data(mac)
    return (d['width'], d['height'])

def offset_for(mac):
    """
    Returns a tuple (top, bottom, left, right) containing the offsets for a mac address
    """
    d = _get_data(mac)
    return (d['offset_top'], d['offset_bottom'], d['offset_left'], d['offset_right'])
