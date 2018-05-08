"""Do the necessary logic to get 6z to 6z values

windspeed -> calculate hourly wind magnitude from uas,vas and average
rh -> calculate hourly RH from tas,qas and average
tasmax -> max of hourly tas

ncra -O --mro -d time,6,,24,24 -v tas -y max regcm4_erai_12km_tas.????.nc /tmp/tasmax.nc

tasmin -> min of hourly tas
pcpn -> sum hourly pr
srad -> sum hourly rsds

"""
import sys

def main(argv):
    """Go Main Go"""


if __name__ == '__main__':
    main(sys.argv)
