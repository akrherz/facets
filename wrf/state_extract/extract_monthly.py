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
    nctime = str(ncfile.variables['Times'][0])
    sz = len(ncfile.variables['Times'][:])
    return datetime.datetime(
        int(nctime[:4]), int(nctime[4:6]), int(nctime[6:8]), 3), sz


def main():
    """Go Main Go."""
    ncaffine = Affine(50000.,
                      0.,
                      -3925000.,
                      0.,
                      -50000.,
                      3725000.)
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
        fps.append(open("data/%s.csv" % (abbr, ), 'w'))
    czs = CachingZonalStats(ncaffine)
    for period in ['1950_2005', '2005_2059', '2060_2099', '2100']:
        pr_nc = ncopen(
            "/mnt/nrel/acaruthe/wrf/precip_wrf_mpi_%s.nc" % (period, ))
        t2_nc = ncopen(
            "/mnt/nrel/acaruthe/wrf/t2_wrf_mpi_%s.nc" % (period, ))
        basedate, timesz = get_basedate(pr_nc)
        print("Running from %s for %s steps" % (basedate, timesz))
        for i in range(timesz):
            date = basedate + datetime.timedelta(hours=(i*3))

            t2 = np.flipud(t2_nc.variables['T2'][i, :, :])
            prc = np.flipud(pr_nc.variables['RAINC'][i, :, :])
            prnc = np.flipud(pr_nc.variables['RAINNC'][i, :, :])
            myt2 = czs.gen_stats(t2, statesdf['geo'])
            myprc = czs.gen_stats(prc, statesdf['geo'])
            myprnc = czs.gen_stats(prnc, statesdf['geo'])
            for ii, fp in enumerate(fps):
                fp.write("%s,%s,%s,%s\n" % (
                    date.strftime("%Y%m%d%H"), myt2[ii], myprc[ii],
                    myprnc[ii]))
        pr_nc.close()
        t2_nc.close()
    for fp in fps:
        fp.close()


if __name__ == '__main__':
    main()
