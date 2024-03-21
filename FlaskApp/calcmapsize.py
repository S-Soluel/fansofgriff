import math

def calc_map_size_from_desired_width(lat_a, long_a, lat_b, long_b, desired_width):

    # Calculate the width and height of the map area in meters
    radius_of_earth = 6371000  # in meters
    lat_difference = math.radians(lat_a - lat_b)
    long_difference = math.radians(long_a - long_b)
    width = radius_of_earth * long_difference * math.cos(math.radians((lat_a + lat_b) / 2))
    height = radius_of_earth * lat_difference

    # Calculate the aspect ratio
    aspect_ratio = width / height

    # Set the desired width of the map
    desired_width = 900  # in pixels

    # Calculate the height based on the aspect ratio
    desired_height = int(desired_width / aspect_ratio)

    return desired_height