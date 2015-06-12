"""
Various utility functions for the deployment API.
"""

import re, string

def get_attributes(obj):
    """
    Returns all attributes of an object, excluding those that start with
    an underscore

    Args:
        obj: the object

    Returns:
        A dictionary of attributes
    """

    return {key:getattr(obj, key) if not key.startswith("_") else None for key in dir(obj)}

def sanitize_name(name):
    """
    Sanitize a given name such that it conforms to unix policy.

    Args:
        name: the name to sanitize.

    Returns:
        The sanitized form of name.
    """

    if len(name) == 0:
        raise Exception("Can not sanitize an empty field.")

    sanitized_name = re.sub(r"[^a-z0-9\+-\.]", "-", name.lower())

    if sanitized_name[0] in string.digits:
        sanitized_name = "p" + sanitized_name

    return sanitized_name
