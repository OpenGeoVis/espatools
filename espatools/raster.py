__all__ = [
    'Band',
    'ColorSchemes',
    'RasterSet',
]

import properties
import numpy as np

from .meta import *


class Band(properties.HasProperties):
    """Contains raster metadata and data for a single band."""

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
    fill_value = properties.Integer('fill value', default=-9999)
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

    # TODO: data validation causes a MAJOR slowdown. WAAAAYYY faster to not set
    #       the data as a `properties` attribute.
    # data = properties.Array(
    #     'The band data as a 2D NumPy data',
    #     shape=('*','*'),
    #     )
    data = None


class ColorSchemes(object):
    """A class to hold various RGB color schemes fo refernce. These color
    schemes are defined on the `USGS website`_.

    .. _USGS website: https://landsat.usgs.gov/how-do-landsat-8-band-combinations-differ-landsat-7-or-landsat-5-satellite-data
    """

    LOOKUP_TRUE_COLOR = dict(
        LANDSAT_8=['sr_band4', 'sr_band3', 'sr_band2'],
        LANDSAT_7=['sr_band3', 'sr_band2', 'sr_band1'],
        LANDSAT_5=['sr_band3', 'sr_band2', 'sr_band1'],
    )

    LOOKUP_INFRARED = dict(
        LANDSAT_8=['sr_band5', 'sr_band4', 'sr_band3'],
        LANDSAT_7=['sr_band4', 'sr_band3', 'sr_band2'],
        LANDSAT_5=['sr_band4', 'sr_band3', 'sr_band2'],
    )

    LOOKUP_FLASE_COLOR_A = dict(
        LANDSAT_8=['sr_band6', 'sr_band5', 'sr_band4'],
        LANDSAT_7=['sr_band5', 'sr_band4', 'sr_band3'],
        LANDSAT_5=['sr_band5', 'sr_band4', 'sr_band3'],
    )

    LOOKUP_FLASE_COLOR_B = dict(
        LANDSAT_8=['sr_band7', 'sr_band6', 'sr_band4'],
        LANDSAT_7=['sr_band7', 'sr_band5', 'sr_band3'],
        LANDSAT_5=['sr_band7', 'sr_band5', 'sr_band3'],
    )

    LOOKUP_FLASE_COLOR_C = dict(
        LANDSAT_8=['sr_band7', 'sr_band5', 'sr_band3'],
        LANDSAT_7=['sr_band7', 'sr_band4', 'sr_band2'],
        LANDSAT_5=['sr_band7', 'sr_band4', 'sr_band2'],
    )


class RasterSet(properties.HasProperties):

    version = properties.String('version', required=False)

    global_metadata = properties.Instance('Raster metadata', RasterMetaData)

    # Bands
    bands = properties.Dictionary('A dictionary of bands for the swath',
                key_prop=properties.String('Band name'),
                value_prop=Band
                )

    nlines = properties.Integer('The number of lines')
    nsamps = properties.Integer('The number of samples')
    pixel_size = properties.Instance('The pixel size', PixelSize)

    RGB_SCHEMES = dict(
        true=ColorSchemes.LOOKUP_TRUE_COLOR,
        infrared=ColorSchemes.LOOKUP_INFRARED,
        false_a=ColorSchemes.LOOKUP_FLASE_COLOR_A,
        false_b=ColorSchemes.LOOKUP_FLASE_COLOR_B,
        false_c=ColorSchemes.LOOKUP_FLASE_COLOR_C,
    )


    def GetRGB(self, scheme='infrared', names=None):
        """Get an RGB color scheme based on predefined presets or specify your
        own band names to use. A given set of names always overrides a scheme."""
        if names is not None:
            if not isinstance(names, (list, tuple)) or len(names) != 3:
                raise RuntimeError('RGB band names improperly defined.')
        else:
            lookup = self.RGB_SCHEMES[scheme]
            names = lookup[self.global_metadata.satellite]

        # Now check that all bands are available:
        for nm in names:
            if nm not in self.bands.keys():
                raise RuntimeError('Band (%s) unavailable.' % nm)

        # Get the RGB bands
        r = self.bands[names[0]].data
        g = self.bands[names[1]].data
        b = self.bands[names[2]].data
        # Note that the bands dhould already be masked from read.
        # If casted then there are np.nans present
        r = ((r - np.nanmin(r)) * (1/(np.nanmax(r) - np.nanmin(r)) * 255)).astype('uint8')
        g = ((g - np.nanmin(g)) * (1/(np.nanmax(g) - np.nanmin(g)) * 255)).astype('uint8')
        b = ((b - np.nanmin(b)) * (1/(np.nanmax(b) - np.nanmin(b)) * 255)).astype('uint8')
        return np.dstack([r, g, b])


    def validate(self):
        b = self.bands.get(list(self.bands.keys())[0])
        ny, nx = b.nlines, b.nsamps
        dx, dy = b.pixel_size.x, b.pixel_size.y
        for name, band in self.bands.items():
            if band.nlines != ny or band.nsamps != nx:
                raise RuntimeError('Band size mismatch.')
            if band.pixel_size.x != dx or band.pixel_size.y != dy:
                raise RuntimeError('Pixel size mismatch.')
        self.nlines = ny
        self.nsamps = nx
        self.pixel_size = b.pixel_size
        return properties.HasProperties.validate(self)
