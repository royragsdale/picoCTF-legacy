"""
Problem migration operations for the shell manager.
"""

import json

from sys import stdin

from shell_manager.package import get_problem


PROBLEM_DEFAULTS = [
    ["version", lambda problem: "1.0-0"],
    ["pkg_description", lambda problem: problem["description"]],
    ["pkg_version", lambda problem: problem["version"]]
]

def migrate_problems(args):
    for problem_path in args.problem_paths:
        problem = get_problem(problem_path)
        print(problem, args.legacy_format)
