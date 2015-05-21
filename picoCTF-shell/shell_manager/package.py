"""
Packaging operations for the shell manager.
"""

import json, re, gzip
import spur

from os import makedirs, listdir
from os.path import join, isdir

from shell_manager import problem_repo
from shell_manager.util import full_copy, move

def problem_to_control(problem, control_path):
    """
    Convert problem.json to a deb control file.

    Args:
        problem: deserialized problem.json (dict)
        control_path: path to the DEBIAN directory
    """

    #a-z, digits 0-9, plus + and minus - signs, and periods
    sanitized_name = re.sub(r"[^a-z0-9\+-\.]", "-", problem["name"].lower())

    control = {
        "Package": sanitized_name,
        "Version": problem.get("version", "1.0-0"),
        "Section": "ctf",
        "Priority": "optional",
        "Architecture": "all",
        "Maintainer": problem.get("author", "None"),
        "Description": problem.get("description", "No provided package description.")
    }

    contents = ""
    for option, value in control.items():
        contents += "{}: {}\n".format(option, value)

    control_file = open(join(control_path, "control"), "w")
    control_file.write(contents)
    control_file.close()

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
