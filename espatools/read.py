"""This module holds the file I/O methods for rasters and bands."""

__all__ = [
    'set_properties',
    'RasterSetReader',
]

import xmltodict
import numpy as np
from PIL import Image
import os
import collections
import properties

from .raster import RasterSet, Band


def set_properties(has_props_cls, input_dict, include_immutable=True):
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
                props._set(k, set_properties(p, v, include_immutable=include_immutable))
            elif isinstance(p, properties.Instance):
                props._set(k, set_properties(p.instance_class, v, include_immutable=include_immutable))
            elif isinstance(p, properties.List):
                if not isinstance(v, list):
                    raise RuntimeError('property value mismatch', p, v)
                if not isinstance(v[0], properties.HasProperties):
                    prop = p.prop.instance_class
                    newlist = []
                    for i in v:
                        value = set_properties(prop, i, include_immutable=include_immutable)
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

class RasterSetReader(object):
    """Read a series of raster files via their XML metadata file in ESPA schema"""

    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename', None)
        self.yflip = kwargs.get('yflip', False)
        self.bdict = dict()

    @staticmethod
    def read_tif(tifFile):
        """Reads a tif file to a 2D NumPy array"""
        img = Image.open(tifFile)
        img = np.array(img)
        return img

    @staticmethod
    def clean_dict(d):
        d = {key.replace('@', '').replace('#', ''): item for key, item in d.items()}
        for key, item in d.items():
            if isinstance(item, (collections.OrderedDict, dict)):
                d[key] = RasterSetReader.clean_dict(item)
            elif isinstance(item, list):
                for i in range(len(item)):
                    if isinstance(item[i], (collections.OrderedDict, dict)):
                        item[i] = RasterSetReader.clean_dict(item[i])
        return d


    def generate_band(self, band, meta_only=False, cast=False):
        """Genreate a Band object given band metadata

        Args:
            band (dict): dictionary containing metadata for a given band

        Return:
            Band : the loaded Band onject"""

        # Read the band data and add it to dictionary
        if not meta_only:
            fname = band.get('file_name')
            data = self.read_tif('%s/%s' % (os.path.dirname(self.filename), fname))
            # band['data'] = data # TODO: data is not a properties object so do not set yet

        def fix_bitmap(d):
            p = d.get('bitmap_description')
            if p:
                lis = p.get('bit')
                bm = dict()
                # Fix bitmap_description from list of dicts to one dict
                for i in lis:
                    key = i['num']
                    value = i['text']
                    bm[key] = value
                del d['bitmap_description']
                d['bitmap_description'] = bm
            return d

        band = set_properties(Band, fix_bitmap(self.clean_dict(band)))
        if not meta_only:
            if cast:
                # cast as floats and fill bad values with nans
                data = data.astype(np.float32)
                data[data==band.fill_value] = -9999
                if band.valid_range is not None:
                    data[data<band.valid_range.min] = -9999
                    data[data>band.valid_range.max] = -9999
                data[data==-9999] = np.nan
            else:
                data = np.ma.masked_where(data==band.fill_value, data)
                if band.valid_range is not None:
                    data = np.ma.masked_where(data<band.valid_range.min, data)
                    data = np.ma.masked_where(data>band.valid_range.max, data)
            # Flip y axis if requested
            if self.yflip:
                data = np.flip(data, 0)
            band.data = data

        if not meta_only:
            band.validate()

        return band


    def read(self, meta_only=False, allowed=None, cast=False):
        """Read the ESPA XML metadata file"""
        if allowed is not None and not isinstance(allowed, (list, tuple)):
            raise RuntimeError('`allowed` must be a list of str names.')

        meta = xmltodict.parse(
                open(self.filename, 'r').read()
            ).get('espa_metadata')

        # Handle bands seperately
        bands = meta.get('bands').get('band')
        del(meta['bands'])

        if not isinstance(bands, (list)):
            bands = [bands]
        meta = self.clean_dict(meta)

        # Get spatial refernce
        ras = set_properties(RasterSet, meta)

        if allowed is not None:
            # Remove non-allowed arrays from bdict
            for k in list(self.bdict.keys()):
                if k not in allowed:
                    del(self.bdict[k])

        for i in range(len(bands)):
            info = self.generate_band(bands[i], meta_only=True, cast=cast)
            if allowed is not None and info.name not in allowed:
                continue
            if info.name not in self.bdict.keys() or self.bdict[info.name].data is None:
                b = self.generate_band(bands[i], meta_only=meta_only, cast=cast)
                self.bdict[b.name] = b
            elif cast and self.bdict[info.name].data.dtype != np.float32:
                b = self.generate_band(bands[i], meta_only=meta_only, cast=cast)
                self.bdict[b.name] = b
            elif not cast and self.bdict[info.name].data.dtype == np.float32:
                b = self.generate_band(bands[i], meta_only=meta_only, cast=cast)
                self.bdict[b.name] = b
        ras.bands = self.bdict

        if not meta_only:
            ras.validate()

        return ras


    def Read(self, *args, **kwargs):
        return self.read(*args, **kwargs)

    def set_file_name(self, filename):
        self.filename = filename

    def SetFileName(self, filename):
        return self.set_file_name(filename)
