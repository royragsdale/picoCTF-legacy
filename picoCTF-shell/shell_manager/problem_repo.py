"""
Problem repository management for the shell manager.
"""

import spur, gzip

from shutil import copy2
from os.path import join

def local_update(repo_path, deb_paths=[]):
    """
    Updates a local deb repository by copying debs and running scanpackages.

    Args:
        repo_path: the path to the local repository.
        dep_paths: list of problem deb paths to copy.
    """

    [copy2(deb_path, repo_path) for deb_path in deb_paths]

    shell = spur.LocalShell()
    result = shell.run(["dpkg-scanpackages", ".", "/dev/null"], cwd=repo_path)

    packages_path = join(repo_path, "Packages.gz")
    with gzip.open(packages_path, "wb") as packages:
        packages.write(result.output)

    print("Updated problem repository.")
