# ASHES
The Angular Solver for Horizon from Elevation Sets (ASHES) code calculates the angular horizon as seen from a given location. While ASHES was developed primarily for low radio frequency global 21-cm experiments, the code is broadly applicable.

## Getting Started
To clone a copy of the repository and install:
```
git clone https://github.com/npbassett/ashes.git
cd ashes
python setup.py develop
```

To download the LRO LOLA elevation data needed for lunar horizon calculations:
```
python remote.py
```
Note that this step will take a few minutes and download an ~8 GB file. If you only want to calculate horizons for locations on Earth, you can skip this step. If something goes wrong or you would like to download a new copy:
```
python remote.py fresh
```
In order for *ashes* to access the input data, it will look in `$ASHES/input` so you will need to set an environment variable that points to the *ashes* install directory in your shell startup file (e.g. `.bashrc`):
```
export ASHES=/users/<yourusername>/ashes
```

## Dependencies
You will need the following Python packages:
* [numpy](http://www.numpy.org/)
* [scipy](http://www.scipy.org/)
* [matplotlib](http://matplotlib.org/)
* [elevation](https://pypi.org/project/elevation/)
* [richdem](https://richdem.readthedocs.io/en/latest/)
* [GDAL](https://pypi.org/project/GDAL/)

## Contributors
Primary Author: Neil Bassett
