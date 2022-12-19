"""
Module:
    coordinates.py

Description:
    This file provides classes for coordinate systems.

Usage:
    from env.coordinates import CartesianPoint, CartesianVector
    point = CartesianPoint(0, 2, 5)

Notes:


References:


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
import utils


class CartesianPoint:
    """
    This class holds a point in a Cartesian coordinate system.
    """

    DEFAULT_MAP = {'x': 0, 'y': 1, 'z': 2}

    def __init__(self, x: float, y: float, z: float, mapping: [dict, None] = None):
        """
        Instantiate the class.

        Args:
            x:          The value along the x-axis of the Cartesian coordinates.
            y:          The value along the y-axis of the Cartesian coordinates.
            z:          The value along the z-axis of the Cartesian coordinates.
            mapping:    Mapping of coordinates to elements in the vector.

        Notes:
            Units (meters vs feet) need to be scrubbed at a level above this.
        """

        if mapping is None:
            mapping = self.DEFAULT_MAP

        self._mapping = mapping
        self._vector = np.zeros((3, 1), dtype=np.float)
        self._set_values_based_on_mapping(x=x, y=y, z=z)

    def _set_values_based_on_mapping(self, x: float, y: float, z: float):
        """
        The default mapping may not be the desired mapping for a user. They can
        override that mapping. This is a convenience function for setting the values
        in the vector. The point is stored and operated on as a vector because it
        is much faster than working with individual points and most calculations
        are done on the vector anyway.

        Args:
            x:          The value along the x-axis of the Cartesian coordinates.
            y:          The value along the y-axis of the Cartesian coordinates.
            z:          The value along the z-axis of the Cartesian coordinates.

        Returns:
            N/A - instance variables are set.
        """

        self._vector[self._mapping['x'], 0] = x
        self._vector[self._mapping['y'], 0] = y
        self._vector[self._mapping['z'], 0] = z

    def __str__(self) -> str:
        output = f'{self.__class__.__name__}:\n'
        for k, _ in self._mapping.items():
            output += utils.strings.formatted_line(f'{k}: {self[k]}', tab_level=1)

        return output

    def __repr__(self) -> str:
        output = utils.strings.formatted_line(f'{self.__class__.__name__}', tab_level=1)
        for k, index in self._mapping.items():
            output += utils.strings.formatted_line(f'{k}={self._vector[index, 0]},', tab_level=2)

        output += utils.strings.formatted_line(f'mapping={self._mapping},', tab_level=2)

        output += utils.strings.formatted_line(')', tab_level=1)
        # output += f'\n\n{self}'
        return output

    def __getitem__(self, key: str):
        # Allow access via class_name['property'].
        # https://stackoverflow.com/questions/11469025/how-to-implement-a-subscriptable-class-in-python-subscriptable-class-not-subsc
        return self._vector[self._mapping[key], 0]

    def __setitem__(self, key: str, value):
        # Allows for setting an instance property via class_name['property'] = value
        self._vector[self._mapping[key], 0] = value

    def __add__(self, other) -> 'CartesianPoint':
        vector = self.as_vector + other.as_vector   # Identical mapping is presumed for performance reasons.
        return CartesianPoint.from_vector(vector=vector, mapping=self.mapping)

    def __sub__(self, other) -> 'CartesianPoint':
        vector = self.as_vector - other.as_vector  # Identical mapping is presumed for performance reasons.
        return CartesianPoint.from_vector(vector=vector, mapping=self.mapping)

    def __mul__(self, other) -> 'CartesianPoint':
        # Just use numpy's multiplication.
        try:
            return CartesianPoint.from_vector(vector=self.as_vector.__mul__(other.as_vector), mapping=self.mapping)
        except AttributeError:
            return CartesianPoint.from_vector(vector=self.as_vector * other, mapping=self.mapping)

    def __rmul__(self, other) -> 'CartesianPoint':
        # Just use numpy's multiplication.
        try:
            return CartesianPoint.from_vector(vector=self.as_vector.__rmul__(other.as_vector), mapping=self.mapping)
        except AttributeError:
            return CartesianPoint.from_vector(vector=self.as_vector * other, mapping=self.mapping)

    def copy(self) -> 'CartesianPoint':
        """
        Returns a copy of this instance of the object.

        Returns:
            (CartesianPoint) Copy of this instance.
        """

        return self.__class__(
            x=self.x,
            y=self.y,
            z=self.z,
            mapping=self._mapping
        )

    @staticmethod
    def from_vector(vector: np.array, mapping: [dict, None] = None) -> 'CartesianPoint':
        """
        This method allows for the creation of a CartesianPoint from a vector.

        Args:
            vector:     Vector of values for each axis.
            mapping:    Mapping of coordinates to elements in the vector.

        Returns:

        """

        if mapping is None:
            mapping = CartesianPoint.DEFAULT_MAP

        # Instantiate a Cartesian object from a vector.
        return CartesianPoint(
            x=vector[mapping['x']],
            y=vector[mapping['y']],
            z=vector[mapping['z']]
        )

    def convert_point_to_new_map(self, mapping: dict) -> 'CartesianPoint':
        """
        While it is unlikely that we would want to use different maps for Cartesian points
        it is conceivable. As a result, this conversion method is provided.

        Args:
            mapping:        Mapping of coordinates to elements in the vector.

        Returns:
            (CartesianPoint) Point with the vector conforming to the new mapping.
        """

        return self.__class__(
            x=self.x,
            y=self.y,
            z=self.z,
            mapping=mapping
        )

    @property
    def as_vector(self) -> np.array:
        return self._vector

    @as_vector.setter
    def as_vector(self, value: np.ndarray):
        self._vector = value.reshape(self._vector.shape)

    @property
    def x(self) -> float:
        return self._vector[self._mapping['x'], 0]

    @x.setter
    def x(self, value: float):
        self._vector[self._mapping['x'], 0] = value

    @property
    def y(self) -> float:
        return self._vector[self._mapping['y'], 0]

    @y.setter
    def y(self, value: float):
        self._vector[self._mapping['y'], 0] = value

    @property
    def z(self) -> float:
        return self._vector[self._mapping['z'], 0]

    @z.setter
    def z(self, value: float):
        self._vector[self._mapping['z'], 0] = value

    @property
    def mapping(self) -> dict:
        return self._mapping


class CartesianVector(CartesianPoint):
    """
    This class holds a vector in a Cartesian coordinate system.
    """

