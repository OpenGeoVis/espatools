"""espatools: an open-source python package for Landsat raster file I/O
"""

import setuptools

__version__ = '0.0.4'

with open("README.rst", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="espatools",
    version=__version__,
    author="Bane Sullivan",
    author_email="info@pvgeo.org",
    description="Landsat raster file I/O",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/OpenGeoVis/espatools",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy>=1.10',
        'scipy>=1.1',
        'pillow>=5.2.0',
        'xmltodict>=0.11.0',
        'vectormath>=0.2.0',
        'properties>=0.5.2',
    ],
    classifiers=(
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Scientific/Engineering :: GIS',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
    ),
)
