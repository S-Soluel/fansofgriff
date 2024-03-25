from flask import Flask, render_template
from pytileTester import main as PyTile
from calcmapsize import calc_map_size_from_desired_width as calcheight
import asyncio
import folium



app = Flask(__name__)

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


    desired_width = 800     # width of map on webpage, used to calc the height
    desired_height = -1 * calcheight(lat_a, long_a, lat_b, long_b, desired_width)
    print(desired_height)

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

    custom_icon = folium.CustomIcon(griff_icon, icon_size=(40, 40))
    #folium.Marker(location=(lat, long), icon=custom_icon).add_to(m)
    standard_icon = folium.Icon(color='darkblue', icon_color='white', icon="dog", angle=0, prefix='fa')

    folium.Marker(location=(lat, long), tooltip="Griff is here!", icon=standard_icon).add_to(m)

    m.get_root().width = f"{desired_width}px"
    m.get_root().height = f"{desired_height}px"
    iframe = m.get_root()._repr_html_()

    return render_template('landing.html', lat=lat, long=long, iframe=iframe)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html', events = events)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)