 3 Aug 2018 - Arritt Gutowski Gassman Spender Alex
  - Reminder that the regcm4 runs for 25 and 50 km went 1950 thru 2099
  - Discussion of logistics for Sirvini visit the second week of Sept
  - [x] start more systematic look at precipitation from LOCA SWAT files

20 Jul 2018 - Arritt Gutowski Gassman Spender Alex(remote)
  - Gonna look at Stage IV 2002-2012 DJF (6hourly)
  - Use NARR for an analysis of circulation
  - Note that the regcm4 spacing is not exactly 50,25,12, but 0.44, 0.22, 0.11
  - MPI run being made on Cheyenne at NCAR, done by end of Sept
  - What are the basic and more advanced evaluation metrics for SWAT
  - HAWQS workshop here on 12-13 Sept, atttempt to meet with Dr Sirvini
  - Dr Arritt has access to the precipitation data from WRF
  - [ ] Paul Deermeyer(sp) has some one-pager showing 25 metrics for LSM
  - AGU abstracts are due 1 August
  - meet in two weeks, 1 PM Aug 3

14 May 2018 - Arritt Gassman Adrianna Alex
  - For the June meeting, we want to show the results of the dynamic downscale
  - [x] Dr Arritt needs me to generate the 0z-0z precip files for erainterim
  - [x] email Dr Arritt about needing more hadgem rcp85 data on cori
  - [x] LOCA dump needs to be between 1989 thru 2010, not 1979 thru 2000
    priorioty: hadgem2-es, gfdl-esm2m, mpi_lr
  - the RCP pathway is more in terms of radiative forcing than CO2
  - [x] For the dynamically downscaled, just dump tmax, tmin, and pr not all
    the other vars, instead of splitting at 2005, just use 1984 thru 2005
    UPDATED: now 1989 thru 2010
  - Todd will likely run these, not Yiannis
  - [x] Dr Arritt wants me to dump the 25km run, not 12km, hmmm
  - [ ] maybe I should send a dump of PRISM data
  - [ ] Do European precip sensors also have 0.01 tipping mechanisms?
  - [ ] shifts in extreme 25mm/day precip
  - [ ] review swat guide for how the climate generator works.

 2 Apr 2018 - Arritt Gassman Sirini
  - SWAT has some online tooling/data available for LOCA downscaled already,
    but this data is only for HUC10 and HUC8, they did not want to go down to
    HUC12
  - [x] various improvements for what was previously generated for SWAT files
    including prefix files with P and T, two seperate folders and generate the
    index file
  - Sirini is going to give a HAWQS talk on 23 April at 11 AM

 6 Mar 2018 - ISU Team Update
  Glisan, Gutowski, Arritt, Karuthe, Spender
  - ERAI is done, so I should prioritize it
  - [ ] I volunteered to look more into MERRA precip

13 Feb 2018 - ISU Team Update
  Glisan, Gutowski, Arritt, Karuthe, Spender, Gasman
  - Perhaps some of Alex and/or Jacob work can be merged into a senior thesis
  - Jacob is working on extreme winter precipitation stuff
  - Justin and Seth are working on metrics
  - [ ] I should be thresholding precip to 0.01 inches to make zeros
  - hadgem_base run got going again on cori
  - could an analysis of frontogenesis be made?
  - and so to clarify what runs Dr Arritt has in mind

Scenario | ERAI | HADGEM | GFDL | MPI
---- | --- | --- | --- | ---
Present | x | x | x | x
Future | n/a | x | x | x