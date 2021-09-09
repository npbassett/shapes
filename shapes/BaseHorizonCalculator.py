"""
File: shapes/BaseHorizonCalculator.py
Author: Neil Bassett
Date: 20 April 2021

Description: File containing BaseHorizonCalculator class which contains common
             properties of both the TerrestrialHorizonCalculator and
             LunarHorizonCalculator classes.
"""
import os
import time
import numpy as np
import elevation
import richdem as rd
import matplotlib.pyplot as plt
from scipy.interpolate import RectBivariateSpline

class BaseHorizonCalculator(object):
    """
    Base class containing common properties of both the
    TerrestrialHorizonCalculator and LunarHorizonCalculator classes.
    """
    @property
    def observer_coordinates(self):
        """
        Property storing the coordinates of the observer in (lon, lat).
        """
        if not hasattr(self, '_observer_coordinates'):
            raise AttributeError('observer_coordinates was referenced before ' +\
                'it was set.')
        return self._observer_coordinates

    @observer_coordinates.setter
    def observer_coordinates(self, coordinates):
        """
        Setter for the coordinates of the observer.

        coordinates: (longitude, latitude) in degrees
        """
        if (coordinates[0] < -180.) or (coordinates[0] > 180.):
            raise ValueError('Longitude coordinate must be between ' +\
                '-180 and 180 degrees')
        elif (coordinates[1] < -90.) or (coordinates[1] > 90.):
            raise ValueError('Latitude coordinate must be between ' +\
                '-90 and 90 degrees')
        self._observer_coordinates = coordinates

    @property
    def gamma_min(self):
        """
        Property storing the minimum gamma angle which to consider for
        calculation of the horizon.
        """
        if not hasattr(self, '_gamma_min'):
            raise AttributeError('gamma_min was referenced before ' +\
                'it was set.')
        return self._gamma_min

    @gamma_min.setter
    def gamma_min(self, value):
        """
        Setter for the minimum gamma angle to conside for the horizon.

        value: positive value (in degrees)
        """
        if value <= 0:
            raise ValueError('gamma_min must be an angle greater than or ' +\
                'equal to 0.')
        self._gamma_min = value

    @property
    def gamma_max(self):
        """
        Property storing the maximum gamma angle which to consider for
        calculation of the horizon.
        """
        if not hasattr(self, '_gamma_max'):
            raise AttributeError('gamma_max was referenced before ' +\
                'it was set.')
        return self._gamma_max

    @gamma_max.setter
    def gamma_max(self, value):
        """
        Setter for the minimum gamma angle to conside for the horizon.

        value: positive value (in degrees)
        """
        if value <= self.gamma_min:
            raise ValueError('gamma_max must be greater than or ' +\
                'equal to gamma_min')
        self._gamma_max = value

    @property
    def observer_elevation(self):
        """
        Property storing the elevation of the observer.
        """
        if not hasattr(self, '_observer_elevation'):
            self._observer_elevation = self.interpolate_elevation(0., 0.)
        return self._observer_elevation

    @property
    def bounds(self):
        """
        Property storing the bounds of the elevation data grid.
        """
        if not hasattr(self, '_bounds'):
            lon_lower_bound = self.observer_coordinates[0] -\
                (self.grid_width_longitude / 2.)
            lon_upper_bound = self.observer_coordinates[0] +\
                (self.grid_width_longitude / 2.)
            lat_lower_bound = self.observer_coordinates[1] -\
                (self.grid_width_latitude / 2.)
            lat_upper_bound = self.observer_coordinates[1] +\
       	        (self.grid_width_latitude / 2.)
            self._bounds =\
                [lon_lower_bound, lat_lower_bound,\
                 lon_upper_bound, lat_upper_bound]
        return self._bounds

    @bounds.setter
    def bounds(self, bounds):
        """
        Setter for the bounds of the elevation data grid.

        bounds: (left, bottom, right, top) in degrees
        """
        if bounds[0] > bounds[2]:
            raise ValueError('Left boundary cannot be greater than the ' +\
                'right boundary')
        elif bounds[1] > bounds[3]:
            raise ValueError('Bottom boundary cannot be greater than the ' +\
                'top boundary')
        self._bounds = bounds

    @property
    def includes_pole(self):
        """
        Property that stores a boolean value, which is True if the bounds
        encompass either the North or South Pole.
        """
        if not hasattr(self, '_includes_pole'):
            if (self.bounds[1] < -90.) or (self.bounds[3] > 90.):
                self._includes_pole = True
            else:
                self._includes_pole = False
        return self._includes_pole

    @property
    def elevation_interpolation_degree(self):
        """
        Property storing the degree of the spline to use in interpolating
        the elevation data grid.
        """
        if not hasattr(self, '_elevation_interpolation_degree'):
            self._elevation_interpolation_degree = 3
        return self._elevation_interpolation_degree

    @elevation_interpolation_degree.setter
    def elevation_interpolation_degree(self, value):
        """
        Setter for the elevation_interpolation_degree property.

        value: integer
        """
        if value <= 0:
            return ValueError('elevation_interpolation_degree must be a' +\
                'positive integer')
        self._elevation_interpolation_degree = value

    @property
    def elevation_interpolation_function(self):
        """
        Property storing the function that interpolates the elevation data
        between grid points.
        """
        if not hasattr(self, '_elevation_interpolation_function'):
            lon_array = np.arange(self.bounds[0], self.bounds[2],\
                self.longitude_resolution)
            lat_array = np.arange(self.bounds[1], self.bounds[3],\
                self.latitude_resolution)
            self._elevation_interpolation_function = RectBivariateSpline(\
                lon_array, lat_array, np.flip(self.elevation_grid.T, axis=1),\
                kx=self.elevation_interpolation_degree,\
                ky=self.elevation_interpolation_degree)
        return self._elevation_interpolation_function

    def find_lon_lat(self, alpha, gamma):
        """
        This function calculates the longitude and latitude coordinate
        of a point given the location of the observer and an azimuthal
        angle (alpha) and angular distance (gamma).

        alpha: azimuthal angle defined such that 0 corresponds to North
               and increases clockwise (in radians)
        gamma: angular distance (in radians)
        coords: coordinates of the observer in the form (lon, lat)

        Returns the longitude (l) and latitude (b) in degrees.
        """
        theta_0 = (np.pi / 2.) - (self.observer_coordinates[1] * (np.pi / 180.))
        phi_0 = self.observer_coordinates[0] * (np.pi / 180.)
        theta = np.arccos((np.cos(theta_0) * np.cos(gamma)) +\
            (np.cos(alpha) * np.sin(theta_0) * np.sin(gamma)))
        phi = np.angle(((np.sin(theta_0) * np.cos(gamma)) +\
            (1j * np.sin(alpha) * np.sin(gamma)) -\
            (np.cos(alpha) * np.cos(theta_0) * np.sin(gamma))) *\
            np.exp(1j * phi_0))
        l = (180. / np.pi) * phi
        b = 90. - ((180. / np.pi) * theta)
        return l, b

    def interpolate_elevation(self, alpha, gamma):
        """
        This functions interpolates the height at the point defined by
        the given alpha and gamma from the elevation grid.

        alpha: azimuthal angle defined such that 0 corresponds to North
               and increases clockwise (in radians)
        gamma: angular distance (in radians)

        Returns the elevation in meters.
        """
        l, b = self.find_lon_lat(alpha, gamma)
        return self.elevation_interpolation_function(l, b, grid=False)

    def horizon_angle(self, alpha, gamma):
        """
        Calculates the horizon angle for a point defined by the angles alpha and gamma
        relative to the observer.

        alpha: the angle from north of the direction the great circle intersecting the
               observer's position and the point of interest, i.e. the azimuthal
               angle (in radians)
        gamma: the angular distance from the observer to the point of interest
               (in radians)

        Returns eta, the horizon angle of the point of interest, in radians.
        """
        h = self.interpolate_elevation(alpha, gamma)
        eta = np.arctan((1 / np.tan(gamma)) - (((self.body_radius +\
            self.observer_elevation) / (self.body_radius + h)) / np.sin(gamma)))
        return eta

    def horizon_profile(self, N_alpha, N_gamma):
        """
        Calculates the full horizon profile.

        N_alpha: number of azimuth angles from 0 to 2pi
        N_gamma: number of gamma angles (i.e. the angular distance from the
                 observer along the azimuthal angle alpha) from gamma_min
                 to gamma_max

        Returns an array of azimuthal angles and a corresponding array of horizon
        angles making up the horizon profile (in degrees).
        """
        azimuths = np.linspace(0, 2*np.pi, N_alpha, endpoint=True)
        gammas = np.linspace(self.gamma_min * (np.pi / 180.),\
            self.gamma_max * (np.pi / 180.), N_gamma)
        horizon_profile = []
        try:
            import progressbar
            self.elevation_grid
            for i in progressbar.progressbar(np.arange(N_alpha)):
                start = time.time()
                horizon_angles = []
                for gamma in gammas:
                    horizon_angles += [self.horizon_angle(azimuths[i], gamma)]
                horizon_profile += [np.amax(horizon_angles)]
        except ModuleNotFoundError:
            for i in np.arange(N_alpha):
                start = time.time()
                horizon_angles = []
                for gamma in gammas:
                    horizon_angles += [self.horizon_angle(azimuths[i], gamma)]
                horizon_profile += [np.amax(horizon_angles)]
                print('alpha angle %i/%i completed in %.1f seconds...'\
                    % (i+1, len(azimuths), time.time() - start))
        return np.array(azimuths) * (180. / np.pi),\
            np.array(horizon_profile) * (180. / np.pi)

    def plot_topo_map(self, show=True, **kwargs):
        """
        Plots a 2D map of the elevation data.

        show: if True, matplotlib.pyplot.show() is called before this function
              returns
        **kwargs: keyword arguments to pass to matplotlib.pyplot.imshow()
        """
        fig, ax = plt.subplots()
        plt.scatter(*self.observer_coordinates, c='r', marker='*', s=50)
        plt.imshow(self.elevation_grid, extent=(self.bounds[0], self.bounds[2],\
            self.bounds[1], self.bounds[3]), cmap='terrain', **kwargs)
        plt.xlabel(r'Longitude ($^{\circ}$)')
        plt.ylabel(r'Latitude ($^{\circ}$)')
        plt.colorbar(label='Elevation (m)')
        if show:
            plt.show()
