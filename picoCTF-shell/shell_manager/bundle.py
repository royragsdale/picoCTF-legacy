"""
Bundling operation for the shell manager. A special case of packaging.
"""

import json, spur
import copy as object_copy

import os
from os import getcwd, makedirs, chmod
from os.path import join, isdir, basename, dirname

from shutil import rmtree, copyfile

from shell_manager.package import DEB_DEFAULTS
from shell_manager.util import BUNDLE_ROOT, sanitize_name, get_problem, get_problem_root, get_bundle, get_bundle_root

def bundle_to_control(bundle, debian_path):
    """
    Create a deb control file for a bundle.

    Args:
        bundle: the bundle object.
        debian_path: path to the DEBIAN directory
    """

    control = object_copy.deepcopy(DEB_DEFAULTS)
    control.update(**{
        "Package": sanitize_name(bundle["name"]),
        "Version": bundle.get("version", "1.0-0"),
        "Architecture": bundle.get("architecture", "all"),
        "Maintainer": bundle["author"],
        "Description": bundle["description"]
    })

    # Need to install problems and bundle dependencies.
    pkg_dependencies = bundle["problems"] + bundle.get("pkg_dependencies", [])
    control["Depends"] = ", ".join(pkg_dependencies)

    contents = ""
    for option, value in control.items():
        contents += "{}: {}\n".format(option, value)

    control_file = open(join(debian_path, "control"), "w")
    control_file.write(contents)
    control_file.close()

def bundle_problems(args, config):
    """
    Main entrypoint for generating problem bundles.
    """

    bundle_path = args.bundle_path
    if os.path.isdir(args.bundle_path):
        bundle = get_bundle(args.bundle_path)
        bundle_path = join(args.bundle_path, "bundle.json")
    elif os.path.isfile(args.bundle_path):
        bundle = json.loads(open(args.bundle_path).read())
    else:
        raise Exception("No bundle {}".format(args.bundle_path))

    for problem_name in bundle["problems"]:
        installed_path = get_problem_root(problem_name, absolute=True)
        if not isdir(installed_path) or not get_problem(installed_path):
            raise Exception("'{}' is not an installed problem.".format(problem_name))

    paths = {"working": getcwd() if args.out is None else args.out}

    if args.staging_dir:
        paths["staging"] = join(args.staging_dir, "__staging")
    else:
        paths["staging"] = join(paths["working"], "__staging")

    paths["debian"] = join(paths["staging"], "DEBIAN")
    paths["bundle_root"] = join(paths["staging"], get_bundle_root(bundle["name"]))

    [makedirs(staging_path) for _, staging_path in paths.items() if not isdir(staging_path)]

    # note that this chmod does not work correct if on a vagrant shared folder,
    # so we need to package the problems elsewhere
    chmod(dirname(paths["bundle_root"]), 0o750)

    bundle_to_control(bundle, paths["debian"])

    copied_bundle_path = join(paths["bundle_root"], "bundle.json")
    copyfile(bundle_path, copied_bundle_path)

    def format_deb_file_name(bundle):
        """
        Prepare the file name of the deb package according to deb policy.

        Args:
            bundle: the bundle object

        Returns:
           An acceptable file name for the bundle.
        """

        raw_package_name = "{}-{}-bundle-{}.deb".format(
            sanitize_name(bundle.get("organization", "ctf")),
            sanitize_name(bundle["name"]),
            sanitize_name(bundle.get("version", "1.0-0"))
        )

        return raw_package_name

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
