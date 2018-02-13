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

/opt/miniconda2/bin/ncrcat -v uas regcm4_erai_12km_SRF.*.nc
    ../singlevar/regcm4_erai_12km_uas.nc

tasmax and tasmin
-----------------
/opt/miniconda2/bin/ncra -O --mro -d time,6,,24,24 -v tas -y min
    regcm4_erai_12km_tas.????.nc ../daily6z/regcm4_erai_12km_tasmin.nc
/opt/miniconda2/bin/ncra -O --mro -d time,6,,24,24 -v tas -y max
    regcm4_erai_12km_tas.????.nc ../daily6z/regcm4_erai_12km_tasmax.nc

precip
------
/opt/miniconda2/bin/ncra -O --mro -d time,6,,24,24 -v pr -y avg
    regcm4_erai_12km_pr.????.nc ../daily6z/regcm4_erai_12km_pr.nc


wind
----
/opt/miniconda2/bin/ncks -A regcm4_erai_12km_uas.1989.nc
    regcm4_erai_12km_vas.1989.nc
mv regcm4_erai_12km_vas.1989.nc regcm4_erai_12km_uas_vas.1989.nc
rm regcm4_erai_12km_uas.1989.nc
# the -6 appears to allow it to even work
/opt/miniconda2/bin/ncap2 -6 -O -s 'sped=sqrt(pow(uas,2)+pow(vas,2))'
    regcm4_erai_12km_uas_vas.1989.nc regcm4_erai_12km_sped.1989.nc

"""
from __future__ import print_function
import sys
import datetime
from collections import namedtuple

from tqdm import tqdm
import netCDF4
import numpy as np
from affine import Affine
import geopandas as gpd
from pyiem.grid.zs import CachingZonalStats
from pyiem.util import get_dbconn
from pyiem.datatypes import temperature

GRIDINFO = namedtuple("GridInfo", ['x0', 'y0', 'xsz', 'ysz', 'mask'])
PROJSTR = ('+proj=omerc +lat_0=37.5 +alpha=90.0 +lonc=264.0 +x_0=0. '
           '+y_0=0. +ellps=sphere +a=6371229.0 +b=6371229.0 +units=m +no_defs')
BASEDIR = "/mnt/nrel/akrherz/cori/regcm4_erai_12km/daily6z"


def get_basedate(ncfile):
    """Compute the dates that we have"""
    nctime = ncfile.variables['time']
    basets = datetime.datetime.strptime(nctime.units,
                                        "hours since %Y-%m-%d 00:00:00 UTC")
    ts = basets + datetime.timedelta(hours=float(nctime[0]))
    return datetime.date(ts.year, ts.month, ts.day), len(nctime[:])


def main(argv):
    """Go Main Go"""
    pgconn = get_dbconn('idep')
    huc12df = gpd.GeoDataFrame.from_postgis("""
    SELECT huc12, ST_Transform(simple_geom, %s) as geo from wbd_huc12
    WHERE swat_use ORDER by huc12
    """, pgconn, params=(PROJSTR,), index_col='huc12', geom_col='geo')
    hucs = huc12df.index.values
    tasmax_nc = netCDF4.Dataset(BASEDIR + "/regcm4_erai_12km_tasmax.nc")
    tasmin_nc = netCDF4.Dataset(BASEDIR + "/regcm4_erai_12km_tasmin.nc")
    pr_nc = netCDF4.Dataset(BASEDIR + "/regcm4_erai_12km_pr.nc")

    # compute the affine
    ncaffine = Affine(pr_nc.getncattr('grid_size_in_meters'),
                      0.,
                      pr_nc.variables['jx'][0],
                      0.,
                      0 - pr_nc.getncattr('grid_size_in_meters'),
                      pr_nc.variables['iy'][-1])
    czs = CachingZonalStats(ncaffine)
    basedate, timesz = get_basedate(pr_nc)
    fps = []
    for i in tqdm(range(timesz)):
        date = basedate + datetime.timedelta(days=i)

        # keep array logic in top-down order
        tasmax = np.flipud(temperature(tasmax_nc.variables['tas'][i, 0, :, :],
                                       'K').value('C'))
        tasmin = np.flipud(temperature(tasmin_nc.variables['tas'][i, 0, :, :],
                                       'K').value('C'))
        pr = np.flipud(pr_nc.variables['pr'][i, :, :])
        mytasmax = czs.gen_stats(tasmax, huc12df['geo'])
        mytasmin = czs.gen_stats(tasmin, huc12df['geo'])
        mypr = czs.gen_stats(pr, huc12df['geo'])
        for j, huc12 in enumerate(hucs):
            if i == 0:
                fps.append([open('swatfiles/%s.pcp' % (huc12, ), 'wb'),
                            open('swatfiles/%s.tmp' % (huc12, ), 'wb')])
                fps[j][0].write("""HUC12 %s



""" % (huc12, ))
                fps[j][1].write("""HUC12 %s



""" % (huc12, ))

            fps[j][0].write(("%s%03i%5.1f\n"
                             ) % (date.year, float(date.strftime("%j")),
                                  mypr[j] * 86400.))
            fps[j][1].write(("%s%03i%5.1f%5.1f\n"
                             ) % (date.year, float(date.strftime("%j")),
                                  mytasmax[j], mytasmin[j]))

    for fp in fps:
        fp[0].close()
        fp[1].close()


if __name__ == '__main__':
    main(sys.argv)
