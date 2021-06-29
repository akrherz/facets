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

For HADGEM we have a 360 day calendar, see http://loca.ucsd.edu/loca-calendar/
They pick 1 random day every 72 days to do linear interpolation.
"""
import sys
import os
import datetime
import logging
from collections import namedtuple

from tqdm import tqdm
import numpy as np
from affine import Affine
import geopandas as gpd
from pyiem.grid.zs import CachingZonalStats
from pyiem.util import get_dbconn, ncopen, logger
from pyiem.datatypes import temperature
LOG = logger()
LOG.setLevel(logging.INFO)
GRIDINFO = namedtuple("GridInfo", ['x0', 'y0', 'xsz', 'ysz', 'mask'])
# 50km
#PROJSTR = ('+proj=lcc +lat_1=35 +lat_2=60 +lat_0=46 +lon_0=-97. '
#           '+a=6370000 +b=6370000 +towgs84=0,0,0 +units=m +no_defs')
# 25km
PROJSTR = ('+proj=omerc +lat_0=46.5 +alpha=90.0 +lonc=263.0 +x_0=0. '
           '+y_0=0. +ellps=sphere +a=6371229.0 +b=6371229.0 +units=m +no_defs')
# 12km
# PROJSTR = ('+proj=omerc +lat_0=37.5 +alpha=90.0 +lonc=264.0 +x_0=0. '
#          '+y_0=0. +ellps=sphere +a=6371229.0 +b=6371229.0 +units=m +no_defs')
BASEDIR = "/mnt/nrel/acaruthe/forSWAT/"



def get_dates(ncfile):
    """Compute the dates that we have"""
    nctime = ncfile.variables['time']
    basets = datetime.datetime.strptime(nctime.units,
                                        "days since %Y-%m-%d 00:00:00")
    if nctime.calendar == "gregorian":
        res = []
        for tm in nctime[:]:
            dt = (basets + datetime.timedelta(days=float(tm))).date()
            res.append(dt)
        LOG.info("Data(len=%s) stretches from %s to %s", len(res), res[0], res[-1])
        return res, False

    # We make assumptions
    assert basets.strftime("%m%d") == "1201"
    # ff to 1 Jan
    basets = (basets + datetime.timedelta(days=33)).replace(day=1)
    times = nctime[:] - 31
    dates = []
    for tm in times:
        # Compute over non leap year
        years = int(tm / 365)
        dt2 = datetime.date(2001, 1, 1) + datetime.timedelta(days=(tm % 365))
        dates.append(datetime.date(basets.year + years, dt2.month, dt2.day))
    LOG.info("Data(len=%s) stretches from %s to %s", len(dates), dates[0], dates[-1])
    return dates, True


def main(argv):
    """Go Main Go"""
    typ = argv[1]
    if typ == "hist":
        STS = datetime.date(1950, 1, 1)
        ETS = datetime.date(2006, 1, 1)
    else:
        STS = datetime.date(2006, 1, 1)
        ETS = datetime.date(2100, 1, 1)
    model = argv[2]
    bc = argv[3]
    outdir = f"swatfiles_{typ}_{model}_{bc}"
    LOG.info("running for %s", outdir)
    if os.path.isdir(outdir):
        LOG.info("returning as %s exists" % (outdir, ))
        return
    os.mkdir(outdir)
    for dirname in ['precipitation', 'temperature']:
        os.mkdir("%s/%s" % (outdir, dirname))

    pgconn = get_dbconn('idep')
    huc12df = gpd.GeoDataFrame.from_postgis("""
    SELECT huc8, simple_geom as geo from wbd_huc8
    WHERE swat_use ORDER by huc8
    """, pgconn, index_col='huc8', geom_col='geo')
    hucs = huc12df.index.values
    tasmax_nc = ncopen(f"{BASEDIR}/tmax.{typ}.{model}.day.NAM-22i.{bc}.nc")
    tasmin_nc = ncopen(f"{BASEDIR}/tmin.{typ}.{model}.day.NAM-22i.{bc}.nc")
    pr_nc = ncopen(f"{BASEDIR}/prec.{typ}.{model}.day.NAM-22i.{bc}.nc")

    # compute the affine
    ncaffine = Affine(0.25,
                      0.,
                      -171.875,
                      0.,
                      -0.25,
                      76.375)
    czs = CachingZonalStats(ncaffine)
    fps = []
    dates, add_leap_day = get_dates(tasmax_nc)
    for i, date in tqdm(enumerate(dates), total=len(dates)):
        if date < STS or date >= ETS:
            continue

        # keep array logic in top-down order
        tasmax = np.flipud(tasmax_nc.variables['tmax'][i, :, :])
        tasmin = np.flipud(tasmin_nc.variables['tmin'][i, :, :])
        pr = np.flipud(pr_nc.variables['prec'][i, :, :])
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

            fps[j][0].write("%.1f\n" % (mypr[j],))
            fps[j][1].write("%.2f,%.2f\n" % (mytasmax[j], mytasmin[j]))
            if add_leap_day and date.month == 2 and date.day == 28 and date.year % 4 == 0:
                # leap
                fps[j][0].write("%.1f\n" % (mypr[j],))
                fps[j][1].write("%.2f,%.2f\n" % (mytasmax[j], mytasmin[j]))

    for fp in fps:
        fp[0].close()
        fp[1].close()


if __name__ == '__main__':
    for a in ["hist",  "rcp85"]:
        for b in ["GFDL-ESM2M.RegCM4", "GFDL-ESM2M.WRF", "MPI-ESM-LR.RegCM4", "MPI-ESM-LR.WRF"]:
            for c in ["mbcn-gridMET", "raw"]:
                main([None, a, b, c])
