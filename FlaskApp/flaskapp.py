from flask import Flask, render_template
from pytileTester import main as PyTile
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

    
    map_center_coords = (41.602277, -93.654747)     # Manually set to center campus on map

    loop = asyncio.new_event_loop()
    lat, long = loop.run_until_complete(PyTile())
    loop.close()
    
    m = folium.Map(location=map_center_coords, zoom_start=17)
    folium.CircleMarker(location=(lat, long), radius=20, fill_color='red').add_to(m)

    m.get_root().width = "800px"
    m.get_root().height = "600px"
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