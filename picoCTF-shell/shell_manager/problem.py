"""
Problem migration operations for the shell manager.
"""

import json, os, logging

from sys import stdin
from copy import deepcopy
from os.path import join
from re import findall

from shell_manager.util import PROBLEM_ROOT, sanitize_name, get_problem_root, get_problem
from shell_manager.util import FatalException

logger = logging.getLogger(__name__)

PROBLEM_DEFAULTS = {
    "version": lambda problem: "1.0-0",
    "pkg_dependencies": lambda problem: [],
    "tags": lambda problem: [],
    "hints": lambda problem: [],
    "organization": "ctf"
}

def translate_problem_fields(translation_table, problem):
    """
    Migrate old problem fields to newer names through the translation table.

    Args:
        translation_table: dict with keys which specify old fields and values which correspond to the new ones.
        problem: the problem object.

    Example:
        Given a translation table of {"name": "display_name"}, the problem would change the "name" key to "display_name".
    """

    for old_field, new_field in translation_table.items():
        if old_field in problem:
            value = problem.pop(old_field)
            problem[new_field] = value

def set_problem_defaults(problem, additional_defaults={}):
    """
    Set the default fields for a given problem.

    Args:
        problem: the problem object.
        additional_defaults: use case specific defaults that should be included.
                             In the same form as defaults, {field: lambda problem: "default"}
    """

    total_defaults = deepcopy(PROBLEM_DEFAULTS)
    total_defaults.update(**additional_defaults)

    for field, setter in total_defaults.items():
        if field not in problem:
            #Use the associated default function
            problem[field] = setter(problem)

def set_problem(problem_path, problem):
    """
    Overwrite the problem.json of a given problem.

    Args:
        problem_path: path to the root of the problem's directory.
        problem: the problem object.
    """

    serialized_problem = json.dumps(problem, indent=True)
    json_path = join(problem_path, "problem.json")

    with open(json_path, "w") as problem_file:
        problem_file.write(serialized_problem)

def migrate_cs2014_problem(problem_path, problem, overrides={}):
    """
    Convert a Cyberstakes 2014 problem to the updated format.

    Args:
        problem_path: path to the root of the problem's directory.
        problem: the problem object to modify.

    Returns:
        A new problem object that is consistent with the current spec.
    """

    field_table = {
        "basescore": "score",
        "displayname": "name",
        "desc": "description",
        "categories": "category"
    }

    category_translations = {
        "binary": "Binary Exploitation",
        "crypto": "Cryptography",
        "web": "Web Exploitation",
        "forensics": "Forensics",
        "reversing": "Reverse Engineering",
        "tutorial": "Tutorial"
    }

    new_defaults = {
        "author": lambda problem: overrides.get("author", "Nihil"),
        "organization": lambda problem: overrides.get("organization", "ctf")
    }

    def get_dependencies(problem_path):
        """
        Retrieve problem dependencies from challenge.py

        Args:
            problem_path: path to the root of the problem's directory.
        """

        challenge_path = join(problem_path, "challenge.py")
        with open(challenge_path, "r") as challenge_file:
            challenge = challenge_file.read()
            dependencies = []
            for requirements in ["local_requirements", "remote_requirements"]:
                requirements_index = challenge.find(requirements)

                #Could not find it, we shouldn't do anything.
                if requirements_index == -1:
                    continue

                requirements_bound = challenge.find("]", requirements_index)

                dependencies_text = challenge[requirements_index:requirements_bound]
                dependencies.extend(findall(r"'([a-z0-9-\+\.]+)'\s*(?:,)?", dependencies_text))

            #Remove any duplicates
            dependencies = list(set(dependencies))

            new_defaults["pkg_dependencies"] = lambda problem: dependencies

    get_dependencies(problem_path)
    translate_problem_fields(field_table, problem)

    #Get the first, primary category.
    problem["category"] = problem["category"][0] if type(problem["category"]) == list else problem["category"]
    if problem["category"] in category_translations:
        problem["category"] = category_translations[problem["category"]]

    set_problem_defaults(problem, additional_defaults=new_defaults)

    return problem

# Corresponds to possible migration formats.
MIGRATION_TABLE = {
    "cyberstakes2014": migrate_cs2014_problem
}

def migrate_problems(args, config):
    """ Main entrypoint for problem migration. """

    additional_defaults = {}
    for default_pair in args.set_defaults:
        if ":" in default_pair:
            field, value = default_pair.split(":")
            additional_defaults[field] = value

    for problem_path in args.problem_paths:
        problem = get_problem(problem_path)
        problem_copy = deepcopy(problem)

        logger.debug("Migrating '%s' from legacy %s format.", problem["name"], args.legacy_format)

        migrater = MIGRATION_TABLE[args.legacy_format]
        updated_problem = migrater(problem_path, problem_copy,
                                   overrides=additional_defaults)

        if args.dry:
            print(updated_problem)
        else:
            logger.info("Updated '%s' to the new problem format.", problem["name"])
            set_problem(problem_path, updated_problem)
