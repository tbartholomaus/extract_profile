# extract_profile
Extract a profile along a vector (i.e., shapefile), through a raster (i.e., geotiff). Uses python and packages.

Dependencies include the python packages numpy, scipy, gdal, and fiona.

Given coordinates of profile vertices within a shapefile, create a line of evenly spaced points along the vector, then sample the values of the geotiff raster at the evenly spaced points.
