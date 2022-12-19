"""
Module:
    main.py

Description:
    This file is an example of running

Usage:
    <from some_module import some_function>
    <Provide a simple example for each class and function in the file.>

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
        Gabe Spradlin | 13-Dec-2022
"""

"""
TODOs:
    1)
"""

# Standard library imports


# Tool imports
import configs
import env


def sim(config_file: [str, None] = None):
    """

    Args:
        config_file:

    Returns:

    """

    config = configs.fetch(file_name=config_file)

    world = env.World(world_config=config['world'])

    # Attach Targets to World.
    for target_name, target_dict in config['targets'].items():
        pass

    # Attach Towers to World.
    for tower_name, tower_dict in config['towers'].items():
        pass