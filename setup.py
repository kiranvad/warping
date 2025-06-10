import numpy
import sys, os
from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from distutils.sysconfig import get_config_var
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

if __name__ == '__main__':
    setup(
        cmdclass={'build_ext': build_ext},
        ext_modules=extensions,
    )