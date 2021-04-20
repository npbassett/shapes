"""
File: ashes/LunarHorizonCalculator.py
Author: Neil Bassett
Date: 20 April 2021

Description: File containing LunarHorizonCalculator class which reads
             elevation data and calculates the angular horizon from a given
             location on the surface of the Moon.
"""
import os
import time
import numpy as np
import elevation
import richdem as rd
import matplotlib.pyplot as plt
from osgeo import gdal, gdal_array
from scipy.interpolate import RectBivariateSpline
from .BaseHorizonCalculator import BaseHorizonCalculator

class LunarHorizonCalculator(BaseHorizonCalculator):
    """
    An object which calculates the angular horizon as seen from a
    location on the Moon at the given coordinates.
    """
    def __init__(self, observer_coordinates, gamma_min=0.005, gamma_max=8.0):
        """
        Initializes a new LunarHorizonCalculator object with the given
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
        Property storing the radius of the body (i.e. the Moon) in meters.
        """
        if not hasattr(self, '_body_radius'):
            self._body_radius = 1.7371e6
        return self._body_radius

    @property
    def longitude_resolution(self):
        """
        Property storing the size of an elevation grid pixel in
        longitude.
        """
        if not hasattr(self, '_longitude_resolution'):
            self._longitude_resolution = 360. / 92160.
        return self._longitude_resolution

    @property
    def latitude_resolution(self):
        """
        Property storing the size of an elevation grid pixel in
        latitude.
        """
        if not hasattr(self, '_latitude_resolution'):
            self._latitude_resolution = 180. / 46080.
        return self._latitude_resolution

    @property
    def grid_width_longitude(self):
        """
        Property storing the size of the elevation grid in longitude.
        """
        if not hasattr(self, '_grid_width_longitude'):
            self._grid_width_longitude = 20.
        return self._grid_width_longitude

    @grid_width_longitude.setter
    def grid_width_longitude(self, value):
        """
        Setter for the grid_width_longitude property.

        Value: positive number greater than gamma_max
        """
        if value < self.gamma_max:
            raise ValueError('grid_width_longitude must be larger' +\
                'than gamma_max.')
        self._grid_width_longitude = value

    @property
    def grid_width_latitude(self):
        """
        Property storing the size of the elevation grid in latitude.
        """
        if not hasattr(self, '_grid_width_latitude'):
            self._grid_width_latitude = 20.
        return self._grid_width_latitude

    @grid_width_latitude.setter
    def grid_width_latitude(self, value):
        """
        Setter for the grid_width_latitude property.

        Value: positive number greater than gamma_max
        """
        if value < self.gamma_max:
            raise ValueError('grid_width_latitude must be larger' +\
                'than gamma_max.')
        self._grid_width_latitude = value

    @property
    def elevation_grid(self):
        """
        Property storing the grid containing the elevation data.
        """
        if not hasattr(self, '_elevation_grid'):
            t_start = time.time()
            elevation_data_path = '{!s}/input/'.format(os.getenv('ASHES')) +\
                'LOLA/Lunar_LRO_LOLA_Global_LDEM_118m_Mar2014.tif'
            raster_array = gdal_array.LoadFile(elevation_data_path)
            raster_res_deg = 180. / raster_array.shape[0]
            lon_bounds_pix = (int((180. + self.bounds[0]) / raster_res_deg),\
                int((180. + self.bounds[2]) / raster_res_deg))
            lat_bounds_pix = (int((90. - self.bounds[3]) / raster_res_deg),\
                int((90. - self.bounds[1]) / raster_res_deg))
            self._elevation_grid =\
                raster_array[lat_bounds_pix[0]:lat_bounds_pix[1],\
                lon_bounds_pix[0]:lon_bounds_pix[1]]
            raster_array = None
            print('Read lunar elevation data in %.2f minutes' %\
                ((time.time() - t_start) / 60.))
        return self._elevation_grid
