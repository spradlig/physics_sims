"""
Module:
    <file_name_goes_here>.py

Description:
    <Short description, but thorough, of what is included in the file.>

Usage:
    <from some_module import some_function>
    <Provide a simple example for each class and function in the file.>

Notes:


References:


"""

"""
Version History:
    Original:
        GS | 28-Oct-22
"""

"""
TODOs:
    1)
"""

# Standard library imports
import numpy as np

# Tool imports


def deduplicate(haystack: str, needle: str):
    # From: https://stackoverflow.com/questions/42216559/fastest-way-to-deduplicate-contiguous-characters-in-string-python
    if haystack.find(needle * 2) != -1:
        return deduplicate(haystack.replace(needle * 2, needle), needle)

    return haystack


def formatted_line(info: str, tab_level: int = 1) -> str:

    tabs = tab_level * '\t'
    return f'{tabs}{info}\n'
