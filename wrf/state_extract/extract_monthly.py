"""Extract monthly data from WRF runs."""
import datetime

import numpy as np
import geopandas as gpd
from affine import Affine
from pyiem.grid.zs import CachingZonalStats
from pyiem.util import ncopen, get_dbconn

# 50km WRF, see top level README.md for validation
PROJSTR = (
    '+proj=lcc +lat_1=35 +lat_2=60 +lat_0=46 +lon_0=-97. +a=6370000 '
    '+b=6370000 +towgs84=0,0,0 +units=m +no_def'
)


def get_basedate(ncfile):
    """Compute the dates that we have"""
    return datetime.datetime(1949, 12, 1), ncfile.variables['time'][:]


def main():
    """Go Main Go."""
    ncaffine = Affine(50000.,
                      0.,
                      -3675000.,
                      0.,
                      -50000.,
                      3475000.)
    pgconn = get_dbconn('postgis')
    statesdf = gpd.GeoDataFrame.from_postgis("""
        (SELECT preabbr as abbr, ST_Transform(geom, %s) as geo
         from canada_provinces)
        UNION ALL
        (SELECT state_abbr as abbr, ST_Transform(the_geom, %s) as geo
         from states)
    """, pgconn, params=(PROJSTR, PROJSTR), index_col='abbr', geom_col='geo')
    abbrs = statesdf.index.values
    fps = []
    for abbr in abbrs:
        fp = open("data/%s.csv" % (abbr.replace(".", ""), ), 'w')
        fp.write("year,month,averagetemp_c,precip_mm\n")
        fps.append(fp)
    czs = CachingZonalStats(ncaffine)
    for period in ['hist', 'rcp85']:
        pr_nc = ncopen(
            "pr.%s.MPI-ESM-LR.WRF.mon.NAM-44.raw.nc" % (period, ))
        t2_nc = ncopen(
            "tas.%s.MPI-ESM-LR.WRF.mon.NAM-44.raw.nc" % (period, ))
        basedate, times = get_basedate(pr_nc)
        print("Running from %s for %s steps" % (basedate, len(times)))
        for i, time in enumerate(times):
            date = basedate + datetime.timedelta(days=time)

            tas = np.flipud(t2_nc.variables['tas'][i, :, :]) - 273.15
            # 3hr avg, this is a HACK
            pr = np.flipud(pr_nc.variables['pr'][i, :, :]) * 10800. * 8 * 30.5
            myt2 = czs.gen_stats(tas, statesdf['geo'])
            myprc = czs.gen_stats(pr, statesdf['geo'])
            for ii, fp in enumerate(fps):
                fp.write("%s,%s,%s\n" % (
                    date.strftime("%Y,%m"), myt2[ii], myprc[ii]))
        pr_nc.close()
        t2_nc.close()
    for fp in fps:
        fp.close()


if __name__ == '__main__':
    main()
