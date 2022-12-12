# Simple Event Driven Model
This model was built as a demonstration of how to model physical systems for people unfamiliar with python, classes, 
and event driven code. Understand that this demonstration was built for engineers not software people and the event 
architecture is not your common pub/sub style events.

## Running the Model
The following is all you need in order to run the model:

    from main import sim
    ball1, ball2 = sim()

The outputs, ball1 and ball2, are golf balls (instantiated Ballistic objects) whose motions were simulated. Their states
at each timestep in the simulation can be accessed through the `states` property. The `states` property outputs a Pandas
DataFrame with each column labelled. The columns are:

   `Index(
      [
         'Position x [m]', 'Position y [m]', 'Position z [m]',
         'Velocity x [m/s]', 'Velocity y [m/s]', 'Velocity z [m/s]',
         'Acceleration x [m/s^2]', 'Acceleration y [m/s^2]', 'Acceleration z [m/s^2]'
      ],
      dtype='object'
   )`

The simulation time is under the column heading `Time[sec]`, it doesn't show up in the list above because it is the 
index of the DataFrame. 

## Basics of the Architecture
This is a simple demonstration to newbies of python. As such, the code is organized for ease of learning to code not
for robustness, speed, good coding practice, etc. The organization is as follows:
 - main.py | sim: The sim function instantiates a SimClock and 2 Ballistic objects. It defines a max simulation time and a while loop that exits at the max time or when the an object reaches an altitude of 0.
 - sim_clock.py | SimClock: The simulation is run from a clock and the SimClock class is that clock. At each timestep the execute_timestep event is executed (this event is called from the while loop in main.py).
 - ballistic.py | Ballistic: This class defines your basic Physics 101 Ballistic (or Projectile) Motion. A state for the object is maintained and the only force acting on the object is gravity.
 - state.py | 
   - State: This class takes in position, velocity, and acceleration as input arg at instantiation. Each input arg is provided a Coordinate frame triplet. In this case, only a Cartesian [x, y, z] coordinate frame has been defined.
   - Cartesian: This class defines the Cartesian coordinate frame [x, y, z] triplet and provides some additional methods around simple vector arithmetic.

For this demonstration, the events are all contained in the SimClock class which only has 1 event - execute_timestep.
Other reasonable architectures might include events in the SimClock and Ballistic classes. Or a pub/sub architecture 
using something like Redis. (Note that I've primarily worked in Aerospace and things like Redis get blocked by IT.)

Adding events to both SimClock and Ballistic classes is unnecessary for this simulation. However, in a more complex 
simulation it can make sense. I once wrote a simulation for 1D fluid dynamics where the state of each component in the 
system was dependent on the fluid state at the outlet of the component immediately upstream. In this instance, every 
component got an event manager and each component was linked via the outlet events. Again, a pub/sub architecture might
have been a better choice but it wasn't really an option without building it myself.
