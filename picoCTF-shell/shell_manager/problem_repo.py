"""
Problem repository management for the shell manager.
"""

import spur, gzip

from shutil import copy2
from os.path import join

def update(repo_path, deb_paths=[]):
    [copy2(deb_path, repo_path) for deb_path in deb_paths]

    shell = spur.LocalShell()
    result = shell.run(["dpkg-scanpackages", ".", "/dev/null"], cwd=repo_path)

    packages_path = join(repo_path, "Packages.gz")
    with gzip.open(packages_path, "wb") as packages:
        packages.write(result.output)

    print("Updated problem repository.")
