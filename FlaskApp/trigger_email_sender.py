# This file is to be run every interval to test if Griff is on campus

from coordinates import *
from get_pytile_lat_long import main as Pytile
from email_functions import send_email
import asyncio
import os

def check_if_on_campus():
    loop = asyncio.new_event_loop()
    tracker_lat, tracker_long = loop.run_until_complete(Pytile())
    loop.close()

    latitude_passed = False
    longitude_passed = False

    if (lat_a > tracker_lat > lat_b):
        latitude_passed = True
    

    if (long_a < tracker_long < long_b):
        longitude_passed = True

    return latitude_passed and longitude_passed

import os

def read_boolean():
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "boolean.txt")
    if os.path.exists(file_path):
        print("Found boolean.txt")
        with open(file_path, "r") as file:
            content = file.read().strip()
            print("Content:", content)
            return content == "True"
    else:
        print("boolean.txt not found")
        return False  # Default value if file doesn't exist

# Test the function
print("Boolean value:", read_boolean())
print (check_if_on_campus())

def write_boolean(boolean_value):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "boolean.txt")
    if os.path.exists(file_path):
        print("Found boolean.txt")
        with open(file_path, "w") as file:
            file.write(str(boolean_value))
            file.close()
            print("Wrote to boolean.txt= ", boolean_value)
            return True
    else:
        print("boolean.txt not found")
        return False  # Default value if file doesn't exist

def main(): 
    have_emailed = read_boolean()

    if check_if_on_campus:
        if not have_emailed:
            send_email('Griff_Sighting')
            have_emailed = True
            print("emailed")
        else:
            print("on campus, but emailed already!")
            return
    else:
        have_emailed = False
    
    write_boolean(have_emailed)


if __name__=="__main__": 
    main() 