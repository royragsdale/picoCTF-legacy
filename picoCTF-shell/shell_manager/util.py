"""
Common utilities for the shell manager.
"""

from os import listdir, unlink, sep
from os.path import join, isdir, isfile

import shutil
import json
import re, string
from shutil import copytree, copy2

# the root of the hacksports local store
HACKSPORTS_ROOT = "/opt/hacksports/"
PROBLEM_ROOT = join(HACKSPORTS_ROOT, "sources")
STAGING_ROOT = join(HACKSPORTS_ROOT, "staging")
DEPLOYED_ROOT = join(HACKSPORTS_ROOT, "deployed")
BUNDLE_ROOT = join(HACKSPORTS_ROOT, "bundles")


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

#I will never understand why the shutil functions act
#the way they do...

def full_copy(source, destination, ignore=[]):
    for f in listdir(source):
        if f in ignore:
            continue
        source_item = join(source, f)
        destination_item = join(destination, f)

        if isdir(source_item):
            if not isdir(destination_item):
                copytree(source_item, destination_item)
        else:
            copy2(source_item, destination_item)

def move(source, destination, clobber=True):
    if sep in source:
        file_name = source.split(sep)[-1]
    else:
        file_name = source

    new_path = join(destination, file_name)
    if clobber and isfile(new_path):
        unlink(new_path)

    shutil.move(source, destination)


def get_problem_root(problem_name, absolute=False):
    """
    Installation location for a given problem.

    Args:
        problem_name: the problem name.
        absolute: should return an absolute path.

    Returns:
        The tentative installation location.
    """

    problem_root = join(PROBLEM_ROOT, sanitize_name(problem_name))

    assert problem_root.startswith(os.sep)
    if absolute:
        return problem_root

    return problem_root[len(os.sep):]

def get_problem(problem_path):
    """
    Retrieve a problem spec from a given problem directory.

    Args:
        problem_path: path to the root of the problem directory.

    Returns:
        A problem object.
    """

    json_path = join(problem_path, "problem.json")
    problem = json.loads(open(json_path, "r").read())

    return problem

def get_bundle_root(bundle_name, absolute=False):
    """
    Installation location for a given bundle.

    Args:
        bundle_name: the bundle name.
        absolute: should return an absolute path.

    Returns:
        The tentative installation location.
    """

    bundle_root = join(BUNDLE_ROOT, sanitize_name(bundle_name))

    assert bundle_root.startswith(os.sep)
    if absolute:
        return bundle_root

    return bundle_root[len(os.sep):]

def get_bundle(bundle_path):
    """
    Retrieve a bundle spec from a given bundle directory.

    Args:
        bundle_path: path to the root of the bundle directory.

    Returns:
        A bundle object.
    """

    bundle = json.loads(open(join(bundle_path, "bundle.json"), "r").read())

    return bundle
