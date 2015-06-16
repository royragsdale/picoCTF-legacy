"""
Packaging operations for the shell manager.
"""

import json, re, gzip
import spur, os

from os import makedirs, listdir, getcwd, chmod
from os.path import join, isdir, isfile

from shutil import copy, rmtree

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

def get_problem_root(problem, absolute=False):
    """
    Installation location for a given problem.

    Args:
        problem: the problem object.
        absolute: should return an absolute path.

    Returns:
        The tentative installation location.
    """

    problem_root = join("opt", "hacksports", "sources", sanitize_package_text(problem["name"]))

    if absolute:
        return join(os.sep, problem_root)

    return problem_root

def postinst_dependencies(problem, problem_path, debian_path, install_path):
    """
    Handles the generation of the postinst script for additional dependencies.

    Args:
        problem: the problem object.
        problem_path: the problem directory.
        debian_path: the deb's DEBIAN directory.
    """

    postinst_template = ["#!/bin/bash"]

    requirements_path = join(problem_path, "requirements.txt")
    dependencies_path = join(problem_path, "install_dependencies")

    staging_requirements_path = join(install_path, "requirements.txt")

    deployed_requirements_path = join(get_problem_root(problem, absolute=True),
                                      "__files", "requirements.txt")
    deployed_setup_path = join(get_problem_root(problem, absolute=True),
                               "__files", "install_dependencies")

    listed_requirements = problem.get("pip_requirements", [])

    #Write or copy the requirements to the staging directory.
    if len(listed_requirements) > 0:
        if isfile(requirements_path):
            raise Exception("Problem has both a pip_requirements field and requirements.txt.")

        with open(staging_requirements_path, "w") as f:
            f.writelines(listed_requirements)
    elif isfile(requirements_path):
        copy(requirements_path, staging_requirements_path)

    if isfile(staging_requirements_path):
        postinst_template.append("pip3 install -r {}".format(deployed_requirements_path))

    if isfile(dependencies_path):
        copy(dependencies_path, join(install_path, "install_dependencies"))

        #Ensure it is executable
        chmod(join(install_path, "install_dependencies"), 0o500)

        postinst_template.append("bash -c '{}'".format(deployed_setup_path))

    postinst_path = join(debian_path, "postinst")
    with open(postinst_path, "w") as f:
        chmod(postinst_path, 0o775)
        contents = "\n".join(postinst_template)
        f.write(contents)

def problem_builder(args):
    """
    Main entrypoint for package building operations.
    """

    problem_path = args.problem_paths.pop()
    problem = get_problem(problem_path)

    paths = {}
    paths["staging"] = join(problem_path, "__staging")

    paths["debian"] = join(paths["staging"], "DEBIAN")
    paths["data"] = join(paths["staging"], get_problem_root(problem))
    paths["install_data"] = join(paths["data"], "__files")

    #Make all of the directories, order does not matter with makedirs
    [makedirs(staging_path) for _, staging_path in paths.items() if not isdir(staging_path)]

    full_copy(problem_path, paths["data"], ignore=["__staging"])

    problem_to_control(problem, paths["debian"])

    postinst_dependencies(problem, problem_path,
                          paths["debian"], paths["install_data"])

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

    print("Cleaning up staging directory '{}'.".format(paths["staging"]))
    rmtree(paths["staging"])

    if len(args.problem_paths) >= 1:
        return problem_builder(args)

def bundle_problems(args):
    pass
