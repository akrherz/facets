Spender's data request
----------------------

fields from the 12km, 25km, and 50km runs

1. 6 hourly precipitation.
  
  /opt/miniconda3/envs/prod/bin/ncra -O --mro -d time,,,6,6 -v pr -y avg     singlevar/regcm4_erai_12km_pr.????.nc 6hourly/regcm4_erai_12km_pr.nc
2. 2m temperature
  ncrcat -v tas -d time,,,6 regcm4_erai_12km_tas.????.nc ../6hourly/regcm4_erai_12km_tas.nc
3. 10 m winds.
4. 2m specific humidity
5. 500 hpa heights.

