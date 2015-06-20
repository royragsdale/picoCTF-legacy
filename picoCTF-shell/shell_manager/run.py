#!/usr/bin/env python3

"""
Shell Manager -- Tools for deploying and packaging problems.
"""

from argparse import ArgumentParser

from shell_manager.package import problem_builder
from shell_manager.bundle import bundle_problems
from shell_manager.problem import migrate_problems
from shell_manager.problem_repo import update_repo
from hacksport.deploy import deploy_problems

from os.path import join
from os import sep

from imp import load_source

def main():
    parser = ArgumentParser(description="Shell Manager")
    subparsers = parser.add_subparsers(help="package problem for distribution")

    problem_package_parser = subparsers.add_parser("package", help="problem package management")
    problem_package_parser.add_argument("-o", "--out", help="folder to store problem package.")
    problem_package_parser.add_argument("problem_paths", nargs="*", type=str, help="paths to problems.")
    problem_package_parser.set_defaults(func=problem_builder)

    publish_parser = subparsers.add_parser("publish", help="publish packaged problems")
    publish_parser.add_argument("-r", "--repository", default="/usr/local/ctf-packages",
                                              help="Location of problem repository.")
    publish_parser.add_argument("repo_type", choices=["local", "remote"])
    publish_parser.add_argument("package_paths", nargs="+", type=str, help="problem packages to publish.")
    publish_parser.set_defaults(func=update_repo)

    migration_parser = subparsers.add_parser("migrate", help="migrate legacy problem formats")
    migration_parser.add_argument("-i", "--interactive", action="store_true", help="update problem fields interactively")
    migration_parser.add_argument("-d", "--dry", action="store_true", help="don't make persistent changes.")
    migration_parser.add_argument("-l", "--legacy-format", default="cyberstakes2014", choices=["cyberstakes2014"],
                                  help="what format the problems are currently in.")
    migration_parser.add_argument("-s", "--set-defaults", type=str, action="append",
                                  default=[], help="field:value used to override new defaults.")
    migration_parser.add_argument("problem_paths", nargs="+", type=str, help="paths to problems.")
    migration_parser.set_defaults(func=migrate_problems)

    bundle_parser = subparsers.add_parser("bundle", help="create a bundle of problems")
    bundle_parser.add_argument("bundle_path", type=str, help="the name of the bundle.")
    bundle_parser.add_argument("-o", "--out", type=str, help="folder to store the bundle.")
    bundle_parser.set_defaults(func=bundle_problems)

    deploy_parser = subparsers.add_parser("deploy", help="problem deployment")
    deploy_parser.add_argument("-n", "--num-instances", type=int, default=1, help="number of instances to generate.")
    deploy_parser.add_argument("-d", "--dry", action="store_true", help="don't make persistent changes.")
    deploy_parser.add_argument("-b", "--bundle", action="store_true", help="specify a bundle of problems to deploy.")
    deploy_parser.add_argument("problem_paths", nargs="*", type=str, help="paths to problems.")
    deploy_parser.set_defaults(func=deploy_problems)

    args = parser.parse_args()

    config = load_source("config", join(sep, "opt", "hacksports", "config.py"))

    #Call the default function
    if "func" in args:
        args.func(args, config)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
