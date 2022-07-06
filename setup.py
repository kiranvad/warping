import setuptools
import numpy
import sys, os
import platform
from distutils.core import setup
from distutils.core import Command
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
from setuptools import dist
from distutils.sysconfig import get_config_var, get_python_inc
from distutils.version import LooseVersion

sys.path.insert(1, 'src/')
import dp_build

# Make sure I have the right Python version.
if sys.version_info[:2] < (3, 6):
    print(("fdasrsf requires Python 3.6 or newer. Python %d.%d detected" % sys.version_info[:2]))
    sys.exit(-1)


if (sys.platform == 'darwin'):
    mac_ver = str(LooseVersion(get_config_var('MACOSX_DEPLOYMENT_TARGET')))
    os.environ['MACOSX_DEPLOYMENT_TARGET'] = mac_ver

extensions = [
	Extension(name="optimum_reparamN2",
	    sources=["src/optimum_reparamN2.pyx", "src/DynamicProgrammingQ2.c",
        "src/dp_grid.c", "src/dp_nbhd.c"],
	    include_dirs=[numpy.get_include()],
	    language="c"
	),
    dp_build.ffibuilder.distutils_extension(),
]


def parse_requirements_file(filename):
    """Read the lines of the requirements file."""
    with open(filename) as input_file:
        return input_file.read().splitlines()


if __name__ == '__main__':
    requirements = parse_requirements_file('requirements.txt')
    packages = ['warping']
    optional_dependencies = {}

    for requirement in requirements:
        packages.append(requirement)  
        
    setup(
        cmdclass={'build_ext': build_ext},
    	ext_modules=extensions,
        name='warping',
        version='0.0.1',
        packages=['warping'],
        description='Warping Functions Computation using Dynamic Programming',
        classifiers=[
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: Mathematics',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.8',
        ]
    )
