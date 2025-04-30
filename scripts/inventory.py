from io_scripts import gmap2inv
from io_scripts import obs_orientation
import numpy as np

inv = gmap2inv('/local/lyakuden/offshore_bc/bc-multiplets/data/2008-triplet-gmap.txt', '*', 'BHZ,HHZ,BH1,HH1,BH2,HH2,BHN,HHN,BHE,HHE,HNE,HNN,HNZ')
# inv = obs_orientation(inv, '/local/lyakuden/offshore_bc/bc-multiplets/data/obs-orientations.txt')

remove_net = []
remove_sta = []

# remove stations whose **1 and **2 azimuths don't differ by 90, -90, 270, or -270
for network in inv:
    for station in network:
        for channel in station:
            if channel.code[-1] == '1':
                az1 = channel.azimuth
            elif channel.code[-1] == '2':
                az2 = channel.azimuth
                if np.abs(az1 - az2) not in [90, -90, 270, -270]:
                    remove_sta.append(station.code)
                    remove_net.append(network.code)

for net, sta in zip(remove_net, remove_sta):
    inv = inv.remove(network=net, station=sta)

inv.write('/local/lyakuden/offshore_bc/bc-multiplets/data/2008-stations.xml', format='STATIONXML')
