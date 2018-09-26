"""Convoluted to create zg500."""
import sys
import os
import glob
import subprocess

from tqdm import tqdm


def runcmd(cmd):
    """Run a command and die if we fail!"""
    proc = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    (stdout, stderr) = proc.communicate()
    if proc.returncode != 0:
        print(
            "%s failed with code: %s %s %s" % (
                cmd, proc.returncode, stdout, stderr)
        )
        sys.exit()


def main(argv):
    """Run for a given folder name."""
    foldername = argv[1]
    os.chdir("/mnt/nrel/akrherz/cori/%s/output" % (foldername, ))
    fns = glob.glob("*ATM*")
    fns.sort()
    for fn in tqdm(fns):
        runcmd(
            "/mnt/nrel/akrherz/RegCM-4.7.0/PostProc/sigma2p %s" % (fn,)
        )
        # creates a _pressure.nc file, now we need to cull variables
        runcmd(
            ("/opt/miniconda3/envs/prod/bin/ncks -v hgt %s_pressure.nc "
             "%s_hgt.nc") % (fn[:-3], fn[:-3])
        )
        # delete pressure file
        os.unlink("%s_pressure.nc" % (fn[:-3], ))
        # collapse the plev dimension
        runcmd(
            ("/opt/miniconda3/envs/prod/bin/ncwa -A -a plev "
             "%s_hgt.nc tmp.nc"
             ) % (fn[:-3], )
        )
        # overwrite
        runcmd("mv tmp.nc %s_hgt.nc" % (fn[:-3], ))


if __name__ == '__main__':
    main(sys.argv)
