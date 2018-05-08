
import netCDF4
import matplotlib
import psycopg2
import numpy as np
from tqdm import tqdm
import geopandas as gpd
matplotlib.use('agg')
import matplotlib.pyplot as plt

PROJSTR = ('+proj=omerc +lat_0=37.5 +alpha=90.0 +lonc=264.0 +x_0=0. '
           '+y_0=0. +ellps=sphere +a=6371229.0 +b=6371229.0 +units=m +no_defs')

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = world[world['name'] == 'United States']
world = world.to_crs(PROJSTR)
print(world['name'])

pgconn = psycopg2.connect('dbname=postgis')
huc12df = gpd.GeoDataFrame.from_postgis("""
SELECT state_abbr, ST_Transform(the_geom, %s) as geo from states
where state_abbr = 'IA'
""", pgconn, params=(PROJSTR,), index_col='state_abbr', geom_col='geo')

nc = netCDF4.Dataset(("/mnt/nrel/akrherz/cori/regcm4_erai_12km/singlevar/"
                      "regcm4_erai_12km_uas.1989.nc"))
nc = netCDF4.Dataset('/tmp/tasmax.nc')
nc2 = netCDF4.Dataset('/tmp/tasmin.nc')
xaxis = nc.variables['jx']
yaxis = nc.variables['iy']

for i in tqdm(range(365)):
    (fig, ax) = plt.subplots(1, 1)
    ax.set_title("'Daily' tasmax - tasmin t=%s" % (i, ))
    data = nc.variables['tas'][i, 0, :, :] - nc2.variables['tas'][i, 0, :, :]
    res = ax.pcolormesh(xaxis, yaxis, data, vmin=0, vmax=40,
                        cmap=plt.get_cmap('viridis'))
    huc12df.plot(ax=ax, facecolor="None", edgecolor='white')
    world.plot(ax=ax, facecolor="None", edgecolor='white')
    fig.colorbar(res, label='C')
    ax.set_xlim(xaxis[0], xaxis[-1])
    # ax.set_xlim(1947819 - 100000, 2280112 + 100000)
     #ax.set_ylim(895740 - 100000, 1415861 + 100000)
    ax.set_ylim(yaxis[0], yaxis[-1])
    ax.set_xticks([])
    ax.set_yticks([])

    fig.savefig('frame%03i.png' % (i, ))
    plt.close()
