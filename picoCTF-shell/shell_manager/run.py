#!/usr/bin/env python3

"""
Shell Manager -- Tools for deploying and packaging problems.
"""

from argparse import ArgumentParser

from shell_manager.package import problem_builder

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

    args = parser.parse_args()

    #Call the default function
    if "func" in args:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
