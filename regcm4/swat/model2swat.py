"""Dump regcm4 data to SWAT files

We had a discussion on using the 0z to 0z summary data or computing 6z to 6z
totals from the 3-hourly or hourly files.  We appear to be going with the
6z to 6z option

The SRF files contain the following. For most runs they are written every 3
hours but recently I have been specifying 1 hour frequency:

surface (10 m) u wind (uas), instantaneous
surface (10 m) v wind (vas), instantaneous
surface (2 m) specific humidity (qas), instantaneous
surface (2 m) temperature (tas), instantaneous
time mean precipitation rate (pr)
time mean incident SW (rsds)
time mean net SW, i.e. incident minus reflected (rsns)

/opt/miniconda2/bin/ncrcat -v uas regcm4_erai_12km_SRF.*.nc ../singlevar/regcm4_erai_12km_uas.nc

"""
from __future__ import print_function
import sys

import netCDF4
import psycopg2
import numpy as np
from affine import Affine
import geopandas as gpd
from rasterstats import zonal_stats
import pandas as pd

PROJSTR = ('+proj=omerc +lat_0=37.5 +alpha=90.0 +lonc=264.0 +x_0=0. '
           '+y_0=0. +ellps=sphere +a=6371229.0 +b=6371229.0 +units=m +no_defs')



def main(argv):
    """Go Main Go"""
    pgconn = psycopg2.connect('dbname=idep')
    huc12df = gpd.GeoDataFrame.from_postgis("""
    SELECT huc12, ST_Transform(simple_geom, %s) as geo from wbd_huc12
    WHERE swat_use
    """, pgconn, params=(PROJSTR,), index_col='huc12', geom_col='geo')
    nc = netCDF4.Dataset(("/mnt/nrel/akrherz/cori/regcm4_erai_12km/singlevar/"
                          "regcm4_erai_12km_uas.1989.nc"))
    ncaffine = Affine(nc.getncattr('grid_size_in_meters'), 0.,
                      nc.variables['jx'][0],
                      0.,
                      0 - nc.getncattr('grid_size_in_meters'),
                      nc.variables['iy'][-1])
    pcp = np.flipud(nc.variables['uas'][10, 0, :, :])
    print(np.shape(pcp))
    # nodata here represents the value that is set to missing within the
    # source dataset!, setting to zero has strange side affects
    zs = zonal_stats(huc12df['geo'], pcp, affine=ncaffine, nodata=-1,
                     all_touched=True)
    i = 0
    for huc12, _ in huc12df.itertuples():
        print(zs[i]['mean'])
        i += 1


if __name__ == '__main__':
    main(sys.argv)
