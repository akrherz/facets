"""Compress down our ATM and SRF files."""
import glob
import sys
import os
import subprocess

from tqdm import tqdm
from pyiem.util import ncopen


def runcmd(args):
    """Run a command and die if we fail!"""
    proc = subprocess.Popen(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    (stdout, stderr) = proc.communicate()
    if proc.returncode != 0:
        print(
            "%s failed with code: %s %s %s" % (
                args, proc.returncode, stdout, stderr)
        )
        sys.exit()


def main(argv):
    """Process the ATM and SRF files for the given model folder."""
    foldername = argv[1]
    os.chdir("/mnt/nrel/akrherz/cori/%s/output" % (foldername, ))
    ncfns = glob.glob("*ATM*nc*")
    ncfns.extend(glob.glob("*SRF*nc*"))
    ncfns.sort()
    for ncfn in tqdm(ncfns):
        if ncfn.endswith(".gz"):
            runcmd(["gunzip", ncfn])
            ncfn = ncfn[:-3]
        nc = ncopen(ncfn)
        # Figure out if we are compressed or not, by checking vars
        complevel = 0
        for varname in nc.variables:
            meta = nc.variables[varname].filters()
            if meta is None:
                continue
            complevel = meta.get('complevel', None)
            if complevel > 0:
                break
        nc.close()
        if complevel == 1:
            continue
        # We have compression work to do!
        runcmd(["nccopy", "-k", "4", "-d", "1", ncfn,  ncfn + ".tmp"])
        runcmd(["mv", ncfn + ".tmp", ncfn])


if __name__ == '__main__':
    main(sys.argv)
