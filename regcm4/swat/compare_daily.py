"""We manually processed one HUC12 of data (near Ames)"""

import pandas as pd
from pandas.io.sql import read_sql
from pyiem.util import get_dbconn
from pyiem.datatypes import distance, temperature


def main():
    """Go Main Go"""
    pgconn = get_dbconn('coop')
    fdf = read_sql("""
    SELECT year, sum(precip) as ob,
    avg(high) as high, avg(low) as low
    from alldata_ia where station = 'IA0200'
    and year > 1988 and year < 2002
    GROUP by year ORDER by year
    """, pgconn, index_col='year')
    df = pd.read_csv('/tmp/ames.txt', sep=r'\s+',
                     names=['date', 'huc12', 'tasmax', 'tasmin', 'pr'])
    df['date'] = pd.to_datetime(df['date'])
    df['pr'] = distance(df['pr'].values, 'MM').value('IN')
    df['tasmax'] = temperature(df['tasmax'].values, 'K').value('F')
    df['tasmin'] = temperature(df['tasmin'].values, 'K').value('F')
    gdf = df.groupby(df['date'].dt.year).sum().copy()
    agdf = df.groupby(df['date'].dt.year).mean().copy()
    fdf['erai_pr'] = gdf['pr']
    fdf['erai_tasmax'] = agdf['tasmax']
    fdf['erai_tasmin'] = agdf['tasmin']
    fdf['diff_pr'] = fdf['erai_pr'] - fdf['ob']
    fdf['diff_high'] = fdf['erai_tasmax'] - fdf['high']
    fdf['diff_low'] = fdf['erai_tasmin'] - fdf['low']
    fdf.to_csv('/tmp/yearly.csv')


if __name__ == '__main__':
    main()
