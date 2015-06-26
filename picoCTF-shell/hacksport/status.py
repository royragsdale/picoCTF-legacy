from shell_manager.util import HACKSPORTS_ROOT, PROBLEM_ROOT, STAGING_ROOT, DEPLOYED_ROOT, BUNDLE_ROOT
from shell_manager.bundle import get_bundle, get_bundle_root
from shell_manager.problem import get_problem, get_problem_root

from os.path import join

import os
import shutil
import socket
import json

def get_all_problems():
    """ Returns a dictionary of name:object mappings """

    problems = {}
    if os.path.isdir(PROBLEM_ROOT):
        for name in os.listdir(PROBLEM_ROOT):
            try:
                problem = get_problem(get_problem_root(name, absolute=True))
                problems[name] = problem
            except FileNotFoundError as e:
                pass
    return problems

def get_all_bundles():
    """ Returns a dictionary of name:object mappings """

    bundles = {}
    if os.path.isdir(BUNDLE_ROOT):
        for name in os.listdir(BUNDLE_ROOT):
            try:
                bundle = get_bundle(get_bundle_root(name, absolute=True))
                bundles[name] = bundle
            except FileNotFoundError as e:
                pass
    return bundles

def get_all_problem_instances(problem_path):
    """ Returns a list of instances for a given problem """

    instances = {}
    instances_dir = join(DEPLOYED_ROOT, problem_path)
    if os.path.isdir(instances_dir):
        for name in os.listdir(instances_dir):
            if name.endswith(".json"):
                try:
                    instance = json.loads(open(join(instances_dir, name)).read())
                except Exception as e:
                    continue

                instances[instance["iid"]] = instance

    result = []
    for i in range(len(instances.items())):
        result.append(instances[i])
    return result

def publish(args, config):
    """ Main entrypoint for publish """

    problems = get_all_problems()
    bundles = get_all_bundles()

    output = {
        "problems": [],
        "bundles": []
    }

    for path, problem in problems.items():
        problem["instances"] = get_all_problem_instances(path)
        if len(problem["instances"]) > 0:
            output["problems"].append(problem)

    for path, bundle in bundles.items():
        output["bundles"].append(bundle)

    print(json.dumps(output, indent=4))

def clean(args, config):
    """ Main entrypoint for clean """

    lock_file = join(HACKSPORTS_ROOT, "deploy.lock")

    # remove staging directories
    if os.path.isdir(STAGING_ROOT):
        shutil.rmtree(STAGING_ROOT)

    # remove lock file
    if os.path.isfile(lock_file):
        os.remove(lock_file)

    #TODO: potentially perform more cleaning

def status(args, config):
    """ Main entrypoint for status """

    bundles = get_all_bundles()
    problems = get_all_problems()

    def print_problem(problem, path, prefix="\t"):
        instances = get_all_problem_instances(path)
        print("{}* [{}] {} ({})".format(prefix, len(instances), problem['name'], path))
        for i, instance in enumerate(instances):
            if "port" in instance:
                status = "(online)"
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect(("localhost", instance["port"]))
                except ConnectionRefusedError as e:
                    status = "[OFFLINE]"
            else:
                status = ""

            print("{0}\t - Instance {1}:\n{0}\t\tport: {2} {4}\n{0}\t\tflag: {3}".format(
                            prefix, i, instance["port"] if "port" in instance else None, instance["flag"],
                            status))

    def print_bundle(bundle, path, prefix=""):
        print("{}[{} ({})]".format(prefix, bundle["name"], path))
        for problem_path in bundle["problems"]:
            problem = problems[problem_path]
            print_problem(problem, problem_path, prefix=prefix+"\t")

    if args.problem is not None:
        problem = problems.get(args.problem, None)
        if problem is None:
            print("Could not find problem \"{}\"".format(args.problem))
            return
        print_problem(problem, args.problem, prefix="")
    elif args.bundle is not None:
        bundle = bundles.get(args.bundle, None)
        if bundle is None:
            print("Could not find bundle \"{}\"".format(args.bundle))
            return
        print_bundle(bundle, args.bundle, prefix="")
    else:
        print("** Installed Bundles [{}] **".format(len(bundles)))
        shown_problems = []
        for path, bundle in bundles.items():
            print_bundle(bundle, path, prefix="\t")
            shown_problems.extend(bundle["problems"])

        print("** Installed Problems [{}] **".format(len(problems)))
        print("   Showing status for problems not already shown...")
        for path, problem in problems.items():
            if path not in shown_problems:
                print_problem(problem, path, prefix="\t")
