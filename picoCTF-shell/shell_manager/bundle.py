"""
Bundling operation for the shell manager. A special case of packaging.
"""

import json, spur

from os import getcwd, makedirs
from os.path import join, isdir

from shutil import rmtree

from copy import deepcopy

from shell_manager.problem import get_problem
from shell_manager.package import get_problem_root, DEB_DEFAULTS
from shell_manager.package import sanitize_name

def bundle_to_control(bundle, debian_path):
    """
    Create a deb control file for a bundle.

    Args:
        bundle: the bundle object.
        debian_path: path to the DEBIAN directory
    """

    control = deepcopy(DEB_DEFAULTS)
    control.update(**{
        "Package": sanitize_name(bundle["name"]),
        "Version": bundle.get("version", "1.0-0"),
        "Architecture": bundle.get("architecture", "all"),
        "Maintainer": bundle["author"],
        "Description": bundle["description"]
    })

    control["Depends"] = ", ".join(bundle["problems"])

    contents = ""
    for option, value in control.items():
        contents += "{}: {}\n".format(option, value)

    control_file = open(join(debian_path, "control"), "w")
    control_file.write(contents)
    control_file.close()

def get_bundle(bundle_path):
    """
    Retrieve a bundle spec from a given bundle directory.

    Args:
        bundle_path: path to the root of the bundle directory.

    Returns:
        A bundle object.
    """

    bundle = json.loads(open(bundle_path, "r").read())

    return bundle

def bundle_problems(args, config):
    """
    Main entrypoint for generating problem bundles.
    """

    bundle = get_bundle(args.bundle_path)

    for problem_name in bundle["problems"]:
        installed_path = get_problem_root(problem_name, absolute=True)
        if not isdir(installed_path) or not get_problem(installed_path):
            raise Exception("'{}' is not an installed problem.".format(problem_name))

    paths = {"working": getcwd() if args.out is None else args.out}
    paths["staging"] = join(paths["working"], "__staging")
    paths["debian"] = join(paths["staging"], "DEBIAN")

    [makedirs(staging_path) for _, staging_path in paths.items() if not isdir(staging_path)]

    bundle_to_control(bundle, paths["debian"])

    def format_deb_file_name(bundle):
        """
        Prepare the file name of the deb package according to deb policy.

        Args:
            bundle: the bundle object

        Returns:
           An acceptable file name for the bundle.
        """

        raw_package_name = "{}-{}-bundle-{}.deb".format(
            bundle.get("organization", "ctf"),
            bundle["name"],
            bundle.get("version", "1.0-0")
        )

        return sanitize_name(raw_package_name)

    deb_path = join(paths["working"], format_deb_file_name(bundle))

    shell = spur.LocalShell()
    result = shell.run(["fakeroot", "dpkg-deb", "--build", paths["staging"], deb_path])

    if result.return_code != 0:
        print("Error building bundle deb for '{}'".format(bundle["name"]))
        print(result.output)
    else:
        print("Bundle '{}' packaged successfully.".format(bundle["name"]))

    print("Cleaning up staging directory '{}'.".format(paths["staging"]))

    rmtree(paths["staging"])
