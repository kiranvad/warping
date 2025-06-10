import sys
import os
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

def get_numpy_include():
    """Get numpy include directory without importing numpy at setup time."""
    try:
        import numpy
        return numpy.get_include()
    except ImportError:
        # If numpy is not installed, return a placeholder that will be resolved later
        # This allows the setup to proceed and numpy will be installed as a dependency
        return ""

class BuildExtCommand(build_ext):
    """Custom build_ext command that ensures numpy is available before building."""
    
    def build_extensions(self):
        # Ensure numpy is available when actually building
        try:
            import numpy
        except ImportError:
            raise ImportError("numpy is required to build extensions. Please install numpy first.")
        
        # Update include directories with actual numpy path
        for ext in self.extensions:
            if hasattr(ext, 'include_dirs'):
                # Replace empty string placeholder with actual numpy include path
                ext.include_dirs = [numpy.get_include() if inc == "" else inc for inc in ext.include_dirs]
                # Also add numpy include if not present
                if numpy.get_include() not in ext.include_dirs:
                    ext.include_dirs.append(numpy.get_include())
        
        super().build_extensions()

extensions = [
    Extension(name="optimum_reparamN2",
        sources=["src/optimum_reparamN2.pyx", "src/DynamicProgrammingQ2.c",
        "src/dp_grid.c", "src/dp_nbhd.c"],
        include_dirs=[get_numpy_include()],
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
        cmdclass={'build_ext': BuildExtCommand},
        ext_modules=extensions,
        name='warping',
        version='0.0.1',
        packages=['warping'],
        description='Warping Functions Computation using Dynamic Programming',
        install_requires=['numpy'],  # Ensure numpy is installed as a dependency
        setup_requires=['numpy'],    # Ensure numpy is available during setup
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