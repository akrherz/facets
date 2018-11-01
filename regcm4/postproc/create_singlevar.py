"""
for year in range(1989, 2013):
  cmd = "/opt/miniconda3/envs/prod/bin/ncrcat
  -4 -v hgt regcm4_erai_12km_ATM.%s*_hgt.nc
  ../singlevar/regcm4_erai_12km_zg500.%s.nc" % (year, year)
  os.system(cmd)
"""
import glob
import os
import sys
import subprocess

from tqdm import tqdm
CONVVARS = ['uas', 'vas', 'qas', 'tas', 'pr', 'rsds', 'rsns']
XREF = {
    'regcm4_hadgem_rcp85': 'regcm4_hadgem_12km'
}


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


def compute_years():
    """Figure out which years we have data for."""
    fns = glob.glob("*STS*00.nc")
    fns.sort()
    syear = int(fns[0].split(".")[1][:4])
    eyear = int(fns[-1].split(".")[1][:4])
    return list(range(syear, eyear + 1))


def main(argv):
    """Run for a given model directory."""
    foldername = argv[1]
    os.chdir("/mnt/nrel/akrherz/cori/%s/output" % (foldername, ))
    years = compute_years()
    for year in tqdm(years):
        for varname in CONVVARS:
            outfn = "../singlevar/%s_%s.%s.nc" % (foldername, varname, year)
            if os.path.isfile(outfn):
                continue
            runcmd(
                ("/opt/miniconda3/envs/prod/bin/ncrcat -4 -v %s %s_SRF.%s*.nc "
                 "%s") % (varname, XREF.get(foldername, foldername), year,
                          outfn)
            )
        # Combine uas vas
        runcmd(
            ("/opt/miniconda3/envs/prod/bin/ncks -A "
             "../singlevar/%s_uas.%s.nc ../singlevar/%s_vas.%s.nc"
             ) % (foldername, year, foldername, year)
        )
        os.rename(
            "../singlevar/%s_vas.%s.nc" % (foldername, year),
            "../singlevar/%s_uas_vas.%s.nc" % (foldername, year)
        )
        os.unlink("../singlevar/%s_uas.%s.nc" % (foldername, year))
        # generate the sped file
        runcmd(
            ("/opt/miniconda3/envs/prod/bin/ncap2 -6 -O -s "
             "'sped=sqrt(pow(uas,2)+pow(vas,2))' "
             "../singlevar/%s_uas_vas.%s.nc "
             "../singlevar/%s_sped.%s.nc"
             ) % (foldername, year, foldername, year)
        )


if __name__ == '__main__':
    main(sys.argv)
