# SHAPES
The Simulating Horizon Angle Profile from Elevation Sets (SHAPES) code calculates the angular horizon as seen from a given location. While SHAPES was developed primarily for low radio frequency global 21-cm experiments, the code is broadly applicable.

## Getting Started
To clone a copy of the repository and install:
```
git clone https://github.com/npbassett/shapes.git
cd shapes
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
In order for *shapes* to access the lunar data, it will look in `$SHAPES/input` so you will need to set an environment variable that points to the *shapes* install directory in your shell startup file (e.g. `.bashrc`):
```
export SHAPES=/users/<yourusername>/shapes
```

## Dependencies
You will need the following Python packages:
* [numpy](http://www.numpy.org/)
* [scipy](http://www.scipy.org/)
* [matplotlib](http://matplotlib.org/)
* [elevation](https://pypi.org/project/elevation/)
* [richdem](https://richdem.readthedocs.io/en/latest/)
* [GDAL](https://pypi.org/project/GDAL/)

Optional:
* [progressbar2](https://progressbar-2.readthedocs.io/en/latest/)

## Contributors
Primary Author: Neil Bassett
