ESPA Tools
==========

.. image:: https://readthedocs.org/projects/espatools/badge/?version=latest
   :target: https://espatools.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/espatools.svg
   :target: https://pypi.org/project/espatools/
   :alt: PyPI

.. image:: https://travis-ci.org/OpenGeoVis/espatools.svg?branch=master
   :target: https://travis-ci.org/OpenGeoVis/espatools
   :alt: Build Status

.. image:: https://img.shields.io/badge/docs%20by-gendocs-blue.svg
   :target: https://gendocs.readthedocs.io/en/latest/?badge=latest)
   :alt: Documentation Built by gendocs

.. image:: https://img.shields.io/github/stars/OpenGeoVis/espatools.svg?style=social&label=Stars
   :target: https://github.com/OpenGeoVis/espatools
   :alt: GitHub

An open-source Python package for simple loading of Landsat imagery as NumPy arrays.
When downloading Landsat imagery from `USGS Earth Explorer`_, the datasets contain
many bands (``.tif`` files) and a few metadata files (``.txt`` and ``.xml`` files).
``espatools`` is built to parse the ``.xml`` metadata file to read all of the bands
for that dataset and provide a convenient and intuitive means of accessing that
metadata along side the raw data in a Python environment.
``espatools`` can be found on `GitHub`_ and `PyPI`_.


.. image:: https://github.com/OpenGeoVis/espatools/raw/master/collage.png
   :alt: Collage of RGB colors


.. _USGS Earth Explorer: https://earthexplorer.usgs.gov
.. _GitHub: https://github.com/OpenGeoVis/espatools/
.. _PyPI: https://pypi.org/project/espatools/

Connections
-----------

- The package heavily uses `properties`_ for the creation of strongly typed objects in a consistent, declarative way.
- `PVGeo`_ has implemented an interface for ``espatools`` to read Landsat imagery via XML metadata files. Check out PVGeo's `Landsat Reader`_ for more details.

.. _properties: http://propertiespy.readthedocs.io/en/latest/
.. _PVGeo: http://pvgeo.org
.. _Landsat Reader: http://pvgeo.org/examples/grids/raster/

Getting Started
---------------

``espatools`` is available from `PyPI`_

.. _PyPI: https://pypi.org/project/espatools/

.. code-block:: bash

    $ pip install espatools


Usage
^^^^^

We think `espatools` is easy to use; give it a try and let us know what you think as this is just the alpha-release!

1. First, take a look at `this example`_ for `PVGeo`_ where ``espatools`` has an interface for direct use in ParaView.

.. _this example: http://pvgeo.org/examples/grids/raster/

2. Then checkout `this Jupyter Notebook`_ for a demonstration of some simple plotting after reading Landsat imagery in a Python environment.

.. _this Jupyter Notebook: https://github.com/OpenGeoVis/espatools/blob/master/Example.ipynb


Example False Color
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    import espatools
    import matplotlib.pyplot as plt

    # Create the reader to manage I/O
    reader = espatools.RasterSetReader(filename='metadata.xml')

    # Perform the read and yield a raster set
    raster = reader.Read()

    # Get an RGB color scheme
    color = raster.GetRGB('false_a')

    # Now plot the false color image
    plt.imshow(color)


The results of the above code yield the following false color image:


.. image:: https://github.com/OpenGeoVis/espatools/raw/master/RGB.png
   :alt: RGB False Color
