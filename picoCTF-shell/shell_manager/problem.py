"""
Problem migration operations for the shell manager.
"""

import json

from sys import stdin
from copy import deepcopy
from os.path import join
from re import findall

#More in-depth validation should occur with some sort of linting step.
PROBLEM_FIELDS = [
    ["author", {"required": True, "validation": str}],
    ["score", {"required": True, "validation": lambda score: type(score) == int and score >= 0}],
    ["name", {"required": True, "validation": str}],
    ["description", {"required": True, "validation": str}],
    ["categories", {"required": True, "validation": list}],
    ["tags", {"required": False, "validation": list}],
    ["hints", {"required": False, "validation": list}],
    ["organization", {"required": False, "validation": str}],
    ["pkg_description", {"required": False, "validation": str}],
    ["pkg_version", {"required": False, "validation": str}],
    ["pkg_name", {"required": False, "validation": str}],
    ["pkg_dependencies", {"required": False, "validation": str}],
]

PROBLEM_DEFAULTS = {
    "version": lambda problem: "1.0-0",
    "pkg_description": lambda problem: problem["description"],
    "pkg_dependencies": lambda problem: []
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
    }

    new_defaults = {
        "author": lambda problem: overrides.get("author", "Nihil"),
        "organization": lambda problem: overrides.get("organization", "")
    }

    def get_dependencies(problem_path):
        challenge_path = join(problem_path, "challenge.py")
        with open(challenge_path, "r") as challenge_file:
            challenge = challenge_file.read()
            requirements_index = challenge.find("local_requirements")
            requirements_bound = challenge.find("]", requirements_index)

            dependencies_text = challenge[requirements_index:requirements_bound]
            dependencies = findall(r"'([a-z0-9-\+\.]+)'\s*(?:,)?", dependencies_text)
            new_defaults["pkg_dependencies"] = lambda problem: dependencies

    get_dependencies(problem_path)
    translate_problem_fields(field_table, problem)
    set_problem_defaults(problem, additional_defaults=new_defaults)

    return problem

# Corresponds to possible migration formats.
MIGRATION_TABLE = {
    "cyberstakes2014": migrate_cs2014_problem
}

def migrate_problems(args):
    """ Main entrypoint for problem migration. """

    additional_defaults = {}
    for default_pair in args.set_defaults:
        if ":" in default_pair:
            field, value = default_pair.split(":")
            additional_defaults[field] = value

    for problem_path in args.problem_paths:
        problem = get_problem(problem_path)
        problem_copy = deepcopy(problem)

        print("Migrating '{}'...".format(problem_path))

        migrater = MIGRATION_TABLE[args.legacy_format]
        updated_problem = migrater(problem_path, problem_copy,
                                   overrides=additional_defaults)

        if args.dry:
            print(updated_problem)
        else:
            print("Updated '{}' to the new problem format.".format(updated_problem["name"]))
            set_problem(problem_path, updated_problem)
