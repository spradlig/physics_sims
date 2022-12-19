"""
Module:
    __init__.py

Description:
    This file allows for the code in this package to operate similar to any pip/conda installed
    package.

Usage:
    N/A

License:
    https://creativecommons.org/licenses/by-nc-nd/4.0/
    Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
    See LICENSE.txt

"""

"""
Version History:
    Original:
        Gabe Spradlin | 12-Dec-2022
"""

"""
TODOs:
    1)
"""

# Standard library imports
import numpy as np

# Tool imports
from env.coordinates import CartesianVector


class CartesianForce(CartesianVector):
    """
    This class represents a force in the Cartesian coordinate system.
    """


class Gravity(CartesianForce):
    """
    For sims using an ECEF reference frame, gravity always acts in -z in the Inertial Frame.
    """

    def __init__(self, **kwargs):
        """
        Instantiate the class.

        Args:
            kwargs:     Ignored.

        Notes:
            Units (meters vs feet) need to be scrubbed at a level above this.
        """

        # https://en.wikipedia.org/wiki/Gravity_of_Earth
        super().__init__(x=0., y=0., z=-9.80665)
