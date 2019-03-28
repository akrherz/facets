"""Create CORDEX compliant files.

raw netcdf files had jx: 657 and iy: 473 online has 655 x 640 ?

"""
import sys

import netCDF4
from pyiem.util import utc

META = {
    'tas': {
        'long_name': 'Near-Surface Air Temperature',
        'standard_name': 'air_temperature',
        'units': 'K',
        'cell_methods': 'time: point m2: mean',
        'coordinates': 'lat lon height'
    }
}


class Context:
    """See how we run."""

    def __init__(self, argv):
        """Figure out our runtime context."""
        (self.varname, self.driving_model, self.scenario) = argv[1:]

    def get_filename(self):
        """Figure out what our output netCDF file should be named."""
        return ".".join([
            self.varname,
            self.scenario,
            self.driving_model,
            "RegCM4",
            "1hr",
            "NAM-11",
            "raw",
            "nc"
        ])


def init_nc(ctx):
    """Initialize the netcdf file."""
    nc = netCDF4.Dataset(ctx.get_filename(), 'w')
    nc.Conventions = "CF-1.4"
    nc.contact = "William Gutowski, gutowski@iastate.edu"
    nc.creation_date = utc().strftime("%Y-%m-%dT%H:%M:%SZ")
    nc.experiment = "TODO"
    nc.experiment_id = "TODO"
    nc.driving_experiment = "TODO"
    nc.driving_model_id = ctx.driving_model
    nc.driving_model_ensemble_member = "TODO"
    nc.driving_experiment_name = "TODO"
    nc.frequency = "1hr"
    nc.institution = "Iowa State University"
    nc.institute_id = "ISU"
    nc.model_id = "NCAR-RegCM4"
    nc.rcm_version_id = "v4.4-rc8"
    nc.project_id = "CORDEX"
    nc.CORDEX_domain = "NAM-11"
    nc.references = " "
    nc.product = "output"
    nc.tracking_id = "TODO"

    return nc


def main(argv):
    """Go Main Go."""
    ctx = Context(argv)
    # Init output file
    nc = init_nc(ctx)
    # file available netcdfs
    # fill out the grid with the data
    # close


if __name__ == '__main__':
    main(sys.argv)
