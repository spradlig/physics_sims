"""
Module:
    reference_frames.py

Description:
    <Short description, but thorough, of what is included in the file.>

Usage:
    from env.reference_frames import CartesianInertial, CartesianTranslatingFrame, CartesianStaticOffsetFrame
    <Provide a simple example for each class and function in the file.>

Notes:


References:


License:
    https://creativecommons.org/licenses/by-nc-nd/4.0/
    Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
    See LICENSE.txt

"""
import numpy as np

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


# Tool imports
from env import coordinates
import utils


class CartesianInertial:
    """
    This class defines an Inertial Reference Frame with a Cartesian coordinate system.
    """

    def __init__(self, mapping: [dict, None] = None):
        """
        Instantiate the class.

        Args:
            mapping:    Mapping of coordinates to elements in the coordinate system vector.
        """

        # Note the inertial frame has +x pointed along North, +y along West, and +z Up.
        # It is presume that the origin of the entire sim is the origin of the Inertial
        # frame and we put it at (0, 0, 0) for convenience. Within a local theater it is
        # assumed that the origin is also on the surface of the Earth/Map. In other words,
        # this isn't an ECI style reference frame but rather and ECEF frame.
        self._origin = coordinates.CartesianPoint(x=0., y=0., z=0., mapping=mapping)

    def __str__(self) -> str:
        output = f'{self.__class__.__name__}:\n'
        output += utils.strings.formatted_line(f'Origin: {self.origin}', tab_level=1)

        return output

    def __repr__(self) -> str:
        output = utils.strings.formatted_line(f'{self.__class__.__name__}', tab_level=1)
        output += utils.strings.formatted_line(f'mapping={self.origin.mapping}', tab_level=2)
        output += utils.strings.formatted_line(')', tab_level=1)

        return output

    @property
    def origin(self) -> coordinates.CartesianPoint:
        return self._origin


class CartesianStaticOffsetFrame:
    """
    This class defines a reference frame which is translated but not rotated wrt an
    instance of CartesianInertial.
    """

    def __init__(
            self,
            base_frame: [CartesianInertial, 'CartesianStaticOffsetFrame'],
            origin: coordinates.CartesianPoint
    ):
        """
        Instantiate the class.

        Args:
            base_frame:         The Base Frame object this frame references.
            origin:             This is the origin of the Static Frame in Inertial Frame
                                coordinates.
        """

        self._origin = origin
        self._base_frame = base_frame
        self._objects = {}

    def __str__(self) -> str:
        output = f'{self.__class__.__name__}:\n'
        output += utils.strings.formatted_line(f'Base Frame: {self.base_frame}', tab_level=1)
        output += utils.strings.formatted_line(f'Origin: {self.origin}', tab_level=1)

        return output

    def __repr__(self) -> str:
        output = utils.strings.formatted_line(f'{self.__class__.__name__}', tab_level=1)
        output += utils.strings.formatted_line(f'base_frame={self.base_frame}', tab_level=2)
        output += utils.strings.formatted_line(f'origin={self.origin}', tab_level=2)
        output += utils.strings.formatted_line(')', tab_level=1)

        return output

    def add_object_to_reference_frame(self, name: str, obj):
        """
        Add an object to this Reference Frame.

        Args:
            name:   Human-readable name of the object.
            obj:    Instantiated object in the "world".

        Returns:
            N/A - instance variables are updated.
        """

        self._objects[name] = obj

    @property
    def origin(self) -> coordinates.CartesianPoint:
        return self._origin

    @property
    def base_frame(self) -> CartesianInertial:
        return self._base_frame


class CartesianTranslatingFrame(CartesianStaticOffsetFrame):
    """
    This class defines a reference frame which translates but does not rotate. The translation
    is wrt an instance of CartesianInertial.
    """

    def __init__(
            self,
            base_frame: [CartesianInertial, CartesianStaticOffsetFrame],
            origin: coordinates.CartesianPoint
    ):
        """
        Instantiate the class.

        Args:
            base_frame:         The Inertial Frame object for the simulation.
            origin:             This is the origin of the Static Frame in Inertial Frame
                                coordinates.
        """

        super().__init__(base_frame=base_frame, origin=origin)

    @property
    def origin(self) -> coordinates.CartesianPoint:
        return self._origin

    @origin.setter
    def origin(self, value: coordinates.CartesianPoint):
        self._origin = value


class CartesianTranslatingRotatingFrame(CartesianTranslatingFrame):
    """
    This class holds a reference frame which can translate and rotate wrt the
    Inertial Frame.
    """

    def __init__(
            self,
            base_frame: [CartesianInertial, CartesianStaticOffsetFrame],
            origin: coordinates.CartesianPoint,
            attitude: coordinates.Attitude
    ):
        """
        Instantiate the class.

        Args:
            base_frame:         The Base Frame object that this frame references.
            origin:             This is the origin of the Static Frame in the Base Frame
                                coordinates.
            attitude:           Attitude of the reference frame wrt to the Base Frame.
        """

        super().__init__(base_frame=base_frame, origin=origin)
        self._attitude = attitude

    def __str__(self) -> str:
        output = f'{self.__class__.__name__}:\n'
        output += utils.strings.formatted_line(f'Base Frame: {self.base_frame}', tab_level=1)
        output += utils.strings.formatted_line(f'Origin: {self.origin}', tab_level=1)
        output += utils.strings.formatted_line(f'Attitude: {self.attitude}', tab_level=1)

        return output

    def __repr__(self) -> str:
        output = utils.strings.formatted_line(f'{self.__class__.__name__}', tab_level=1)
        output += utils.strings.formatted_line(f'base_frame={self.base_frame}', tab_level=2)
        output += utils.strings.formatted_line(f'origin={self.origin}', tab_level=2)
        output += utils.strings.formatted_line(f'attitude={self.attitude}', tab_level=2)
        output += utils.strings.formatted_line(')', tab_level=1)

        return output

    def transform_point_in_base_frame_to_this_frame(
            self,
            point: [coordinates.CartesianPoint, coordinates.CartesianVector]
    ) -> [coordinates.CartesianPoint, coordinates.CartesianVector]:
        """

        Args:
            point:

        Returns:

        """

        base_point = point.as_vector
        frame_point = self.dcm_base_to_frame @ (base_point - self.origin.as_vector)
        return point.from_vector(frame_point)

    def transform_point_in_this_frame_to_base_frame(
            self,
            point: [coordinates.CartesianPoint, coordinates.CartesianVector]
    ) -> [coordinates.CartesianPoint, coordinates.CartesianVector]:
        """

        Args:
            point:

        Returns:

        """

        frame_point = point.as_vector
        base_point = self.dcm_frame_to_base @ frame_point
        return point.from_vector(base_point + self.origin.as_vector)

    @property
    def attitude(self) -> coordinates.Attitude:
        return self._attitude

    @attitude.setter
    def attitude(self, value: coordinates.Attitude):
        self._attitude = value

    @property
    def dcm_base_to_frame(self) -> np.ndarray:
        # This calculates the DCM from some base to this frame. The base
        # can be the inertial frame or a NED frame or something else. This
        # is relative to that base.
        attitude = self.attitude
        return utils.angles.dcm(
            w_x=attitude.w_x,
            w_y=attitude.w_y,
            w_z=attitude.w_z,
        )

    @property
    def dcm_frame_to_base(self) -> np.ndarray:
        # This calculates the DCM from this frame to some base. The base
        # can be the inertial frame or a NED frame or something else. This
        # is relative to that base.
        return self.dcm_base_to_frame.T


class NedToInertialFrame(CartesianTranslatingRotatingFrame):
    """
    The NED frame used in aircraft stands for North-East-Down where +x points
    along North, +y points along East, and +z points down toward the center of
    the Earth.

    Note that the Body Frame for an aircraft would have +x along the velocity
    vector.

    Additional note, this is an example of how one could build a specialized
    frame within this framework. Since we do not need to model aircraft dynamics
    we don't need this frame within the tower defense framework.
    """

    def __init__(
            self,
            base_frame: [CartesianInertial, CartesianStaticOffsetFrame],
            origin: coordinates.CartesianPoint,
    ):
        """
        Instantiate the class.

        Args:
            base_frame:         The Base Frame object that this frame references.
            origin:             This is the origin of the Static Frame in the Base Frame
                                coordinates.
        """

        # The DCM used in this sim is the same as is usually used for aircraft.
        # That is to say it is Rot_z * Rot_y * Rot_x or Yaw-Pitch-Roll. The order
        # matters and for a different order these w_x, w_y, and w_z values would
        # produce a different frame.
        #
        # Note that in a tracking type Cartesian reference frame we have +x along
        # North, +z Up, and that requires +y be West.
        ned_attitude = coordinates.Attitude(
            w_x=np.deg2rad(180.),
            w_y=np.deg2rad(0.),
            w_z=np.deg2rad(0.)
        )
        super().__init__(base_frame=base_frame, origin=origin, attitude=ned_attitude)
