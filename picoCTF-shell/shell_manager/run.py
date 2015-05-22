#!/usr/bin/env python3

"""
Shell Manager -- Tools for deploying and packaging problems.
"""

from argparse import ArgumentParser

from shell_manager.package import problem_builder
from shell_manager.problem import migrate_problems

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
    problem_package_parser.set_defaults(func=problem_builder)

    migration_parser = subparsers.add_parser("migrate", help="migrate legacy problem formats")

    migration_parser.add_argument("-i", "--interactive", action="store_true", help="update problem fields interactively")
    migration_parser.add_argument("-d", "--dry", action="store_true", help="don't make persistent changes.")
    migration_parser.add_argument("-l", "--legacy-format", default="cyberstakes2014", choices=["cyberstakes2014"],
                                  help="what format the problems are currently in.")
    migration_parser.add_argument("-s", "--set-defaults", type=str, action="append",
                                  default=[], help="field:value used to override new defaults.")
    migration_parser.add_argument("problem_paths", nargs="+", type=str, help="paths to problems.")
    migration_parser.set_defaults(func=migrate_problems)
    args = parser.parse_args()

    #Call the default function
    if "func" in args:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
