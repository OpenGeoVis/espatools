__all__ = [
    'Band',
    'RasterSet',
]

import properties
import numpy as np

from .meta import *


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
    pixel_size = properties.Instance('The pixel size', PixelSize)


    def GetRGB(self):
        if 3 > len(self.bands):
            print(self.rgb)
            raise RuntimeError('RGB bands are improperly defined.')
        color = [None, None, None]
        for name, band in self.bands.items():
            for i in range(3):
                if 'band%d' % self.rgb[i] in name:
                    color[i] = band.data
                    # TODO: check ValidRange
        for a in color:
            if isinstance(a, type(None)):
                raise RuntimeError('RGB bands unavailable.')
        # now convert to 2D array of RGB tuples
        color = np.dstack(color)
        color = np.array(color, dtype=np.float)
        color /= 2000.0 # TODO: check max valid range
        color *= (255.0/color.max())
        return np.array(color, dtype=np.uint8)


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
