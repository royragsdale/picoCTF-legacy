#!/usr/bin/env python3

"""
Shell Manager -- Tools for deploying and packaging problems.
"""

from argparse import ArgumentParser

from shell_manager.package import problem_builder
from shell_manager.bundle import bundle_problems
from shell_manager.problem import migrate_problems
from shell_manager.problem_repo import update_repo
from shell_manager.util import HACKSPORTS_ROOT
from hacksport.deploy import deploy_problems
from hacksport.status import clean, status, publish

from os.path import join
from os import sep

from imp import load_source

def main():
    parser = ArgumentParser(description="Shell Manager")
    subparsers = parser.add_subparsers(help="package problem for distribution")

    problem_package_parser = subparsers.add_parser("package", help="problem package management")
    problem_package_parser.add_argument("-o", "--out", help="folder to store problem package.")
    problem_package_parser.add_argument("-i", "--ignore", dest="ignore", default=[], action="append", help="list of files to ignore adding to the deb")
    problem_package_parser.add_argument("problem_paths", nargs="*", type=str, help="paths to problems.")
    problem_package_parser.set_defaults(func=problem_builder)

    publish_repo_parser = subparsers.add_parser("publish_repo", help="publish packaged problems")
    publish_repo_parser.add_argument("-r", "--repository", default="/usr/local/ctf-packages",
                                              help="Location of problem repository.")
    publish_repo_parser.add_argument("repo_type", choices=["local", "remote"])
    publish_repo_parser.add_argument("package_paths", nargs="+", type=str, help="problem packages to publish.")
    publish_repo_parser.set_defaults(func=update_repo)

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
    deploy_parser.add_argument("-D", "--deployment-directory", type=str, default=None, help="the directory to deploy to")
    deploy_parser.add_argument("-b", "--bundle", action="store_true", help="specify a bundle of problems to deploy.")
    deploy_parser.add_argument("problem_paths", nargs="*", type=str, help="paths to problems.")
    deploy_parser.set_defaults(func=deploy_problems)

    clean_parser = subparsers.add_parser("clean", help="Clean up the intermediate staging data stored during deployments")
    clean_parser.set_defaults(func=clean)

    status_parser = subparsers.add_parser("status", help="List the installed problems and bundles and any instances associated with them.")
    status_parser.add_argument("-a", "--all", action="store_true", help="Show information about all problem instanes.")
    status_parser.add_argument("-p", "--problem", type=str, default=None, help="Display status information for a given problem.")
    status_parser.add_argument("-b", "--bundle", type=str, default=None, help="Display status information for a given bundle.")
    status_parser.add_argument("-j", "--json", action="store_true", default=None, help="Display status information in json format")
    status_parser.set_defaults(func=status)

    publish_parser = subparsers.add_parser("publish", help="Generate the information needed by the web server for this deployment.")
    publish_parser.set_defaults(func=publish)

    args = parser.parse_args()

    config = load_source("config", join(HACKSPORTS_ROOT, "config.py"))

    #Call the default function
    if "func" in args:
        args.func(args, config)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
