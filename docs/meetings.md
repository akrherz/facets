 8 Feb 2019 - Manu Alex Gasmann Jacob Gutowski
  - Gasmann will be out 5-6 weeks starting 25 Feb for medical treatment :(
  - Gasmann hopes to have a ABE appointment soon
  - NARCAAP -> CORDEX -> FACETS
  - [ ] was running regcm4 at 12.5km hydrostatic a good idea? check emails
  - [ ] What was used for numerical diffusion for these runs?
  - Jacob is noticing little difference in omega between the 12.5 and 25km runs
  - need to account for reserviours in Missouri
  - There were two hyperfacets presentations to DOE, which went OK
  - Need to look more into the national water model and how it can be used here
  - Interesting to note that Colorado River does not always make it to ocean
  - also interesting that ocean waves can impart momentum on atmosphere

31 Dec 2018 - Manu Alex Gasmann Jacob Gutowski
  - Our continuation project is currently/informally labelled Hyper-FACETs
  - There is a big Jan 3 presentation on the path forward, which prompted this
  - Need to resolve what the overarching goals are
    1) Can metrics inform uncertainty in projections?
    2) Are there mutli-sector interactions?
  - "storylines" are a new buzz word to describe change impacts in relatable
  - Continued goal of software package of metrics
  - Hyperion has targeted 4 basins and have partners in each
  - [ ] look at what the CLM-PAWS model is
  - Slide that discussed machine learning for reservior management
  - [ ] which is DOE's model, MPAS or E3SM ?
  - Timeline for continuation is mid March and then funding by early summer
  - Getting Dr Gasmann as a PhD committee member is progressing

 5 Dec 2018 - Manu Alex Gasmann Jacob
  - First meeting without Dr Arritt :(
  - Discuss the results from the Livneh runs, which look promising when using
    Hargraeves.  They noted 73% ET for the runs in MRB.
  - Their process is now calibration to get ready to run scenarios.

31 Oct 2018 - Arritt Manu Alex Gasmann
  - IEMRE was found to be way too low during 1997, still bad prior to 2003
  - CMIP5 is not necessarily based on obs for present climate runs
  - Discussion on what tunables exist within SWAT
  - There is a Nature publication on biases of Livneh dataset
  - Decision was to calibrate against Livneh

12 Oct 2018 - Arritt Manu Alex Spender Gasmann
  - Discussion on how SWAT handles sub basins
  - My TODO list for huc8 areal averaged values
    - [x] Linveh
    - [x] PRISM
    - [x] Stage IV (IEMRE)
    - [ ] Models starting with hadgem
  - [ ] is there a SWAT Linux binary?

28 Sep 2018 - Arritt Gutowski Manu Alex Spender
  - [x] there's a model status sheet floating around I should review.
  - The MPAS run with hadgem is a lower priority due to CFL issues regcm4
    and wrf had with the runs
  - discussion on best precip comparison to do between 1, 3, and 6 hourly
  - [ ] generate the mass conserving stage IV analysis

14 Sep 2018 - Arritt Gutowski Manu Alex Spender
  - [x] update NCL on arnold to the latest release

13 Sep 2018 - HAWQS workshop
  - [ ] create a cheatsheet for now my gridding algo works, so that others
    could use it, potentially
  - could do the above as an ipython notebook perhaps
  - Discussion about how the EPA picked the CMIP5 models, turns out there are
    variograms that allow for a picking strategy
  - [ ] investigate http://2w2e.com 's referenced paper
  - [ ] email details on my COOP processing to Dr Sirnivi
  - [ ] I'll produce an extracted PRISM dataset
  - Is there a CRU equivalent for Asia?
  - [ ] check how tmax and tmin are provided to SWAT min,max or max,min
  - [ ] check how the yearly replacement of data works for SWAT download COOP

31 Aug 2018 - Arritt Gutowski Spender Alex
  - Arritt and Gutowski are currently planning on attending the PIs meeting
  - Need to organize the project PIs monthly conference call again

24 Aug 2018 - Arritt Gutowski Gassman Spender Alex
  - [x] Gassman denoted an excel output issue for me from climodat stations
  - Key project point is to show we compared downscaling approaches
  - MPI regcm4 runs all done at NCAR
  - The MPAS runs took three iterations with HADGEM, same stability issues as
    we saw with regcm4
  - For MPAS, gonna focus on a 25km MPI run
  - Statistical downscaling will be available for 10 stations, maybe more
  - Need to itemize for presentations which simple metrics are completed
  - [x] email Seth about providing our 12km runs
  - Discussion on the upcoming HAWQS workshop
  - Discussion on the upcoming DOE PIs meeting
  - Will meet at 1 PM on 31 Aug next

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