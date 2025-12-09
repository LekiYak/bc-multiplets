import numpy as np
import matplotlib.colors as mcolors

def gmap2inv(txtfile, location, channel):
    """
    Converts a list of inventory stations from IRIS (i.e. gmap-stations.txt) into an Obspy inventory.

    INPUTS:
    txtfile: str
        Path to the text file containing the station information.

    location: str
        Location code of the station.

    channel: str 
        Channel code of the station. 

    OUTPUTS:
    inv: Obspy inventory object
        Inventory object containing the station information.
    """

    import obspy
    from obspy.clients.fdsn.client import Client
    from collections import Counter
    client = Client('IRIS')

    # Read the text file
    file = open(txtfile, 'r')
    lines = file.readlines()
    file.close()

    # Remove header
    lines = lines[3:]

    # Initialize lists  
    networks = []
    stations = []

    # Split the lines
    for line in lines:
        line = line.split('|')
        if len(line) < 2:
            continue
        networks.append(line[0])
        stations.append(line[1])

    # Count the number of stations in each network
    # and create a dictionary with the network and the number of stations
    networks_set = set(networks)

    inv = obspy.Inventory()
    for network in networks_set:
        
        # Get a list of stations in the network
        network_stations = [station for station, net in zip(stations, networks) if net == network]
        network_stations_string = ','.join(network_stations)

        # Get the inventory for the network
        try:
            inv += client.get_stations(network=network, station=network_stations_string, location=location, channel=channel, level='response')
            print('Downloaded network: %s' % network)
        except:
            # print('Failed to download network: %s' % network)
            continue
        
    return inv
    
def obs_orientation(inv, correction_file, **kwargs):
    """"
    Updates the orientations of OBS stations in an Obspy inventory using a corrections file.

    INPUTS:
    inv: Obspy inventory object
        Inventory object containing network and station metadata

    correction_file: str
        Path to text file containing corrections for stations in the format:
        HEADER
        STATION BH1_ORIENTATION 
        where BH1_ORIENTATION is assumed to be 90 degrees counterclockwise from BH2

    OPTIONAL INPUTS:
    accepted_error: int or float
        Azimuthal uncertainty 2-standard dev. threshhold (in degrees). 
        Stations whose azimuth estimate carries a 2sd error greater than this input will not be updated.

    OUTPUTS:
    inv: Obspy inventory object
        Inventory object with updated station orientations.
    """

    #------------------------------#
    # READING THE CORRECTIONS FILE #
    #------------------------------#

    accepted_error = kwargs.get('accepted_error', 180)

    # Open corrections file
    file = open(correction_file, 'r')
    lines = file.readlines()
    file.close()

    # Remove header
    lines = lines[1:]

    # Initialize station and orientation lists
    corrected_stations = []
    azimuths = []
    errors   = []

    # If there are no errors (error column empty)
    # replace all errors with 0
    if len(lines[0].split(' ')) < 3:
        errors = [0] * len(lines)

    # Iterate offover lines to add stations, azimuths, and errors to lists
    for line in lines:
        line = line.split(' ')
        
        # Checks if the error of this station is above the threshold
        # skips this iteration (station) if true
        if int(line[2]) > accepted_error:
            continue

        corrected_stations.append(line[0]) # Appending station
        azimuths.append(int(line[1])) # Appending azimuth
        errors.append(int(line[2]))   # Appending error

    #------------------------#
    # UPDATING THE INVENTORY #
    #------------------------#

    temp_list = []

    for network in inv:
        for station in network:
            if station.code == 'J50C':
                print(station.channels, station.code in corrected_stations)
            if station.code in corrected_stations: # Found station that needs correction

                index = corrected_stations.index(station.code) # Index of station
                primary_orientation = azimuths[index] # Fetching corresponding azimuthal correction
                secondary_orientation = primary_orientation + 90 # **2 is 90 degrees clockwise of **1
                if secondary_orientation > 360:
                    secondary_orientation -= 360

                for channel in station.channels:
                    if channel.code.endswith('1'): # **1, or primary orientation
                        channel.azimuth = primary_orientation
                        channel.dip = 0
                    elif channel.code.endswith('2'): # **2, or secondary orientation
                        channel.azimuth = secondary_orientation
                        channel.dip = 0

                # print(network.code, station.code, primary_orientation)

                # print(f'Updated orientation of {station.code} to {primary_orientation}')

    return inv

def read_nedb(nedb_filepath):
    """
    Reads a catalog in the NEDB format (| delimiters) and outputs a pandas dataframe of the catalog.
    The dataframe has appropriate data types (i.e. datetime instead of string) and column names (lowercase).
    
    INPUTS:
    nedb_filepath: str
        Path to the NEDB file.

    OUTPUTS:
    df: pandas dataframe
        Dataframe containing the catalog information.
    
    """

    import pandas as pd

    # read the NEDB file
    data = pd.read_csv(nedb_filepath, delimiter='|')

    # change column names to lower case and fix types
    data['time'] = pd.to_datetime(data['Time'])
    data['time'] = data['time'].dt.tz_localize(None)
    data['latitude'] = data['Latitude'].astype(float)
    data['longitude'] = data['Longitude'].astype(float)
    data['depth'] = data['Depth/km'].astype(float)
    data['magnitude'] = data['Magnitude'].astype(float)
    data['magtype'] = data['MagType']
    data['eventlocationname'] = data['EventLocationName']
    data['eventid'] = data['#EventID'].astype(str)

    # drop the original columns
    data = data.drop(columns=['Time', 'Latitude', 'Longitude', 'Depth/km', 'Magnitude', 'MagType', 'EventLocationName', '#EventID'])

    return data

def cpt2rgb(cpt_file, value):
    z_vals = []
    rgb_vals = []
    with open(cpt_file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(("#", "B", "F", "N")):
                continue
            parts = line.split()
            if len(parts) < 4:
                continue
            try:
                z1 = float(parts[0])
                c1 = parts[1]
                z2 = float(parts[2])
                c2 = parts[3]

                def parse_color(c):
                    if "/" in c:
                        return np.array(list(map(float, c.split("/"))))
                    else:
                        return np.array(mcolors.to_rgb(c)) * 255  # convert to 0–255 scale

                rgb1 = parse_color(c1)
                rgb2 = parse_color(c2)

                z_vals.extend([z1, z2])
                rgb_vals.extend([rgb1, rgb2])
            except Exception as e:
                print(f"Skipping line: {line} -- Error: {e}")

    if not z_vals:
        raise ValueError("No valid color entries found in CPT.")
    zipped = sorted(set(zip(z_vals, [tuple(rgb) for rgb in rgb_vals])))
    z_vals = np.array([z for z, _ in zipped])
    rgb_vals = np.array([rgb for _, rgb in zipped])

    if value <= z_vals[0]:
        return rgb_vals[0]
    elif value >= z_vals[-1]:
        return rgb_vals[-1]
    idx = np.searchsorted(z_vals, value) - 1
    z1, z2 = z_vals[idx], z_vals[idx + 1]
    rgb1, rgb2 = rgb_vals[idx], rgb_vals[idx + 1]
    t = (value - z1) / (z2 - z1)
    return np.round((1 - t) * rgb1 + t * rgb2).astype(int)

    return np.round((1 - t) * rgb1 + t * rgb2).astype(int)