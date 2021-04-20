"""
File: ashes/TerrestrialHorizonCalculator.py
Author: Neil Bassett
Date: 20 April 2021

Description: File containing Terrestrial HorizonCalculator class which reads
             elevation data and calculates the angular horizon from a given
             on Earth location.
"""
import os
import time
import numpy as np
import elevation
import richdem as rd
import matplotlib.pyplot as plt
from scipy.interpolate import RectBivariateSpline
from .BaseHorizonCalculator import BaseHorizonCalculator

class TerrestrialHorizonCalculator(BaseHorizonCalculator):
    """
    An object which calculates the angular horizon as seen from a
    location on Earth at the given coordinates.
    """
    def __init__(self, observer_coordinates, gamma_min=0.005, gamma_max=1.0):
        """
        Initializes a new TerrestrialHorizonCalculator object with the given
        inputs.

        observer_coordinates: tuple of the form (longitude, latitude) in degrees
        gamma_min: minimum angle which to consider in the calculation of the
                   horizon (in degrees)
        gamma_max: maximum angle which to consider in the calculation of the
                   horizon (in degrees)
        """
        self.observer_coordinates = observer_coordinates
        self.gamma_min = gamma_min
        self.gamma_max = gamma_max

    @property
    def body_radius(self):
        """
        Property storing the radius of the body (i.e. the Earth) in meters.
        """
        if not hasattr(self, '_body_radius'):
            self._body_radius = 6.378e6
        return self._body_radius

    @property
    def elevation_grid(self):
        """
        Property storing the grid containing the elevation data.
        """
        if not hasattr(self, '_elevation_grid'):
            dem_path = os.path.join(os.getcwd(), 'DEM.tif')
            elevation.clip(bounds=self.bounds, output=dem_path)
            self._elevation_grid = np.array(rd.LoadGDAL(dem_path))
        return self._elevation_grid
