"""
Module:
    world.py

Description:
    This file contains the World class and most top-level simulation functions reside in it.

Usage:
    import env
    earth = env.World()

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
from env.coordinates import CartesianPoint, CartesianVector
from env.reference_frames import CartesianInertial, CartesianTranslatingFrame, CartesianStaticOffsetFrame
from utils.events import Event, EventManager


class World:
    """
    This class represents the simulated world. Reference frames, objects, and forces will contain
    a reference to the sim's instantiation of this object.
    """

    def __init__(self, world_config=None):
        """
        Instantiate the class.

        Args:
            world_config:   This is the config parameters for the world and only the world setup.
                            This should not include config params for objects or forces in the
                            world.
        """

        # Capture the world specific portion of the config.
        self._config = world_config

        # Define the default events.
        self._events = EventManager(
            targets_pre_timestep=Event(name='targets_pre_timestep'),
            towers_pre_timestep=Event(name='towers_pre_timestep'),
            targets_timestep=Event(name='targets_timestep'),
            towers_timestep=Event(name='towers_timestep'),
            targets_post_timestep=Event(name='targets_post_timestep'),
            towers_post_timestep=Event(name='towers_post_timestep'),
        )

        # Create the Inertial Frame of the World based on the config.
        if world_config is not None:
            np.random.seed(world_config['random_seed'])

            self._inertial_frame = world_config['inertial_frame']['object']['instance']

            self._objects = {k: v['object']['instance'] for k, v in world_config['objects'].items()}
            self._forces = {k: v['object']['instance'] for k, v in world_config['forces'].items()}
            self._clutter = {k: v['object']['instance'] for k, v in world_config['clutter'].items()}

            self._clock = world_config['clock']
            self._timestep = world_config['timestep']

            for name, event in world_config['extra_events'].items():
                self._events.add_event(name=name, event=event)

        else:
            np.random.seed(42)

            # No config was provided. Provide a default Inertial Frame.
            self._inertial_frame = CartesianInertial()

            # Dicts for holding the objects and forces present in this world.
            self._objects = {}
            self._forces = {}
            self._clutter = {}

            # Define the simulation clock.
            #   In previous sims I've built, the sim clock was its own class but for this
            #   sim it made sense to roll the sim clock into this world object.
            self._clock = 0.
            self._timestep = None

    def add_object_to_world(self, name: str, obj):
        """
        Add an object to the world.

        Args:
            name:   Human-readable name of the object.
            obj:    Instantiated object in the world.

        Returns:
            N/A - instance variables are updated.
        """

        if name not in self._objects:
            self._objects[name] = obj
        else:
            raise ValueError(f'The name {name} is already present. Each object in the world must have a unique name.')

    def remove_object_from_world(self, name: str):
        """
        Remove an from this world.

        Args:
            name:   Human-readable name of the object.

        Returns:
            N/A - instance variables are updated.
        """

        self._objects.pop(name, None)

    def add_world_forces(self, name: str, force: callable):
        """
        Add forces that act on all objects in the Inertial Frame. For example,
        gravity acts on all objects and, if -z is pointed towards the center of the
        Earth, than it will act on all objects as a constant force of [0., 0., -9.8].

        Args:
            name:   Human-readable name of the force.
            force:  Instantiated force in the world.

        Returns:
            N/A - instance variables are updated.
        """

        self._forces[name] = force

    def set_clock(self, clock_time: float):
        """
        This method allows the clock to be set/reset.

        Args:
            clock_time:     The time value the clock should have.

        Returns:
            N/A - instance variables are updated.
        """

        if clock_time >= 0.:
            self._clock = clock_time
        else:
            raise ValueError(f'The sim clock must be a non-negative float. A value of {clock_time} of type {type(clock_time)} was provided.')

    def increment_clock(self, **kwargs):
        """
        This method increments the internal sim clock by the timestep.

        Args:
            kwargs:     Ignored, this allows the method to be called from an event firing.

        Returns:
            N/A - instance variables are updated.
        """

        self._clock += self._timestep

    def add_event_function(self, event: str, name: str, function: callable):
        """
        This method adds a function to the list of functions executed when a given
        event fires.

        Args:
            event:      The event to be fired, i.e., pre_timestep, timestep, or
                        post_timestep.
            name:       Human-readable name/identifier of the function.
            function:   The function to be called when the event fires.

        Returns:
            N/A - instance variables are updated.
        """

        self._events[event].add_function(name=name, function=function)

    def remove_event_function(self, event: str, name: str):
        """
        This method removes a function from the list of functions executed when a
        given event fires.

        Args:
            event:      The event to be fired, i.e., pre_timestep, timestep, or
                        post_timestep.
            name:       Human-readable name/identifier of the function.
                        (Must already be in the list of events.)

        Returns:
            N/A - instance variables are updated.
        """

        self._events[event].remove_function(name=name)

    def event_fire(self, event: str, **kwargs):
        """
        For an event based simulation we have discrete events that happen during the sim.
        When the events happen the event is "fired" and therefore we call the fire method.

        This method allows us to call any events contained in the World object with any set
        of input args we desire.

        Args:
            event:      The event to be fired, i.e., pre_timestep, timestep, or
                        post_timestep.
            kwargs:     This allows any calling function to provide any input args the
                        event functions require.

        Returns:
            N/A - this method calls other functions.
        """

        self._events[event].fire(world=self, **kwargs)

    def fire_all_timestep_events(self, **kwargs):
        """
        This method is a simple convenience method for calling all the default timestep
        related methods in sequence.

        Args:
            **kwargs:   Input args to be passed to each set of events.

        Returns:
            N/A - this method calls other functions.
        """

        # Execute/Move Targets before the Towers.
        self._events['targets_pre_timestep'].fire(**kwargs)
        self._events['towers_pre_timestep'].fire(**kwargs)

        self._events['targets_timestep'].fire(**kwargs)
        self._events['towers_timestep'].fire(**kwargs)

        self._events['targets_post_timestep'].fire(**kwargs)
        self._events['towers_post_timestep'].fire(**kwargs)

    # Read-Only properties
    @property
    def inertial_frame(self) -> CartesianInertial:
        return self._inertial_frame

    @property
    def objects(self) -> dict:
        return self._objects

    @property
    def forces(self) -> dict:
        return self._forces

    @property
    def clutter(self) -> dict:
        return self._clutter

    @property
    def events(self) -> EventManager:
        return self._events

    @property
    def clock(self) -> float:
        return self._clock

    # Read-Write properties
    @property
    def timestep(self) -> [float, None]:
        return self._timestep

    @timestep.setter
    def timestep(self, value: float):
        if value > 0.:
            self._timestep = value
