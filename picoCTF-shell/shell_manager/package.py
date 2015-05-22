"""
Packaging operations for the shell manager.
"""

import json, re, gzip
import spur

from os import makedirs, listdir
from os.path import join, isdir

from copy import deepcopy

from shell_manager import problem_repo
from shell_manager.util import full_copy, move
from shell_manager.problem import get_problem

DEB_DEFAULTS = {
    "Section": "ctf",
    "Priority": "optional",
}

def problem_to_control(problem, control_path):
    """
    Convert problem.json to a deb control file.

    Args:
        problem: deserialized problem.json (dict)
        control_path: path to the DEBIAN directory
    """

    #a-z, digits 0-9, plus + and minus - signs, and periods
    package_name = problem.get("pkg_name", problem["name"])
    sanitized_name = re.sub(r"[^a-z0-9\+-\.]", "-", package_name.lower())

    control = deepcopy(DEB_DEFAULTS)
    control.update(**{
        "Package": sanitized_name,
        "Version": problem.get("version", "1.0-0"),
        "Architecture": problem.get("architecture", "all"),
        "Maintainer": problem["author"],
        "Depends": ",".join(problem.get("pkg_dependencies", [])),
        "Description": problem.get("pkg_description", problem["description"])
    })

    contents = ""
    for option, value in control.items():
        contents += "{}: {}\n".format(option, value)

    control_file = open(join(control_path, "control"), "w")
    control_file.write(contents)
    control_file.close()

def problem_builder(args):
    """
    Main entrypoint for package building operations.
    """

    problem_path = args.problem_paths.pop()
    problem = get_problem(problem_path)

    paths = {}
    paths["staging"] = join(problem_path, "staging")

    paths["control"] = join(paths["staging"], "DEBIAN")
    paths["data"] = join(paths["staging"], "problems", problem["name"])

    #Make all of the directories, order does not matter with makedirs
    [makedirs(staging_path) for _, staging_path in paths.items() if not isdir(staging_path)]

    full_copy(problem_path, paths["data"], ignore=["staging"])

    problem_to_control(problem, paths["control"])

    deb_directory = args.out if args.out is not None else paths["staging"]
    deb_path = join(deb_directory, problem["name"] + ".deb")

    shell = spur.LocalShell()
    result = shell.run(["fakeroot", "dpkg-deb", "--build", paths["staging"], deb_path])

    if result.return_code != 0:
        print("Error building problem deb for '{}'".format(problem["name"]))
        print(result.output)
    else:
        print("Problem '{}' packaged successfully.".format(problem["name"]))

    #Ensure repo exists
    if not isdir(args.repository):
        makedirs(args.repository)

    deb_package_path = join(paths["staging"], deb_path)

    if len(args.problem_paths) >= 1:
        #Copy the deb and process the rest of the problems
        move(deb_package_path, args.repository)
        return problem_builder(args)

    problem_repo.update(args.repository, [deb_package_path])
