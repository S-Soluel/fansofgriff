from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session, json
import secrets
from get_pytile_lat_long import main as PyTile
from trigger_email_sender import check_if_on_campus as checker
import asyncio
from email_functions import *
from coordinates import *

app = Flask(__name__, static_folder='/static')
app.config["SESSION_PERMANENT"] = False
app.secret_key = secrets.token_bytes(32)
app.config['SESSION_TYPE'] = 'filesystem'

# ------------------------------------
@app.route('/')
def hello():
    return render_template('landing.html')

@app.route('/map_data', methods = ['GET'])
def map_data():
    marker_lat = 0
    marker_long = 0

    # Only give the actual numbers if we are on campus
    if checker():
        loop = asyncio.new_event_loop()
        marker_lat, marker_long = loop.run_until_complete(PyTile())
        loop.close()

    data = {'latitude': lat_center_coord, 
            'longitude': long_center_coord,
            'markerlat': marker_lat,
            'markerlong': marker_long,
            'lat_a': lat_a,
            'lat_b': lat_b,
            'long_a': long_a,
            'long_b': long_b,
    }
    return jsonify(data)

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

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
        try:
            # try block for calling the unsubscribe function
            unsubscribe(email)
            flash('You have successfully unsubscribed from Griff Tracker Alerts!', 'success')  # 'success' is a category; makes a green banner at the top
            
            return render_template('notifications.html')
        except:
            temp_message = 'An error occurred. The following email is not subscribed to the Griff Tracker, or is not a valid email: ' + email 
            flash(temp_message, 'warning')
            return render_template('notifications.html')
    else:
        return render_template('unsubscribe.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
