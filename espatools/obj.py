import properties
import numpy as np
import collections


###############################################################################

def SetProperties(has_props_cls, input_dict, include_immutable=True):
    """A helper method to set an ``HasProperties`` object's properties from a dictionary"""
    props = has_props_cls()
    if not isinstance(input_dict, (dict, collections.OrderedDict)):
        raise RuntimeError('input_dict invalid: ', input_dict)
    for k, v in iter(input_dict.items()):
        if (k in has_props_cls._props and (
                include_immutable or
                any(hasattr(has_props_cls._props[k], att) for att in ('required', 'new_name'))
                )
           ):
            p = props._props.get(k)
            if isinstance(p, properties.HasProperties):
                props._set(k, SetProperties(p, v, include_immutable=include_immutable))
            elif isinstance(p, properties.Instance):
                props._set(k, SetProperties(p.instance_class, v, include_immutable=include_immutable))
            elif isinstance(p, properties.List):
                if not isinstance(v, list):
                    raise RuntimeError('property value mismatch', p, v)
                if not isinstance(v[0], properties.HasProperties):
                    prop = p.prop.instance_class
                    newlist = []
                    for i in v:
                        value = SetProperties(prop, i, include_immutable=include_immutable)
                        newlist.append(value)
                    props._set(k, newlist)
                else:
                    props._set(k, v)
            else:
                props._set(k, p.from_json(v))

    # Return others as well
    # others_dict = {k: v for k, v in iter(input_dict.items())
    #                if k not in has_props_cls._props}
    return props #, others_dict


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



class Band(properties.HasProperties):
    """An object to contain raster data for a single band"""

    # metadata attributes
    name = properties.String('Name of the band')
    data_type = properties.String('Band data type')
    nlines = properties.Integer('number of lines')
    nsamps = properties.Integer('number of samples')
    product = properties.String('Data product')
    # Not required
    app_version = properties.String('app version', required=False)
    production_date = properties.String('production date', required=False)
    resample_method = properties.String('resample method', required=False)
    category = properties.String('Band category', required=False)
    source = properties.String('Band source', required=False)
    qa_description = properties.String('QA description', required=False)
    # TODO: class_values
    percent_coverage = properties.Float('percent coverage', required=False)

    # metadata: All required
    short_name = properties.String('Short name')
    long_name = properties.String('Long display name')
    file_name = properties.String('Original file name')
    pixel_size = properties.Instance('The pixel size', PixelSize)

    # data information
    fill_value = properties.Integer('fill value', required=False)
    saturate_value = properties.Integer('Saturate value', required=False)
    add_offset = properties.Float('Add offset', required=False)
    data_units = properties.String('Data units', required=False)
    scale_factor = properties.Float('Scaling factor', required=False)
    valid_range = properties.Instance('The valid data range', ValidRange, required=False)
    radiance = properties.Instance('The radiance', Lum, required=False)
    reflectance = properties.Instance('The reflectance', Lum, required=False)
    thermal_const = properties.Instance('The thermal const', ThermalConst, required=False)

    bitmap_description = properties.Dictionary(
        'band bitmap description (not always present)',
        required=False,
        key_prop=properties.String('Key value'),
        value_prop=properties.String('Bitmap value description')
        )

    data = properties.Array(
        'The band data as a 2D NumPy data',
        shape=('*','*'),
        )



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



class RasterSet(properties.HasProperties):

    version = properties.String('version', required=False)

    global_metadata = properties.Instance('Raster metadata', RasterMetaData)

    # Bands
    bands = properties.Dictionary('A dictionary of bands for the swath',
                key_prop=properties.String('Band name'),
                value_prop=Band
                )
    rgb = properties.Array('The RGB band numbers',
                default=[4, 3, 2],
                shape=(3,),
                dtype=int,
                )

    nlines = properties.Integer('The number of lines')
    nsamps = properties.Integer('The number of samples')


    def GetRGB(self):
        if np.max(self.rgb) > len(self.bands):
            raise RuntimeError('RGB bands are improperly defined.')
        color = [None, None, None]
        for name, band in self.bands.items():
            for i in range(3):
                if 'band%d' % self.rgb[i] in name:
                    color[i] = band.data
        for a in color:
            if isinstance(a, type(None)):
                raise RuntimeError('RGB bands unavailable.')
        # now convert to 2D array of RGB tuples
        color = np.dstack(color)
        color /= 2000.0 # TODO: check max valid range
        color *= (255.0/color.max())
        return np.array(color, dtype=int) # TODO check type


    def validate(self):
        b = self.bands.get(list(self.bands.keys())[0])
        ny, nx = b.nlines, b.nsamps
        for name, band in self.bands.items():
            if band.nlines != ny or band.nsamps != nx:
                raise RuntimeError('Band size mismatch.')
        self.nlines = ny
        self.nsamps = nx
        return properties.HasProperties.validate(self)









###############################################################################
