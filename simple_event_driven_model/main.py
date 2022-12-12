# -*- coding: utf-8 -*-
"""
Module:
    main.py

Description:
    Demonstration of an Event driven sim.

Usage:
    from main import sim

    ball1, ball2 = sim()

Notes:
    This sim holds all of its own configuration but a more complicated
    sim would use an Excel file style of configuration.

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
from sim_clock import SimClock
from state import State, Cartesian
from ballistic import Ballistic


def sim() -> tuple:
    # Define the clock
    clock = SimClock(timestep=0.01)
    max_time = 100.             # Maximum time the simulation will run to in seconds.

    # Define the initial conditions. This would normally come from the
    # Excel file as would timestep and max_time above.
    golf_ball_one = Ballistic(
        initial_state=State(
            position=Cartesian(
                x=0.,           # Position in m
                y=0.,
                z=15.
            ),
            velocity=Cartesian(
                x=10.,          # Velocity in m/s
                y=10.,
                z=1.
            ),
            acceleration=Cartesian(
                x=0.,
                y=0.,
                z=-9.8          # Gravity at 9.8 m/s^2
            ),
        )
    )

    golf_ball_two = Ballistic(
        initial_state=State(
            position=Cartesian(
                x=-100.,
                y=100.,
                z=100.
            ),
            velocity=Cartesian(
                x=-12.5,
                y=10.,
                z=0.
            ),
            acceleration=Cartesian(
                x=0.,
                y=0.,
                z=-9.8
            ),
        )
    )

    # Define the model and it's connections.
    clock.add_function_to_timestep(
        name='golf_ball_one', function=golf_ball_one.dynamics
    )
    clock.add_function_to_timestep(
        name='golf_ball_two', function=golf_ball_two.dynamics
    )

    while clock.time <= max_time and (golf_ball_one.state.position.z >= 0 and golf_ball_two.state.position.z >= 0):
        clock.execute_timestep()

    return golf_ball_one, golf_ball_two
