# -*- coding: utf-8 -*-
"""
Module:
    event.py

Description:
    This file holds the Event and EventManager classes used to create an
    event driven framework.

Usage:
    from simple_event_driven_model.event import EventManager, Event

    manager = EventManager(timestep=Event('timestep'))

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
import numpy as np  # We only use np for numpy because it is what every tutorial (and therefore
# almost everyone) uses.
import pandas as pd
import scipy  # We don't use an as here because most people use scipy not some abbreviation.


# Custom Package Imports


class Event:
    """
    A class to manage a single Event.
    """

    def __init__(self, name: str):
        """
        Instantiate the class

        Args:
            name:           A descriptive name for the Event.
        """

        self.name = name
        self._functions = {}

        self.__iteration_counter = 0

    def __repr__(self):
        # This function defines the display when we type an instantiated class
        # instance into Spyder or iPython.
        return self.__str__()

    def __str__(self):
        # This function defines the display when we type an instantiated class
        # instance into Spyder or iPython.
        output = '\tEvent {0}:\n'.format(self.name)
        for function in self.functions:
            output += '\t\t{0}\n'.format(function)

        return output

    def __iter__(self):
        # This is part of what allows us to use this class in a loop like we
        # would a list.
        self.__iteration_counter = 0
        return self

    def __next__(self):
        # This is the other part that allows us to use this class in a loop like
        # we would a list.
        try:
            function = self.functions[self.__iteration_counter]
            self.__iteration_counter += 1
            return self._functions[function]
        except IndexError:
            raise StopIteration

    def add_function(self, name: str, function: callable):
        """
        Add a function from the list of functions to execute when the
        event is triggered (fired).

        Args:
            name:       A descriptive name for the function.
            function:   The function to be executed.

        Returns:
            N/A
        """

        self._functions[name] = function

    def remove_function(self, name: str):
        """
        Remove a function from the list of functions to execute when the
        event is triggered (fired).

        Args:
            name:       A descriptive name for the function.

        Returns:
            N/A - except if the function's name is not in the _functions
            dict then this method will raise an AttributeError.
        """

        try:
            _ = self._functions.pop(name)
        except KeyError:
            raise AttributeError('{0} is not an function in this event.'.format(name))

    def fire(self, **kwargs):
        """
        This is the heart of any event driven architecture. This
        executes the events.

        Args:
            **kwargs:   This class is a generic handler for events as
                        such it needs to handle whatever set of input
                        arguments any event may need. So we use
                        **kwargs.

        Example:
        def execute(**kwargs):
            for event in [lambda a, b: a**b, lambda a, b: a+b]:
                print(event(**kwargs))

        execute(a=2, b=3)
        -> 8
        -> 5

        This won't work.
        execute(2, 3)

        Returns:

        """

        # We could speed this up by making it multi-threaded because no
        # events should rely on the output/outcome of another event.
        for function in self:
            function(**kwargs)

    @property
    def functions(self) -> list:
        return list(self._functions.keys())


class EventManager:
    """
    A class to manage multiple Events. This class doesn't have an iterator or
    execution because there is no use-case for wanting to fire every Event
    indiscriminately.
    """

    def __init__(self, **kwargs):
        """

        Args:
            **kwargs:   This allows for the EventManager to be instantiated
                        with a named set of Event objects.
        """

        self._events = {}

        for k, v in kwargs.items():
            self._events[k] = v

        self.lock = False

    def __repr__(self):
        # This function defines the display when we type an instantiated class
        # instance into Spyder or iPython.
        return self.__str__()

    def __str__(self):
        # This function defines the display when we type an instantiated class
        # instance into Spyder or iPython.
        output = '\tEvents:\n'
        for event in self.events:
            output += '\t\t{0}\n'.format(event)

        return output

    def __getitem__(self, key: str):
        # Allow access via class_name['property'] as well as class_name.property.
        # https://stackoverflow.com/questions/11469025/how-to-implement-a-subscriptable-class-in-python-subscriptable-class-not-subsc
        if key in self.events:
            return self._events[key]
        else:
            raise AttributeError('{0} is not an event.'.format(key))

    def __setitem__(self, key: str, value):
        # Allows for setting an instance property via class_name['property'] = value
        # as well as class_name.property = value.
        if self.lock is False:
            self._events[key] = value

    def add_event(self, name: str, event: Event):
        """
        Add an event to the list of events.

        Args:
            name:       A descriptive name for the event.
            event:      An instantiated Event class.

        Returns:
            N/A
        """

        self._events[name] = event

    def remove_event(self, name: str):
        """
        Remove an event from the list.

        Args:
            name:       A descriptive name for the event.

        Returns:
            N/A
        """

        try:
            _ = self._events.pop(name, None)
        except KeyError:
            raise AttributeError('{0} is not an event.'.format(name))

    @property
    def events(self) -> list:
        return list(self._events.keys())

    @property
    def lock(self) -> bool:
        return self.__lock

    @lock.setter
    def lock(self, value: bool):
        self.__lock = value
