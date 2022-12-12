# -*- coding: utf-8 -*-
"""
Module:
    sim_clock.py

Description:
    This file holds the SimClock class which is used to manage the time/clock
    of a simulation.

Usage:
    from simple_event_driven_model.sim_clock import SimClock

    clock = SimClock(timestep=0.01)

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


# Custom Package Imports
from event import EventManager, Event


class SimClock:
    """
    This class is a clock for a simulation.
    """

    def __init__(self, timestep: [float, None] = None):
        """

        Args:
            timestep:       A float to define the timestep to be taken.
        """

        # The timestep can be a float, constant value, or None. If None, then we
        # are using an adaptive timestep.
        if timestep is not None:
            self._timestep = lambda: timestep
        else:
            # This isn't actually adaptive at this time. It is here to demonstrate
            # how you would do it.
            self._timestep = self.__adaptive_timestep

        self._time = 0.

        # Events for the SimClock -
        #   timestep:   functions to fire at each timestep
        self._events = EventManager(timestep=Event('timestep'))

        # Add a basic event function to provide feedback, on screen, for the user.
        self.add_function_to_timestep(
            'user_feedback',
            lambda timestep, time: print(f'Timestep: {timestep}, Time: {time} sec')
        )

    def __adaptive_timestep(self) -> float:
        """
        Implementing an adaptive step is complicated and would use something like
        a Runge-Kutta ODE solver style of algorithm. This requires all sort of
        feedback from the physics engine to ensure no part of the physics engine
        has shown dynamics changes which are "too large".

        Returns:
            float:      A timestep (float) which is >= 0.
        """

        # Implementing an adaptive timestep is significant project all by itself.

        return 1.

    def add_function_to_timestep(self, name: str, function: callable):
        """

        Args:
            name:       A descriptive name for the function.
            function:   The function to be executed.

        Returns:

        """

        self._events['timestep'].add_function(name=name, function=function)

    def execute_timestep(self):
        """
        This method executes all of the functions tied to the timestep event.

        Returns:
            N/A
        """

        timestep = self.timestep
        self._time += timestep

        self._events['timestep'].fire(timestep=timestep, time=self._time)

    @property
    def timestep(self) -> float:
        return self._timestep()

    @property
    def time(self) -> float:
        return self._time
