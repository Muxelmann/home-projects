import os
import time
from flask import Blueprint, render_template, redirect, url_for, request, current_app
from . import mvg
from . import displays

from PIL import Image, ImageFont, ImageDraw

def create_bp(app):
    bp_mvg = Blueprint('mvg-frame', __name__, url_prefix='/mvg-frame')

    displays.init(app)

    @bp_mvg.route('/index/')
    @bp_mvg.route('/')
    def index():
        return render_template('mvg-frame/index.html.j2', data=displays.data())
    
    @bp_mvg.route("/updateData/<string:mac>", methods={'GET', 'POST'})
    def update_data(mac):
        data = {}
        
        # Check if a specific station ID has been passed
        if 'station_id' in request.args:
            station_id = request.args.get('station_id')
            station_name = mvg.get_name_for_id(station_id)
            # Only set the data if ID is valid, i.e. returns a valid station name
            if station_name is not None:
                data['station_id'] = station_id
                data['station_name'] = station_name
        
        # Populate data with form inputs
        for key, value in request.form.items():
            if key in ['station_name']:
                data[key] = value
                # vv Makes sure that the old station ID is not accidentally kept
                data['station_id'] = None
            if key in ['offset_top', 'offset_bottom', 'offset_left', 'offset_right'] and value.isnumeric():
                data[key] = int(value)

        # Upate the stored data
        displays.update(mac, data)

        # Check if a station ID has already been passed / set
        if data['station_id'] is None:
            # Find all station IDs for the station name
            station_ids = mvg.get_ids_for_satation(data['station_name'])
            # If not exactly one station was found...
            if len(station_ids) == 1:
                # ... save the found station ID
                for key, value in station_ids.items():
                    displays.update(mac, {'station_id': key})
            elif len(station_ids) > 1:
                # ... or let the user choose and pass (via GET) a station ID
                return render_template('mvg-frame/index.html.j2',  mac=mac, station_ids=station_ids)

        return redirect(url_for('mvg-frame.index'))

    # Functions called from frame

    @bp_mvg.route('/update/<string:mac>')
    def update(mac):
        # Make a new empty image in the size of the screen

        img_path = os.path.join(current_app.instance_path, 'mvg-{}.png'.format(mac.replace(':', '')))
        (w, h) = displays.size_for(mac)
        img = Image.new('RGB', (w, h), (0, 0, 0))
        draw = ImageDraw.Draw(img)

        font_dir = os.path.join('/'.join(os.path.abspath(__file__).split('/')[0:-1]), 'static')
        font_normal = ImageFont.truetype(os.path.join(font_dir, 'EXCITE.otf'), 42)
        font_bold = ImageFont.truetype(os.path.join(font_dir, 'EXCITE_B.otf'), 42)

        station_id, _ = displays.station_for(mac)
        if station_id is None:
            draw.text((w/2, h/2), "STATION ERROR", fill=(255, 255, 255), font=font_bold, anchor='mm')
            img.save(img_path, 'PNG')
            return "0"

        (o_t, o_b, o_l, o_r) = displays.offset_for(mac)
        draw.polygon([
            o_l, o_t,
            o_l, h-o_b,
            w-o_r, h-o_b,
            w-o_r, o_t,
        ], fill=(255, 255, 255))

        
        # Get the departures for the station ID
        departures = mvg.get_departures_for_id(station_id, limit=7)

        if len(departures) == 0:
            draw.text((w/2, h/2), "NO DATA", fill=(0, 0, 0), font=font_bold, anchor='mm')
            img.save(img_path, 'PNG')
            return "0"
        
        # departure_times = "\n".join([time.strftime('%H:%M', d['departure']) for d in departures])
        departure_minutes = "\n".join(["{:.0f}".format((time.mktime(d['departure'])-time.time())/60) for d in departures])
        departure_service = "\n".join(["{} {}".format(d['service'], d['destination']) for d in departures])

        draw.multiline_text((o_l + 10, o_t+5), departure_minutes, font=font_bold, fill=(0, 0, 0))
        draw.multiline_text((o_l + 100, o_t+5), departure_service, font=font_normal, fill=(0, 0, 0))

        img.save(img_path, 'PNG')
        return "1"

    @bp_mvg.route('/imageData/<string:mac>') # GET: segCount & seg
    def image_data(mac):
        seg_count = int(request.args.get('segCount', default="1"))
        seg = int(request.args.get('seg', default="0"))
        
        img_path = os.path.join(current_app.instance_path, 'mvg-{}.png'.format(mac.replace(':', '')))

        img = Image.open(img_path)
        (w, h) = img.size
        img = img.rotate(180)
        crop_box = (0, seg*h/seg_count, w, (seg+1)*h/seg_count)
        img = img.crop(crop_box)
        (w, h) = img.size
        
        data = ''
        pixels = img.load()
        for y in range(h):
            for x in range(0, w, 4):
                black = [all([pixel == 0 for pixel in pixels[x+px, y]]) for px in range(4)]
                white = [all([pixel == 255 for pixel in pixels[x+px, y]]) for px in range(4)]

                new_data = ''
                for z in range(4):
                    if white[z]:
                        new_data += '11'
                    elif black[z]:
                        new_data += '00'
                    else:
                        new_data += '01'
                data += '{:02x}'.format(int(new_data, base=2))

        return data 

    @bp_mvg.route('/delayTime/<string:mac>')
    def delay_time(mac):
        return "30000"

    return bp_mvg