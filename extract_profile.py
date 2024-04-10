# -*- coding: utf-8 -*-
"""

File initiated by Tristan Amaral, Univ. of Idaho, Nov 16, 2018
Modifications by Tim Bartholomaus on Dec 4, 2018

Extracts an evenly spaced profile, defined along a vector polyline,
    from a netCDF or geotiff.
    
"""

#%%
def extract_profile(raster, line_file, ds, var='None'):
    """ Extracts an evenly spaced profile, defined along a vector polyline,
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
        
    """

    import numpy as np
    from osgeo import gdal
    import xarray as xr

    import geopandas as gpd
    from scipy.interpolate import interp1d
    from scipy.ndimage import map_coordinates
    
    #%% Create evenly spaced points
    # Read coordinates of the profile line from geopackage or shapefile
    gpd_file = gpd.read_file(line_file)
    coords = np.array(gpd_file.geometry[0].coords[:]) # m the easting and northing coordinates of the vertices along the shapefile

    sqrd_deltas = np.diff(coords, axis=0)**2 # squared differences between x and y coordinates
    deltas = np.sum(sqrd_deltas, axis=1)**0.5 # m  straight-line path length between adjacent points in the shapefile
    dist = np.cumsum( np.append(0, deltas) ) # m  running distance along the shapefile from one end.
    
    disti = np.arange(dist[0], dist[-1], ds) # m  vector of evenly spaced distances along the shapefile,
                                                    # equivalent to an evenly spaced version of dist
    xi = interp1d(dist, coords[:,0])(disti) # m  the easting coordinates of disti points, at which profile will be extracted
    yi = interp1d(dist, coords[:,1])(disti) # m  the northing coordinates of disti points, at which profile will be extracted

    #%% Manipulate the raster and extract its data
    if raster[-3:] == 'tif':
        # ---- dimensions of geotiff
        gtif = gdal.Open(raster)
        xmin,xres,xskew,ymax,yskew,yres = gtif.GetGeoTransform()

        # pull out the array of raster data.  Data are assumed to be in band 1.
        raster_data = gtif.GetRasterBand(1).ReadAsArray()

    elif raster[-2:] == 'nc':

        raster_xr = xr.open_dataset(raster)
        raster_data = raster_xr[var].values

        rast_x,rast_y = raster_xr['x'].values, raster_xr['y'].values
        xmin = rast_x[0]
        ymax = rast_y[0]
        xres = np.unique(np.round(np.diff(rast_x), 6))[0]
        yres = np.unique(np.round(np.diff(rast_y), 6))[0]

    # convert the profile coordinates into pixel coordinates
    px = (xi - xmin) / xres
    py = (yi - ymax) / yres
    

    # Interpolate within raster_data at given pixel coordinates to identify values from the geotiff  
    #   Uses a 1st order spline interpolant to extract estimated values of
    #   raster_data at the (non-integer) pixel values px and py.
    #   Function returns `cval' at undefined values of gtif_data.
    profile = map_coordinates(raster_data, np.vstack((py, px)),
                              order=1, cval=np.nan)
    
    #profile[np.abs(profile) == 9999] = np.nan
   
    return disti, profile, xi, yi
