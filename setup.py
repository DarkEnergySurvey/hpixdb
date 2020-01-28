"""
Setup for hpixDB package
"""
from distutils.core import setup
setup(name='hpixDB',
      version='3.0.0',
      license="NCSA",
      description="Small routine to convert from RA,DEC to HEALPIX pixel indices to be ingested in the DB",
      author="Matias Carrasco Kind",
      author_email="mcarras2@illinois.edu",
      packages=['hpixdb'],
      package_dir={'': 'python'},
      scripts=['bin/hpixDB'],
      data_files=[('ups', ['ups/hpixDB.table'])])
