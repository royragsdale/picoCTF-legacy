"""
Bundling operation for the shell manager. A special case of packaging.
"""

from os import getcwd, makedirs
from os.path import join, isdir

from shell_manager.problem import get_problem
from shell_manager.package import get_problem_root, DEB_DEFAULTS
from shell_manager.package import sanitize_name

def bundle_problems(args, config):
    for package_name in args.package_names:
        installed_path = get_problem_root(package_name, absolute=True)
        if not isdir(installed_path) or not get_problem(installed_path):
            raise Exception("'{}' is not an installed problem.".format(package_name))

    paths = {"working": getcwd() if args.out is None else args.out}
    paths["staging"] = join(paths["working"], "__staging")
    paths["debian"] = join(paths["staging"], "DEBIAN")

    [makedirs(staging_path) for _, staging_path in paths.items() if not isdir(staging_path)]

