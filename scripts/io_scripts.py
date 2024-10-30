def gmap2inv(txtfile, location, channel):
    """
    Converts a list of inventory =stations from IRIS (i.e. gmap-stations.txt) into an Obspy inventory object.

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
    