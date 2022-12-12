# -*- coding: utf-8 -*-
"""
Module:
    ballistic.py

Description:
    This file holds the Ballistic class which is a simple Physics 101
    example of ballistic motion of an object with an initial state
    (position, velocity, and acceleration).

Usage:
    from simple_event_driven_model.ballistic import Ballistic

    golf_ball = Ballistic(
        initial_state=State(
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

# Standard Library Imports
import numpy as np
import pandas as pd

# Custom Package Imports
from state import State, Cartesian


class Ballistic:
    """
    This class is the framework of the classic Physics 101
    ballistic motion.
    """

    def __init__(self, initial_state: State):
        """
        Instantiate the class.

        Args:
            initial_state:  The initial state of the object.
        """

        self._state = initial_state

        self._states = []
        self.capture_state()

    def dynamics(self, timestep: float, time: float):
        """
        The dynamics equations based on a timestep.

        Args:
            timestep:   The timestep since the last time this
                        method was called. [sec]
            time:       The absolute sim time. [sec]

        Returns:
            N/A
        """

        self._state.velocity = self._state.velocity + (self._state.acceleration * timestep)
        self._state.position = self._state.position + (self._state.velocity * timestep)
        self._state.time = time

        # Log states for later analysis.
        self.capture_state()

    def capture_state(self):
        """
        Log states for later analysis.

        Returns:
            N/A
        """

        self._states.append(self._state.as_vector)

    @property
    def state(self) -> State:
        return self._state

    @property
    def states(self) -> pd.DataFrame:
        states = pd.DataFrame(
            self._states,
            columns=[
                'Time [sec]',
                'Position x [m]', 'Position y [m]', 'Position z [m]',
                'Velocity x [m/s]', 'Velocity y [m/s]', 'Velocity z [m/s]',
                'Acceleration x [m/s^2]', 'Acceleration y [m/s^2]', 'Acceleration z [m/s^2]',
            ]
        )
        states.set_index('Time [sec]', inplace=True)

        return states
