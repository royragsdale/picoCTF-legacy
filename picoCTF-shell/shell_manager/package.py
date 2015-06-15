"""
Packaging operations for the shell manager.
"""

import json, re, gzip
import spur

from os import makedirs, listdir, getcwd, chmod
from os.path import join, isdir

from copy import deepcopy

from shell_manager.util import full_copy, move
from shell_manager.problem import get_problem

DEB_DEFAULTS = {
    "Section": "ctf",
    "Priority": "optional",
}

def sanitize_package_text(name):
    """
    Sanitize a given name such that it conforms to deb policy.

    Args:
        name: the name to sanitize.

    Returns:
        The sanitized form of name.
    """

    sanitized_name = re.sub(r"[^a-z0-9\+-\.]", "-", name.lower())
    return sanitized_name

def problem_to_control(problem, debian_path):
    """
    Convert problem.json to a deb control file.

    Args:
        problem: deserialized problem.json (dict)
        debian_path: path to the DEBIAN directory
    """

    #a-z, digits 0-9, plus + and minus - signs, and periods
    package_name = problem.get("pkg_name", problem["name"])
    sanitized_name = sanitize_package_text(package_name)
    control = deepcopy(DEB_DEFAULTS)
    control.update(**{
        "Package": sanitized_name,
        "Version": problem.get("version", "1.0-0"),
        "Architecture": problem.get("architecture", "all"),
        "Maintainer": problem["author"],
        "Description": problem.get("pkg_description", problem["description"])
    })

    if "pkg_dependencies" in problem:
        control["Depends"] = ", ".join(problem.get("pkg_dependencies", []))

    contents = ""
    for option, value in control.items():
        contents += "{}: {}\n".format(option, value)

    control_file = open(join(debian_path, "control"), "w")
    control_file.write(contents)
    control_file.close()

def postinst_dependencies(problem, problem_path, debian_path):
    """
    Handles the generation of the postinst script for additional dependencies.

    Args:
    """

    postinst = join(paths["debian"], "postinst")
    with open(postinst, "w") as f:
        chmod(postinst, 0o775)

def problem_builder(args):
    """
    Main entrypoint for package building operations.
    """

    problem_path = args.problem_paths.pop()
    problem = get_problem(problem_path)

    paths = {}
    paths["staging"] = join(problem_path, "staging")

    paths["debian"] = join(paths["staging"], "DEBIAN")
    paths["data"] = join(paths["staging"], "problems", problem["name"])

    #Make all of the directories, order does not matter with makedirs
    [makedirs(staging_path) for _, staging_path in paths.items() if not isdir(staging_path)]

    full_copy(problem_path, paths["data"], ignore=["staging"])

    problem_to_control(problem, paths["debian"])

    deb_directory = args.out if args.out is not None else getcwd()

    def format_deb_file_name(problem):
        """
        Prepare the file name of the deb package according to deb policy.

        Args:
            problem: the problem object

        Returns:
           An acceptable file name for the problem.
        """

        raw_package_name = "{}-{}-{}.deb".format(
            problem.get("organization", "ctf"),
            problem.get("pkg_name", problem["name"]),
            problem.get("version", "1.0-0")
        )

        return sanitize_package_text(raw_package_name)

    deb_path = join(deb_directory, format_deb_file_name(problem))

    shell = spur.LocalShell()
    result = shell.run(["fakeroot", "dpkg-deb", "--build", paths["staging"], deb_path])

    if result.return_code != 0:
        print("Error building problem deb for '{}'".format(problem["name"]))
        print(result.output)
    else:
        print("Problem '{}' packaged successfully.".format(problem["name"]))

    if len(args.problem_paths) >= 1:
        return problem_builder(args)

def bundle_problems(args):
    pass
