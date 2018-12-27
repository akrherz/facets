"""Dr Gasman sent listing of requested HUC12s

I used this csv file to set a database flag on what should be used"""
from __future__ import print_function
import subprocess

import pandas as pd
from pandas.io.sql import read_sql
import psycopg2


def generate_index():
    """Go Main Go"""
    pgconn = psycopg2.connect(dbname='idep', host='iemdb')
    df = read_sql("""
    select huc8, name, st_x(st_centroid(geom)) as lon,
    st_y(st_centroid(geom)) as lat from wbd_huc8 where swat_use
    """, pgconn, index_col='huc8')
    tfp = open('huc8_temperature.txt', 'w')
    tfp.write("ID,NAME,LAT,LONG,ELEVATION\n")
    pfp = open('huc8_precipitation.txt', 'w')
    pfp.write("ID,NAME,LAT,LONG,ELEVATION\n")
    i = 1
    for huc8, row in df.iterrows():
        cmd = (
            "python /home/akrherz/projects/iem/"
            "scripts/dbutil/set_elevation.py %s %s"
        ) % (row['lon'], row['lat'])
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        elev, _ = proc.communicate()
        elev = float(elev.strip())
        tfp.write(("%s,T%08i,%s,%s,%s\n"
                   ) % (i, int(huc8), row['lat'], row['lon'], elev))
        pfp.write(("%s,P%08i,%s,%s,%s\n"
                   ) % (i, int(huc8), row['lat'], row['lon'], elev))
        i += 1
    pgconn.commit()


def write_index():
    """Write some needed index files"""
    df = pd.read_excel('/tmp/UMRB_OTRB_HUC12.xlsx', sheet_name='All')
    tfp = open('huc12_temperature.txt', 'w')
    tfp.write("ID,NAME,LAT,LONG,ELEVATION\n")
    pfp = open('huc12_precipitation.txt', 'w')
    pfp.write("ID,NAME,LAT,LONG,ELEVATION\n")
    i = 1
    for _, row in df.iterrows():
        huc12 = "%012i" % (row['HUC12'], )
        tfp.write(("%s,T%s,%s,%s,%s\n"
                   ) % (i, huc12, row['Lat'], row['Long_'], row['Elev']))
        pfp.write(("%s,P%s,%s,%s,%s\n"
                   ) % (i, huc12, row['Lat'], row['Long_'], row['Elev']))
        i += 1
    tfp.close()
    pfp.close()


def main():
    """Go Main Go"""
    pgconn = psycopg2.connect(dbname='idep', host='iemdb', user='mesonet')
    cursor = pgconn.cursor()
    df = pd.read_excel('/tmp/HUC8 codes for MRB.xlsx', sheet_name='MRB')
    df2 = read_sql("""
    select huc8, 'F' as flag from wbd_huc8 where swat_use
    """, pgconn, index_col='huc8')
    memory = []
    for _, row in df.iterrows():
        huc12 = "%08i" % (row['HUC8'], )
        if huc12 in memory:
            print("DUPLICATED in spreadsheet: %s" % (huc12, ))
        memory.append(huc12)
        if huc12 not in df2.index:
            print("NEW %s" % (huc12, ))
        cursor.execute("""
            UPDATE wbd_huc8 SET swat_use = 't' where huc8 = %s
        """, (huc12, ))
        if cursor.rowcount != 1:
            print(huc12)
    print("updated %s rows" % (len(df.index), ))
    cursor.close()
    pgconn.commit()


if __name__ == '__main__':
    # main()
    # write_index()
    generate_index()
