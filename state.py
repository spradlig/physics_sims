# -*- coding: utf-8 -*-
"""
Module:
    state.py

Description:
    This file holds a class for the State of an object as well as
    a class, Cartesian, for the coordinate frame.

Usage:
    from simple_event_driven_model.state import State, Cartesian

    initial_state = State(
        position=Cartesian(
            x=0.,
            y=0.,
            z=15.
        ),
        velocity=Cartesian(
            x=10.,
            y=10.,
            z=1.
        ),
        acceleration=Cartesian(
            x=0.,
            y=0.,
            z=-9.8
        ),
    )

Notes:


References:


"""

"""
Version History:
    Original:
        GS | 22-Oct-21
"""

"""
TODOs:
    1)
"""

# Standard Library
import numpy as np


class Cartesian:
    """
    A simple class for the Cartesian coordinate frame.
    """

    def __init__(self, x: float = 0., y: float = 0., z: float = 0.):
        """
        Instantiate the class.

        Args:
            x:      The x-axis value of the Cartesian coordinate vector.
            y:      The y-axis value of the Cartesian coordinate vector.
            z:      The z-axis value of the Cartesian coordinate vector.
        """

        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        # This function defines the display when we type an instantiated class
        # instance into Spyder or iPython.
        return self.__str__()

    def __str__(self):
        # This function defines the display when we type an instantiated class
        # instance into Spyder or iPython.
        return f'\tCartesian: [{self.x:0.4f}, {self.y:0.4f}, {self.z:0.4f}]'

    def __add__(self, other) -> 'Cartesian':
        # Add 2 Cartesian classes and return a new one.
        if isinstance(other, Cartesian) is True:
            output = Cartesian(
                x=self.x + other.x,
                y=self.y + other.y,
                z=self.z + other.z
            )
        else:
            raise ValueError('There is no method to multiply Cartesian by {0}.'.format(type(other)))

        return output

    def __sub__(self, other) -> 'Cartesian':
        # Subtract 2 Cartesian classes and return a new one.

        if isinstance(other, Cartesian) is True:
            output = Cartesian(
                x=self.x - other.x,
                y=self.y - other.y,
                z=self.z - other.z
            )
        else:
            raise ValueError('There is no method to multiply Cartesian by {0}.'.format(type(other)))

        return output

    def __mul__(self, other) -> 'Cartesian':
        # Multiply 2 Cartesian classes and return a new one. Or multiply a Cartesian vector by a
        # float (scalar).

        try:
            _ = float(other)
        except ValueError:
            pass

        if isinstance(other, float) is True:
            output = Cartesian(
                x=self.x * other,
                y=self.y * other,
                z=self.z * other
            )

            return output
        elif isinstance(other, Cartesian) is True:
            output_vector = np.cross(self.as_vector, other.as_vector)
            return Cartesian.from_vector(output_vector)
        else:
            raise ValueError('There is no method to multiply Cartesian by {0}.'.format(type(other)))

    @staticmethod
    def from_vector(vector: np.array) -> 'Cartesian':
        # Instantiate a Cartesian object from a vector.
        return Cartesian(
            x=vector[0],
            y=vector[1],
            z=vector[2]
        )

    @property
    def as_vector(self) -> np.array:
        return np.array([self.x, self.y, self.z])


class State:
    """
    A class for holding the state of an object. Currently the state is limited to the
    time (float), position (Cartesian), velocity (Cartesian), and acceleration (Cartesian).
    """

    def __init__(self, position: Cartesian, velocity: Cartesian, acceleration: Cartesian):
        """
        Instantiate the class.
        """

        self._position = position
        self._velocity = velocity
        self._acceleration = acceleration
        self.time = 0.

    def __repr__(self):
        # This function defines the display when we type an instantiated class
        # instance into Spyder or iPython.
        return self.__str__()

    def __str__(self):
        # This function defines the display when we type an instantiated class
        # instance into Spyder or iPython.
        return f'\tState: \n\t\t\tPosition: {self._position}\n\t\t\tVelocity: {self._velocity}\n\t\tAcceleration: {self._acceleration}'

    @property
    def position(self) -> Cartesian:
        return self._position

    @position.setter
    def position(self, value: Cartesian):
        # We do it this way only so that we can add checks on value later.
        self._position = value

    @property
    def velocity(self) -> Cartesian:
        return self._velocity

    @velocity.setter
    def velocity(self, value: Cartesian):
        # We do it this way only so that we can add checks on value later.
        self._velocity = value

    @property
    def acceleration(self) -> Cartesian:
        return self._acceleration

    @acceleration.setter
    def acceleration(self, value: Cartesian):
        # We do it this way only so that we can add checks on value later.
        self._acceleration = value

    @property
    def as_vector(self) -> np.array:
        return np.hstack((self.time, self.position.as_vector, self.velocity.as_vector, self.acceleration.as_vector))
