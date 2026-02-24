import numpy as np
import obspy
from obspy.core import read, Stream, Trace, UTCDateTime
from obspy.clients.fdsn.client import Client
from glob import glob
from obspy.clients.fdsn.mass_downloader import (
    CircularDomain,
    Restrictions,
    MassDownloader,
)

# def download_mseed(network, station, channel, tstart, tend, output_dir):
#     st = Stream()
    
#     try:
#         try:
#             client = Client('IRIS')
#             st += client.get_waveforms(network=network, station=station, location='*', channel=channel, starttime=tstart, endtime=tend, attach_response=False)
#         except Exception as e:
#             client = Client('https://www.earthquakescanada.nrcan.gc.ca')
#             st += client.get_waveforms(network=network, station=station, location='*', channel=channel, starttime=tstart, endtime=tend, attach_response=False)
#     except Exception as e:
#         print(f"Failed to download {network}.{station}.{channel} from {tstart} to {tend}: {e}")

#     if len(st) != 0:
#         # separate by channel
#         for tr in st:
#             tr.stats.channel = tr.stats.channel.strip()

#             # save mseed
#             tstart_str = tstart.strftime('%Y%m%dT%H%M%S')
#             tend_str = tend.strftime('%Y%m%dT%H%M%S')
#             filename = f"{network}.{station}..{tr.stats.channel}__{tstart_str}__{tend_str}.mseed"
#             tr.write(output_dir + filename, format='MSEED')
#             print("Saved", filename)

# # run 1 day chunks on station PHC CN
# start_date = UTCDateTime("2000-01-01T00:00:00.000")
# end_date   = UTCDateTime("2025-01-01T00:00:00.000")

# get number of days between start and end date
# num_days = int((end_date - start_date) / (24 * 60 * 60))

# loop over station xml list to get network and station codes

# for stationxml in glob('/local/lyakuden/offshore_bc/bc-multiplets/data/station_xmls/stations/*.xml'):
#     filename = stationxml.split('/')[-1]
#     network = filename.split('.')[0]
#     station = filename.split('.')[1]

#     # break
# for day in range(num_days):
#     tstart = start_date + day * 24 * 60 * 60
#     tend   = tstart + 24 * 60 * 60
#     download_mseed(network, station, '*', tstart, tend, '/mckenzie/lyakuden/multiplet-data/2008/relocation/2000-2025/waveforms/')

# Start and end time of waveforms
starttime = UTCDateTime("2008-01-01T00:00:00.000")
endtime   = UTCDateTime("2025-08-01T00:00:00.000")

domain = CircularDomain(
    latitude=51.2, longitude=-131, minradius=0, maxradius=15
)

# see https://docs.obspy.org/packages/autogen/obspy.clients.fdsn.mass_downloader.html
restrictions = Restrictions(
    starttime=starttime,
    endtime=endtime,
    reject_channels_with_gaps=False,
    #channel="", # use all available channels if not provided
    channel_priorities=['BHZ', 'HHZ'], #['BH*','HH*', 'EH*'],
    network='CN',#AV,TA,NC,US,CN',#,CN,EC,II,KZ,N4,HE,GB,DK',#['CN', 'EC', 'II', 'IU', 'KZ', 'N4'], # use all available networks if not provided
    station="BUTB,GRIB,GRNB,HWKB,KITB,SHB,NCSB,NCRB,BNAB,RUBB,PCLB,DI2B,TAHB,BPEB,NTKA,TOFB,OZB,WRAK,SNB,FHBB,HAKB,BFSB,MGRB,BCH07,BCH16,BCH26,EDB,BCH18,BCC01,BCH21,BCH08,BCH14,V35K,FSJB,BCH04,BCH11,TXDB,NBC8,BCOV",#'CLRN,MNTQ,GUMO,SCHQ,COHC,LVZ,HKT,KIP,MAJO,OTAV,PAYG,SJG,WAKE,WCI,WVT,YAK,BVAR,KNDC,SS1A,FRB,PTCN',
    location="*",
    minimum_length = 0.5,
    sanitize=False,
    chunklength_in_sec=86400,  # 1 day
)

eventid = '2008'

# use all available providers
mdl = MassDownloader(providers=['IRIS','https://www.earthquakescanada.nrcan.gc.ca'])

# Get the data (if available) and write to output file
mdl.download(domain, restrictions, 
             mseed_storage=f'/mckenzie/lyakuden/multiplet-data/{eventid}/relocation/2000-2025/waveforms/', 
             stationxml_storage=f'/mckenzie/lyakuden/multiplet-data/{eventid}/relocation/2000-2025/stations/')
