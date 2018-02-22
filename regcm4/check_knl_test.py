"""Check knl_test output from cori

Dr Arritt made a run on the KNL nodes to see if the results are comparable
"""
from __future__ import print_function
import datetime

import matplotlib.pyplot as plt
import pandas as pd
import netCDF4
import numpy as np


def plot():
    """Make a plot of our fancy data"""
    df = pd.read_csv("/tmp/pr.txt", sep=r'\s+',
            names=['step', 'haswell', 'knl', 'diff', 'rmse'])
    xticks = []
    xticklabels = []
    ts = datetime.datetime(1989, 1, 1)
    for i in range(len(df.index)):
        if ts.hour == 0 and ts.day == 1:
            xticks.append(i)
            xticklabels.append(ts.strftime("%-d %b"))

        ts += datetime.timedelta(hours=1)

    (fig, ax) = plt.subplots(1, 1)
    # TODO tas was backwards
    ax.set_title("pr regcm4 cori difference KNL minus Haswell")
    ax.plot(np.arange(len(df.index)), df['diff'].values, label='Bias')
    ax.plot(np.arange(len(df.index)), df['rmse'].values, label='RMSE')
    ax.set_ylabel("1 Hour Precipitation [mm]")
    ax.legend()
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels)
    ax.grid(True)
    fig.savefig('test.png')


def dump_stats():
    """dump stats"""
    step = 0
    for month in range(1, 6):
        kfn = ("/mnt/nrel/akrherz/cori/knl_test/output/"
               "regcm4_erai_12km_SRF.19890%s0100.nc") % (month,)
        pfn = ("/mnt/nrel/akrherz/cori/regcm4_erai_12km/output/"
               "regcm4_erai_12km_SRF.19890%s0100.nc") % (month,)
        knc = netCDF4.Dataset(kfn)
        pnc = netCDF4.Dataset(pfn)
        for i in range(knc.variables['pr'].shape[0]):
            kvals = knc.variables['pr'][i, :, :] * 3600.
            pvals = pnc.variables['pr'][i, :, :] * 3600.
            print(("%4i %9.5f %9.5f %9.5f %9.5f"
                   ) % (step, np.mean(pvals), np.mean(kvals),
                        np.mean(kvals) - np.mean(pvals),
                        np.mean(((kvals - pvals)**2)**0.5)))
            step += 1
        knc.close()
        pnc.close()


if __name__ == '__main__':
    # dump_stats()
    plot()
