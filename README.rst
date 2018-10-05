ESPA Tools
==========

.. image:: https://readthedocs.org/projects/espatools/badge/?version=latest
   :target: https://espatools.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image :: https://img.shields.io/pypi/v/espatools.svg
   :target: https://pypi.org/project/espatools/
   :alt: PyPI

.. image :: https://travis-ci.org/OpenGeoVis/espatools.svg?branch=master
   :target: https://travis-ci.org/OpenGeoVis/espatools
   :alt: Build Status

.. image:: https://img.shields.io/badge/docs%20by-gendocs-blue.svg
   :target: https://gendocs.readthedocs.io/en/latest/?badge=latest)
   :alt: Documentation Built by gendocs

.. image :: https://img.shields.io/github/stars/OpenGeoVis/espatools.svg?style=social&label=Stars
   :target: https://github.com/OpenGeoVis/espatools
   :alt: GitHub

An open-source Python package for simple loading of Landsat imagery as NumPy arrays.
This website hosts the code documentation for the ``espatools`` python package found on `GitHub`_ and `PyPI`_. This website documents the code so that users
have a convenient and familiar means of searching through the library to understand
the backend of the features they are using.


.. _GitHub: https://github.com/OpenGeoVis/espatools/
.. _PyPI: https://pypi.org/project/espatools/

Connections
-----------

- The package heavily uses `properties`_ for the creation of strongly typed objects in a consistent, declarative way.
- `PVGeo`_ has implemented an interface for ``espatools`` to read Landsat imagery via XML metadata files. Check out PVGeo's `Landsat Reader`_ for more details.

.. _properties: http://propertiespy.readthedocs.io/en/latest/
.. _PVGeo: http://pvgeo.org
.. _Landsat Reader: http://docs.pvgeo.org/en/latest/content/PVGeo/grids/fileio.html#PVGeo.grids.fileio.LandsatReader

Getting Started
---------------

``espatools`` is available from `PyPI`_

.. _PyPI: https://pypi.org/project/espatools/

.. code-block:: bash

    $ pip install espatools


Usage
^^^^^

We think `espatools` is easy to use; give it a try and let us know what you think as this is just the alpha-release! See `this Jupyter Notebook`_ for a demonstration of some simple plotting after reading Landsat imagery.

.. _this Jupyter Notebook: https://github.com/OpenGeoVis/espatools/blob/master/Example.ipynb
