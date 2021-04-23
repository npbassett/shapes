"""
File: shapes/examples/terrestrial_horizon_calculator.py
Author: Neil Bassett
Date: 20 April 2021

Description: Example showing how to use the TerrestrialHorizonCalculator
             class.
"""
from shapes import CTP_coordinates, TerrestrialHorizonCalculator
import matplotlib.pyplot as plt

terrestrial_horizon_calculator = TerrestrialHorizonCalculator(CTP_coordinates)
N_alpha = 361
N_gamma = 1000
horizon_azimuths, horizon_profile =\
    terrestrial_horizon_calculator.horizon_profile(N_alpha, N_gamma)

fig, ax = plt.subplots(figsize=(20, 5))
plt.plot(horizon_azimuths, horizon_profile)
plt.xlim(0, 360)
plt.xlabel('Azimuth (deg)')
plt.ylabel('Horizon Angle (deg)')
plt.show()
