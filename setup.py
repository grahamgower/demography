import setuptools

import numpy.distutils.core as core
import sys
import numpy.distutils
compiler = numpy.distutils.ccompiler.get_default_compiler()
for arg in sys.argv:
    if arg.startswith('--compiler'):
        compiler = arg.split('=')[1]

from distutils.core import setup
from distutils.extension import Extension
# from Cython.Build import cythonize
# from Cython.Distutils import build_ext
import numpy as np

__version__ = open("demography/_version.py").readlines()[-1].split()[-1].strip("\"'")

numpy.distutils.core.setup(name='demography',
                           version=__version__,
                           author='Aaron Ragsdale',
                           author_email='aaron.ragsdale@mail.mcgill.ca',
                           url='',
                           packages=['demography'],
                           license='BSD'
                           )


