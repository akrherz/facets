"""Dr Gasman sent listing of requested HUC12s

I used this csv file to set a database flag on what should be used"""
from __future__ import print_function

import pandas as pd
import psycopg2


def main():
    """Go Main Go"""
    pgconn = psycopg2.connect(dbname='idep')
    cursor = pgconn.cursor()
    df = pd.read_csv('hucs.csv')
    for _, row in df.iterrows():
        huc12 = "%012i" % (row['HUC12'], )
        cursor.execute("""
            UPDATE wbd_huc12 SET swat_use = 't' where huc12 = %s
        """, (huc12, ))
        if cursor.rowcount != 1:
            print(huc12)
    print("updated %s rows" % (len(df.index), ))
    cursor.close()
    pgconn.commit()


if __name__ == '__main__':
    main()
