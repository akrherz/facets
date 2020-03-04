"""Dump info for SWAT usage."""
from __future__ import print_function
import os
import datetime
from collections import namedtuple

from tqdm import tqdm
import numpy as np
from affine import Affine
import geopandas as gpd
from pyiem.grid.zs import CachingZonalStats
from pyiem.util import get_dbconn, ncopen
from metpy.units import masked_array, units

GRIDINFO = namedtuple("GridInfo", ['x0', 'y0', 'xsz', 'ysz', 'mask'])
# 50km, 25km
# PROJSTR = ('+proj=lcc +lat_1=35 +lat_2=60 +lat_0=46 +lon_0=-97. '
#           '+a=6370000 +b=6370000 +towgs84=0,0,0 +units=m +no_defs')
# 12km
PROJSTR = ('+proj=omerc +lat_0=37.5 +alpha=90.0 +lonc=264.0 +x_0=0. '
           '+y_0=0. +ellps=sphere +a=6371229.0 +b=6371229.0 +units=m '
           '+no_defs')
BASEDIR = "/tera12/acaruthe/wrf"

STS = datetime.date(1989, 1, 1)
ETS = datetime.date(2011, 1, 1)


def get_basedate(ncfile):
    """Compute the dates that we have"""
    nctime = ncfile.variables['time']
    basets = datetime.datetime.strptime(nctime.units,
                                        "days since %Y-%m-%d 00:00:00")
    ts = basets + datetime.timedelta(days=float(nctime[0]))
    return datetime.date(ts.year, ts.month, ts.day), len(nctime[:])


def main():
    """Go Main Go"""
    outdir = "swatfiles"
    if os.path.isdir(outdir):
        print("ABORT: as %s exists" % (outdir, ))
        return
    os.mkdir(outdir)
    for dirname in ['precipitation', 'temperature']:
        os.mkdir("%s/%s" % (outdir, dirname))

    pgconn = get_dbconn('idep')
    huc12df = gpd.GeoDataFrame.from_postgis("""
        SELECT huc8, ST_Transform(simple_geom, %s) as geo from wbd_huc8
        WHERE swat_use ORDER by huc8
    """, pgconn, params=(PROJSTR,), index_col='huc8', geom_col='geo')
    hucs = huc12df.index.values
    tasmax_nc = ncopen(BASEDIR + "/tasmax.eval.ERA-Int.WRF.day.FACETS-11.raw.nc")
    tasmin_nc = ncopen(BASEDIR + "/tasmin.eval.ERA-Int.WRF.day.FACETS-11.raw.nc")
    pr_nc = ncopen(BASEDIR + "/pr.eval.ERA-Int.WRF.day.FACETS-11.raw.nc")

    # compute the affine
    # NB: x, y values are wrong in the file.
    print("WARNING: we are manually hacking the affine here.")
    ncaffine = Affine(12000.,
                      0.,
                      pr_nc.variables['x'][0] - 280. * 12000.,
                      0.,
                      -12000.,
                      pr_nc.variables['y'][-1] - 192. * 12000.)
    czs = CachingZonalStats(ncaffine)
    basedate, timesz = get_basedate(pr_nc)
    fps = []
    for i in tqdm(range(timesz)):
        date = basedate + datetime.timedelta(days=i)
        if date < STS or date >= ETS:
            continue

        # keep array logic in top-down order
        tasmax = np.flipud(
            masked_array(
                tasmax_nc.variables['tasmax'][i, :, :], units.degK
                ).to(units.degC).m)
        tasmin = np.flipud(
            masked_array(
                tasmin_nc.variables['tasmin'][i, :, :], units.degK
                ).to(units.degC).m)
        pr = np.flipud(pr_nc.variables['pr'][i, :, :])
        mytasmax = czs.gen_stats(tasmax, huc12df['geo'])
        mytasmin = czs.gen_stats(tasmin, huc12df['geo'])
        mypr = czs.gen_stats(pr, huc12df['geo'])
        for j, huc12 in enumerate(hucs):
            if date == STS:
                fps.append([open(('%s/precipitation/P%s.txt'
                                  ) % (outdir, huc12), 'w'),
                            open(('%s/temperature/T%s.txt'
                                  ) % (outdir, huc12), 'w')])
                fps[j][0].write("%s\n" % (STS.strftime("%Y%m%d"), ))
                fps[j][1].write("%s\n" % (STS.strftime("%Y%m%d"), ))

            fps[j][0].write("%.1f\n" % (mypr[j] * 86400.,))
            fps[j][1].write("%.2f,%.2f\n" % (mytasmax[j], mytasmin[j]))

    for fp in fps:
        fp[0].close()
        fp[1].close()


if __name__ == '__main__':
    main()
