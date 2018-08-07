__all__ = [
    'Lum',
    'ThermalConst',
    'PixelSize',
    'ValidRange',
    'WRS',
    'Corner',
    'CornerPoint',
    'BoundingCoordinates',
    'Projection',
    'SolarAngle',
    'RasterMetaData',
]

import properties
import numpy as np
import collections


###############################################################################


###############################################################################


class Lum(properties.HasProperties):
    gain = properties.Float('The gain')
    bias = properties.Float('The bias')


class ThermalConst(properties.HasProperties):
    k1 = properties.Float('K1')
    k2 = properties.Float('K2')


class PixelSize(properties.HasProperties):
    x = properties.Float('The X size of the pixel')
    y = properties.Float('The Y size of the pixel')
    units = properties.String('The pixel size units')


class ValidRange(properties.HasProperties):
    min = properties.Float('Minimum of valid range')
    max = properties.Float('Maximum of valid range')




###############################################################################


class WRS(properties.HasProperties):
    system = properties.Integer('The system type')
    path = properties.Integer('The WRS path')
    row = properties.Integer('The WRS row')


class Corner(properties.HasProperties):
    location = properties.String('The location')
    latitude = properties.Float('The latitude', min=-90.0, max=90.0)
    longitude = properties.Float('The longitude', min=-180.0, max=180.0)


class CornerPoint(properties.HasProperties):
    location = properties.String('The location')
    x = properties.Float('The X value')
    y = properties.Float('The Y value')


class BoundingCoordinates(properties.HasProperties):
    west = properties.Float('West line')
    east = properties.Float('East line')
    north = properties.Float('North line')
    south = properties.Float('South line')


class Projection(properties.HasProperties):
    projection = properties.String('The coordinate projection')
    datum = properties.String('The projection datum')
    units = properties.String('The projection units')
    corner_point = properties.List('The corner points', prop=CornerPoint)
    grid_origin = properties.String('The grid origin')
    utm_proj_params = properties.Dictionary('The UTM projection parameters', required=False)
    ps_proj_params = properties.Dictionary('The PS projection parameters', required=False)
    albers_proj_params = properties.Dictionary('The Albers projection parameters', required=False)
    sin_proj_params = properties.Dictionary('The Sin projection parameters', required=False)


class SolarAngle(properties.HasProperties):
    zenith = properties.Float('The zenith')
    azimuth = properties.Float('The azimuth')
    units = properties.String('The units')


class RasterMetaData(properties.HasProperties):
    """An object to contain all the information for a single swath.
    """
    #https://landsat.usgs.gov/how-do-landsat-8-band-combinations-differ-landsat-7-or-landsat-5-satellite-data

    # Metadata
    data_provider = properties.String('The data provider')
    satellite = properties.String('The satellite from which data was aquired')
    instrument = properties.String('The instrument on the satellite')
    acquisition_date = properties.String('The date of acquisition', required=False)
    scene_center_time = properties.String('Center time', required=False)
    level1_production_date = properties.String('Production date', required=False)
    solar_angles = properties.Instance('The solar angles', SolarAngle, required=False)
    earth_sun_distance = properties.Float('The earth-sun distance', required=False)
    product_id = properties.String('Data product ID', required=False)
    lpgs_metadata_file = properties.String('metadata file', required=False)
    wrs = properties.Instance('WRS', WRS, required=False)
    # TODO modis = properties.Instance('Modis', Modis, required=False)

    corner = properties.List('The corner points', prop=Corner)

    # Spatial Reference
    bounding_coordinates = properties.Instance('The bounding coordinates', BoundingCoordinates)
    projection_information = properties.Instance('The projection', Projection)
    orientation_angle = properties.Float('The orientation angle', min=-360.0, max=360.0)
