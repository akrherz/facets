# facets
My work on the FACETs project

Sharing output data
-------------------

I have a copy of the CORDEX variable requirements on our website:
https://na-cordex.org/sites/default/files/na-cordex/CORDEX_variables_requirement_table.pdf

We're collecting a subset of those variables for the NA-CORDEX archive:
https://na-cordex.org/variable-list

In general, we're adhering to the CORDEX specs for the FACETS run, so
the requirements for the grids would come from there:
https://na-cordex.org/sites/default/files/na-cordex/cordex_archive_specifications.pdf



25km grid navigation
--------------------

```
:projection = "ROTMER" ;
:grid_size_in_meters = 25000. ;
:latitude_of_projection_origin = 46.5 ;
:longitude_of_projection_origin = 263. ;
:grid_north_pole_latitude = 46.5 ;
:grid_north_pole_longitude = 263. ;
:grid_factor = 0. ;

lat,lon lower left corner 3.09 -131.19
lat,lon upper right corner 55.859 -8.09

jx -4750000.0 to 4750000
iy -4050000 to 4050000

$ invproj -f "%f" +proj=omerc +lat_0=46.5 +alpha=90.0 +lonc=263.0 +x_0=0. +y_0=0. +ellps=sphere +a=6371229.0 +b=6371229.0 +units=m +no_defs
-4750000 -4050000
-131.190746	3.096919
4750000 4050000
-8.094820	55.858988
```

12km grid navigation
--------------------

```
:projection = "ROTMER" ;
:grid_size_in_meters = 12000. ;
:latitude_of_projection_origin = 37.5 ;
:longitude_of_projection_origin = 264. ;
:grid_north_pole_latitude = 37.5 ;
:grid_north_pole_longitude = 264. ;
:grid_factor = 0. ;


jx[0] =  -3936000
iy[0] =  -2832000

ix[-1] = 3936000
iy[-1] = 2832000

xlat[0,0] = 6.8826475
xlon[0,0] = -128.01791

xlat[-1,-1] = 51.450836
xlon[-1,-1] = -38.367317

invproj -f "%f" +proj=omerc +lat_0=37.5 +alpha=90.0 +lonc=264.0 +x_0=0. +y_0=0. +ellps=sphere +a=6371229.0 +b=6371229.0 +units=m +no_defs
-3936000 -2832000
-128.017913 6.882647
3936000 2832000
-38.367318  51.450835
```

50km grid WRF
-------------

```
		:CEN_LAT = 46.f ;
		:CEN_LON = -97.f ;
		:TRUELAT1 = 35.f ;
		:TRUELAT2 = 60.f ;
		:MOAD_CEN_LAT = 46.f ;
		:STAND_LON = -97.f ;
		:POLE_LAT = 90.f ;

xsz = 158 ysz = 150
XLAT,XLONG lowerleft = -127.087 7.71317
XLAT,XLONG upperright = -13.62 58.4

invproj -f "%f" +proj=lcc +lat_1=35 +lat_2=60 +lat_0=46 +lon_0=-97. +a=6370000 +b=6370000 +towgs84=0,0,0 +units=m +no_defs
-3925000. -3725000.
-127.087241	7.713160
3925000. 3725000.   
-13.629138	58.541067

```