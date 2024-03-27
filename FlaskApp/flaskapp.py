from flask import Flask, render_template
from calcmapsize import calc_map_size_from_desired_width as calcheight
import folium

app = Flask(__name__)

@app.route('/')
def hello():
    griff_icon = "https://griffcapstone.s3.us-east-2.amazonaws.com/images.png"
    lat_a, long_a = 41.607283, -93.659769  # Top left corner of campus
    lat_b, long_b = 41.600262, -93.649731  # Bottom right corner of campus
    map_center_coords = ((lat_a + lat_b) / 2, (long_a + long_b) / 2)

    desired_width = 1000     # width of map on webpage, used to calc the height
    desired_height = -1 * calcheight(lat_a, long_a, lat_b, long_b, desired_width)

    # Call get_tile_data function to get tile data synchronously
    lat, long = get_tile_data()

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

@app.route('/')
def home():
    return render_template('landing.html')

# Define route for the calendar page
@app.route('/calendar')
def calendar():
    # Add logic to render the calendar page
    return render_template('calendar.html')

# Define route for the email notifications page
@app.route('/emails')
def notifications():
    # Add logic to render the email notifications page
    return render_template('email_notifications.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
