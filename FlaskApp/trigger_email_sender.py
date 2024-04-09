# This file is to be run every interval to test if Griff is on campus

from coordinates import *
from get_pytile_lat_long import main as Pytile
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

def read_boolean():
    if os.path.exists("boolean.txt"):
        with open("boolean.txt", "r") as file:
            return file.read().strip() == "True"
    else:
        return False  # Default value if file doesn't exist

def write_boolean(boolean_value):
    with open("boolean.txt", "w") as file:
        file.write(str(boolean_value))

def main(): 
    have_emailed = read_boolean

    if check_if_on_campus:
        if not have_emailed:
            # email_list()
            have_emailed = True
            print("emailed")
        else:
            print("on campus, but emailed already!")
            return
    else:
        have_emailed = False
        print("off campus")

    
    write_boolean(have_emailed)


if __name__=="__main__": 
    main() 