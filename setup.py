import distutils
from distutils.core import setup
import glob

bin_files = glob.glob("bin/*") 

setup(name='hpixDB',
      version ='1.0.1',
      license = "NCSA",
      description = "Small routine to convert from RA,DEC to HEALPIX pixel indices to be ingested in the DB",
      author = "Matias Carrasco Kind",
      author_email = "mcarras2@illinois.edu",
      packages = ['hpixdb'],      
      package_dir = {'': 'python'},
      scripts =  ['bin/hpixDB'],
      data_files=[('ups',['ups/hpixDB.table']),
                  ],
      )
