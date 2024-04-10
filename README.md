# extract_profile
Extract a profile along a vector (i.e., geopackage or shapefile), through a raster (i.e., netCDF or geotiff). Uses python and packages.

Dependencies include the python packages numpy, scipy, xarray, geopandas, gdal, and fiona.

Given coordinates of profile vertices within a shapefile, create a line of evenly spaced points along the vector, then sample the values of the geotiff raster at the evenly spaced points.
This function is essentially a geospatial wrapper script of scipy.ndimage's map_coordinates function, that also creates an evenly-spaced, length vector for use in sampling the raster.

This script is useful for purposes such as pulling topographic profiles out of DEMs, or velocity profiles from remotely-sensed velocity fields.

Here's the header information from extract_profile.py, that describes the inputs and outputs:
```
    Extracts an evenly spaced profile, defined along a vector polyline,
    from a netCDF or geotiff.
    
    Inputs include:
        raster: a netCDF or geotiff file passed as a string (with path).  File is
                    expected to have units of meters.
        line_file: a vector-based (string of filename, with path) consisting
                    of only one polyline along which to extract the 
                    profile values.
        ds: the spacing of points along the polyline at which to extract
                    profile values from the geotiff, assumed to be in meters.
        var: data variable name to use for extracting the profile through
                    
    Returns include:
        disti: a vector (np.array) of evenly-space distances along
                    the shapefile.
        profile: values drawn from raster at the distances of disti.
        xi: the interpolated, evenly spaced x coordinates along the line_file,
                    at which the disti and profile values are defined.
        yi: the interpolated, evenly spaced y coordinates along the line_file,
                    at which the disti and profile values are defined.                    
        
        
```
