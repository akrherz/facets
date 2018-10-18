"""Generate needed CSV file for HUC8 stations"""
from __future__ import print_function
import subprocess

from pandas.io.sql import read_sql
from pyiem.util import get_dbconn


def write_index(df):
    """Write some needed index files"""
    tfp = open('huc8_temperature.txt', 'w')
    tfp.write("ID,NAME,LAT,LONG,ELEVATION\n")
    pfp = open('huc8_precipitation.txt', 'w')
    pfp.write("ID,NAME,LAT,LONG,ELEVATION\n")
    i = 1
    for huc8, row in df.iterrows():
        tfp.write(("%s,T%s,%s,%s,%s\n"
                   ) % (i, huc8, row['lat'], row['lon'], row['elev']))
        pfp.write(("%s,P%s,%s,%s,%s\n"
                   ) % (i, huc8, row['lat'], row['lon'], row['elev']))
        i += 1
    tfp.close()
    pfp.close()


def main():
    """Go Main Go"""
    pgconn = get_dbconn('idep')
    df2 = read_sql("""
    select huc8, ST_x(ST_Centroid(geom)) as lon,
    ST_y(ST_Centroid(geom)) as lat from wbd_huc8 where swat_use
    """, pgconn, index_col='huc8')
    df2['elev'] = 0
    for huc8, row in df2.iterrows():
        cmd = (
            "python /home/akrherz/projects/iem/"
            "scripts/dbutil/set_elevation.py %s %s"
        ) % (row['lon'], row['lat'])
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        elev = float(proc.stdout.read().decode('utf-8').strip())
        df2.at[huc8, 'elev'] = elev
    write_index(df2)


if __name__ == '__main__':
    main()
