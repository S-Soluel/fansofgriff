
from flask import Flask, render_template, request, redirect, url_for, flash, session
import secrets
from pytileTester import main as PyTile
from calcmapsize import calc_map_size_from_desired_width as calcheight
from turbo_flask import Turbo
import asyncio, time, random
import folium
from email_functions import *
import threading

app = Flask(__name__, static_url_path='/static')
app.config["SESSION_PERMANENT"] = False
app.secret_key = secrets.token_bytes(32)
app.config['SESSION_TYPE'] = 'filesystem'

# ------------------------------------

turbo = Turbo(app)

def update_load():
    while True:
        try:
            with app.app_context():
                print("test")
                turbo.push(turbo.replace(render_template('loadmap.html'), 'load'))
        except Exception as e:
            print(f"Error in update_load: {str(e)}")
        time.sleep(5)
    
events = [
    {
        'todo' : 'Relays Opening',
        'date' : '04-26-2024',
    },
    {
        'todo' : 'Beautiful Bulldog Contest',
        'date' : '04-20-2024'
    }
]


@app.route('/')
def hello():
    griff_icon = "https://griffcapstone.s3.us-east-2.amazonaws.com/images.png"
    lat_a, long_a = 41.607283, -93.659769  # Top left corner of campus
    lat_b, long_b = 41.600262, -93.649731  # Bottom right corner of campus
    map_center_coords = ((lat_a + lat_b) / 2, (long_a + long_b) / 2)

    desired_width = 1000     # width of map on webpage, used to calc the height
    desired_height = -1 * calcheight(lat_a, long_a, lat_b, long_b, desired_width)

    loop = asyncio.new_event_loop()
    lat, long = loop.run_until_complete(PyTile())
    loop.close()

    m = folium.Map(
        location=map_center_coords, 
        zoom_start=17, bounds=[(lat_a, long_a), (lat_b, long_b)], 
        zoom_control=False, 
        dragging=False, 
        scrollWheelZoom=False, 
        touchZoom=False, 
        doubleClickZoom=False, 
        boxZoom=False, 
        keyboard=False, 
        tap=False
    )

    standard_icon = folium.Icon(color='darkblue', icon_color='white', icon="dog", angle=0, prefix='fa')
    folium.Marker(location=(lat, long), tooltip="Griff is here!", icon=standard_icon).add_to(m)

    m.get_root().width = f"{desired_width}px"
    m.get_root().height = f"{desired_height}px"
    iframe = m.get_root()._repr_html_()

    return render_template('landing.html', lat=lat, long=long, iframe=iframe)

def get_tile_data():
    # Simulate fetching tile data synchronously
    return 41.603062, -93.653819

# Define route for the calendar page
@app.route('/calendar')
def calendar():
    # Add logic to render the calendar page
    return render_template('calendar.html')

@app.context_processor
def inject_load():
    loop = asyncio.new_event_loop()
    lat, long = loop.run_until_complete(PyTile())
    loop.close()
    lat2 = random.randrange(100) + lat
    long2 = random.randrange(100) + long
    print(lat2)
    print(long2)
    return {'lat2': lat2, 'long2': long2}

# Define route for the email notifications page
@app.route('/notifications', methods = ["GET", "POST"])
def email_notifications():
    if request.method == "POST":
        email = request.form['submit_email']
        fname = request.form['submit_fname']
        lname = request.form['submit_lname']
        try:
            subscribe(email, fname, lname)
            flash('You have successfully signed up for Griff Tracker Alerts!', 'success')  # 'success' is a category; makes a green banner at the top
            # Add logic to render the email notifications page
            return render_template('notifications.html')
        except:
            flash('The email you entered has already subscribed to Griff Tracker Alerts', 'warning')  # 'success' is a category; makes a green banner at the top
            return render_template('notifications.html')
        
    else:
        return render_template('notifications.html')


@app.route('/unsubscribe', methods = ["GET", "POST"])
def email_unsubscribe():
    if request.method == "POST":
        email = request.form['unsub_email']
        unsubscribe(email)

        flash('You have successfully unsubscribed from Griff Tracker Alerts!', 'success')  # 'success' is a category; makes a green banner at the top
        return render_template('notifications.html')
    else:
        return render_template('unsubscribe.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    threading.Thread(target=update_load).start()
