This repository is a copy of the original code that only contains the DP code required to compute warping functions between a pair of functions. You should refer to the main repository here for all citations/questions here: https://github.com/jdtuck/fdasrsf_python

This repository exists because I had several issues with installing the entire fdasrsf repo on my local computer.

To install this package, you can do the following:

1. Create an environment using the following (installs Cython etc..)

```
conda env create --file environment.yml
```

2. Activate the conda environemnt using the following:

```
conda activate warping
```

3. Then install the package locally using pip, for example : 

```
pip install -e .
```

Alternatively, to install it as a package in an existing environment, you can do the following:

1. Install required pacakages using the following:

```
pip install -r requirements.txt
```

2. Then proceed to install the warping package same as step 3 above.