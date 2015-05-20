#!/usr/bin/env python3

"""
Shell Manager -- Tools for deploying and packaging problems.
"""

from argparse import ArgumentParser

from os.path import join, isdir
from os import makedirs, listdir, getcwd

from functools import reduce
from shutil import copytree, copy2, ignore_patterns, move

import re
import gzip
import spur
import json
import tarfile

def problem_to_control(problem, control_path):

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

def problem_package_builder(args):

    problem_path = args.problem_paths.pop()

    problem = json.loads(open(join(problem_path, "problem.json"), "r").read())

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
        #Copy the deb
        move(deb_package_path, args.repository)
        problem_package_builder(args)
    else:
        update_problem_repo(args.repository, [deb_package_path])

def update_problem_repo(repo_path, deb_paths):
    [copy2(deb_path, repo_path) for deb_path in deb_paths]

    shell = spur.LocalShell()
    result = shell.run(["dpkg-scanpackages", ".", "/dev/null"], cwd=repo_path)

    packages_path = join(repo_path, "Packages.gz")
    with gzip.open(packages_path, "wb") as packages:
        packages.write(result.output)

    print("Updated problem repository.")

def main():
    parser = ArgumentParser(description="Shell Manager")
    subparsers = parser.add_subparsers(help="package problem for distribution")

    problem_package_parser = subparsers.add_parser("package", help="problem package management")

    #build_subparser = problem_packager_parser.add_subparsers(help="build deb package from problem source")

    #problem_package_build_parser = build_subparser.add_parser("build")
    problem_package_parser.add_argument("-r", "--repository", default="/usr/local/ctf-packages",
                                              help="Location of problem repository.")
    problem_package_parser.add_argument("-o", "--out", help="folder to store problem package.")
    problem_package_parser.add_argument("problem_paths", nargs="+", type=str, help="paths to problems.")
    problem_package_parser.set_defaults(func=problem_package_builder)

    args = parser.parse_args()

    #Call the default function
    if "func" in args:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
