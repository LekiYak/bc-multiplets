def gmap2inv(txtfile, location, channel):
    """
    Converts a list of inventory =stations from IRIS (i.e. gmap-stations.txt) into an Obspy inventory object.

    INPUTS:
    txtfile: str
        Path to the text file containing the station information.

    OUTPUTS:
    inv: Obspy inventory object
        Inventory object containing the station information.
    """

    import obspy
    from obspy.clients.fdsn.client import Client
    client = Client('IRIS')

    # Read the text file
    file = open(txtfile, 'r')
    lines = file.readlines()
    file.close()

    # Remove header
    lines = lines[3:]

    # Initialize lists  
    network = []
    station = []

    # Split the lines
    for line in lines:
        line = line.split('|')
        if len(line) < 2:
            continue
        network.append(line[0])
        station.append(line[1])

    # Create inventory object
    inv = obspy.Inventory()
    for network, station in zip(network, station):
        # continue if exception is raised
        try:
            inv += client.get_stations(network=network, station=station, location=location, channel=channel, level='response')
        except:
            print('Failed to download station: %s.%s' % (network, station))
            continue

    return inv
    