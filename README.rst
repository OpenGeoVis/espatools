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
- This package implements a way to convert these datasets to a `PyVista`_ dataset (``vtkImageData``).
- `PVGeo`_ has implemented an interface for ``espatools`` to read Landsat imagery via XML metadata files. Check out PVGeo's `Landsat Reader`_ for more details.

.. _properties: http://propertiespy.readthedocs.io/en/latest/
.. _PyVista: http://docs.pyvista.org
.. _PVGeo: http://pvgeo.org
.. _Landsat Reader: https://pvgeo.org/content/PVGeo/grids/fileio.html#landsat-xml-reader

Getting Started
---------------

``espatools`` is available from `PyPI`_

.. _PyPI: https://pypi.org/project/espatools/

.. code-block:: bash

    $ pip install espatools


Usage
^^^^^

We think `espatools` is easy to use; give it a try and let us know what you think as this is just the alpha-release!

1. First, checkout `this Jupyter Notebook`_ for a demonstration of some simple plotting after reading Landsat imagery in a Python environment.

.. _this Jupyter Notebook: https://github.com/OpenGeoVis/espatools/blob/master/Example.ipynb

2. And take a look at the ``.to_pyvista()`` method on ``RasterSet`` objects to have a 3D dataset of the imagery in PyVista/VTK

3. Then take a look at the `Landsat Reader`_ in `PVGeo`_'s documentation where ``espatools`` has an interface for direct use in ParaView.


Example False Color
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    import espatools
    import matplotlib.pyplot as plt

    # Create the reader to manage I/O
    reader = espatools.RasterSetReader(filename='metadata.xml')

    # Perform the read and yield a raster set
    raster = reader.read()

    # Get an RGB color scheme
    color = raster.get_rgb('false_a')

    # Now plot the false color image
    plt.imshow(color)


The results of the above code yield the following false color image:


.. image:: https://github.com/OpenGeoVis/espatools/raw/master/RGB.png
   :alt: RGB False Color


You can also view the dataset in 3D using `PyVista`_:

.. code-block:: python

    mesh = raster.to_pyvista()
    mesh.plot(scalars='false_a', rgb=True, cpos='xy')
