__all__ = [
    'SetProperties',
    'RasterSetReader',
]
import xmltodict
import numpy as np
from PIL import Image
import os
import collections
import properties

from .raster import RasterSet, Band


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

class RasterSetReader(object):
    """Read a series of raster files via their XML metadata file in ESPA schema"""

    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename', None)
        self.bdict = dict()

    @staticmethod
    def ReadTif(tifFile):
        """Reads a tif file to a 2D NumPy array"""
        img = Image.open(tifFile)
        img = np.array(img)
        return img

    @staticmethod
    def CleanDict(d):
        d = {key.replace('@', '').replace('#', ''): item for key, item in d.items()}
        for key, item in d.items():
            if isinstance(item, (collections.OrderedDict, dict)):
                d[key] = RasterSetReader.CleanDict(item)
            elif isinstance(item, list):
                for i in range(len(item)):
                    if isinstance(item[i], (collections.OrderedDict, dict)):
                        item[i] = RasterSetReader.CleanDict(item[i])
        return d


    def GenerateBand(self, band, meta_only=False):
        """Genreate a Band object given band metadata

        Args:
            band (dict): dictionary containing metadata for a given band

        Return:
            Band : the loaded Band onject"""

        # Read the band data and add it to dictionary
        if not meta_only:
            fname = band.get('file_name')
            data = self.ReadTif('%s/%s' % (os.path.dirname(self.filename), fname))
            # band['data'] = data # TODO: data is not a properties object so do not set yet

        def FixBitmap(d):
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

        band = SetProperties(Band, FixBitmap(self.CleanDict(band)))
        if not meta_only:
            data = np.ma.masked_where(data==band.fill_value, data)
            band.data = data
            # Mask the data arra using the fill_value

        if not meta_only:
            band.validate()

        return band


    def Read(self, meta_only=False, allowed=None):
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
        meta = self.CleanDict(meta)

        # Get spatial refernce
        ras = SetProperties(RasterSet, meta)

        if allowed is not None:
            # Remove non-allowed arrays from bdict
            for k in self.bdict.keys():
                if k not in allowed:
                    del(self.bdict[k])

        for i in range(len(bands)):
            info = self.GenerateBand(bands[i], meta_only=True)
            if allowed is not None and info.name not in allowed:
                continue
            if info.name not in self.bdict.keys() or self.bdict[info.name].data is None:
                b = self.GenerateBand(bands[i], meta_only=meta_only)
                self.bdict[b.name] = b
        ras.bands = self.bdict

        if not meta_only:
            ras.validate()

        return ras



    def SetFileName(self, filename):
        self.filename = filename
