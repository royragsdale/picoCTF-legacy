"""
Problem deployment.
"""

PROBLEM_FILES_DIR = "problem_files"

# will be set to the configuration module during deployment
deploy_config = None

port_map = {}
current_problem = None
current_instance = None

def get_deploy_context():
    """
    Returns the deployment context, a dictionary containing the current
    config, port_map, problem, instance
    """

    global deploy_config, port_map, current_problem, current_instance

    return {
        "config": deploy_config,
        "port_map": port_map,
        "problem": current_problem,
        "instance": current_instance
    }

from os.path import join
from random import Random, randint
from abc import ABCMeta
from hashlib import md5
from imp import load_source
from pwd import getpwnam
from grp import getgrnam
from time import sleep
from copy import copy, deepcopy
from spur import RunProcessError
from jinja2 import Environment, Template, FileSystemLoader
from hacksport.problem import Remote, Compiled, Service, FlaskApp, PHPApp
from hacksport.problem import File, ProtectedFile, ExecutableFile
from hacksport.operations import create_user, execute
from hacksport.utils import sanitize_name, get_attributes
from shell_manager.bundle import get_bundle

from shell_manager.bundle import get_bundle, get_bundle_root
from shell_manager.problem import get_problem, get_problem_root
from shell_manager.util import HACKSPORTS_ROOT, PROBLEM_ROOT, STAGING_ROOT, DEPLOYED_ROOT, BUNDLE_ROOT

import os
import json
import shutil
import functools

def challenge_meta(attributes):
    """
    Returns a metaclass that will introduce the given attributes into the class
    namespace.

    Args:
        attributes: The dictionary of attributes

    Returns:
        The metaclass described above
    """

    class ChallengeMeta(ABCMeta):
        def __new__(cls, name, bases, attr):
            attrs = dict(attr)
            attrs.update(attributes)
            return super().__new__(cls, name, bases, attrs)
    return ChallengeMeta

def update_problem_class(Class, problem_object, seed, user, instance_directory):
    """
    Changes the metaclass of the given class to introduce necessary fields before
    object instantiation.

    Args:
        Class: The problem class to be updated
        problem_name: The problem name
        seed: The seed for the Random object
        user: The linux username for this challenge instance
        instance_directory: The deployment directory for this instance

    Returns:
        The updated class described above
    """

    random = Random(seed)
    attributes = deepcopy(problem_object)

    attributes.update({"random": random, "user": user, "default_user": deploy_config.DEFAULT_USER,
                       "server": deploy_config.HOSTNAME, "directory": instance_directory})

    return challenge_meta(attributes)(Class.__name__, Class.__bases__, Class.__dict__)

def create_service_file(problem, instance_number, path):
    """
    Creates a systemd service file for the given problem

    Args:
        problem: the instantiated problem object
        instance_number: the instance number
        path: the location to drop the service file
    Returns:
        The path to the created service file
    """

    template = """[Unit]
Description={} instance

[Service]
Type={}
ExecStart={}

[Install]
WantedBy=default.target
"""

    problem_service_info = problem.service()
    converted_name = sanitize_name(problem.name)
    content = template.format(problem.name, problem_service_info['Type'], problem_service_info['ExecStart'])
    service_file_path = join(path, "{}_{}.service".format(converted_name, instance_number))

    with open(service_file_path, "w") as f:
        f.write(content)

    return service_file_path

def create_instance_user(problem_name, instance_number):
    """
    Generates a random username based on the problem name. The username returned is guaranteed to
    not exist.

    Args:
        problem_name: The name of the problem
        instance_number: The unique number for this instance
    Returns:
        A tuple containing the username and home directory
    """

    converted_name = sanitize_name(problem_name)
    username = "{}_{}".format(converted_name, instance_number)

    try:
        #Check if the user already exists.
        user = getpwnam(username)
        return username, user.pw_dir
    except KeyError:
        home_directory = create_user(username, deploy_config.HOME_DIRECTORY_ROOT)
        return username, home_directory

def generate_seed(*args):
    """
    Generates a seed using the list of string arguments
    """

    return md5("".join(args).encode("utf-8")).hexdigest()

def generate_staging_directory(root=STAGING_ROOT):
    """
    Creates a random, empty staging directory

    Args:
        root: The parent directory for the new directory. Defaults to join(HACKSPORTS_ROOT, "staging")

    Returns:
        The path of the generated directory
    """

    if not os.path.isdir(root):
        os.makedirs(root)

    def get_new_path():
        path = join(root, str(randint(0, 1e12)))
        if os.path.isdir(path):
            return get_new_path()
        return path

    path = get_new_path()
    os.makedirs(path)
    return path

def template_string(template, **kwargs):
    """
    Templates the given string with the keyword arguments

    Args:
        template: The template string
        **kwards: Variables to use in templating
    """

    temp = Template(template)
    return temp.render(**kwargs)

def template_file(in_file_path, out_file_path, **kwargs):
    """
    Templates the given file with the keyword arguments.

    Args:
        in_file_path: The path to the template
        out_file_path: The path to output the templated file
        **kwargs: Variables to use in templating
    """

    env = Environment(loader=FileSystemLoader(os.path.dirname(in_file_path)))
    template = env.get_template(os.path.basename(in_file_path))
    output = template.render(**kwargs)

    with open(out_file_path, "w") as f:
        f.write(output)

def template_staging_directory(staging_directory, problem, dont_template_files = ["problem.json", "challenge.py"],
                                                           dont_template_directories = ["templates"]):
    """
    Templates every file in the staging directory recursively other than
    problem.json and challenge.py.

    Args:
        staging_directory: The path of the staging directory
        problem: The problem object
        dont_template_files: The list of files not to template. Defaults to ["problem.json", "challenge.py"]
        dont_template_directories: The list of files not to recurse into. Defaults to ["templates"]
    """

    # prepend the staging directory to all
    dont_template_directories = [join(staging_directory, directory) for directory in dont_template_directories]

    for root, dirnames, filenames in os.walk(staging_directory):
        if root in dont_template_directories:
            continue
        for filename in filenames:
            if filename in dont_template_files:
                continue
            fullpath = join(root, filename)
            try:
                template_file(fullpath, fullpath, **get_attributes(problem))
            except UnicodeDecodeError as e:
                # tried templating binary file
                pass

def deploy_files(staging_directory, instance_directory, file_list, username):
    """
    Copies the list of files from the staging directory to the instance directory.
    Will properly set permissions and setgid files based on their type.
    """

    # get uid and gid for default and problem user
    user = getpwnam(username)
    default = getpwnam(deploy_config.DEFAULT_USER)

    for f in file_list:
        # copy the file over, making the directories as needed
        output_path = join(instance_directory, f.path)
        if not os.path.isdir(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))
        shutil.copy2(join(staging_directory, f.path), output_path)

        # set the ownership based on the type of file
        if isinstance(f, ProtectedFile) or isinstance(f, ExecutableFile):
            os.chown(output_path, default.pw_uid, user.pw_gid)
        else:
            uid = default.pw_uid if f.user is None else getpwnam(f.user).pw_uid
            gid = default.pw_gid if f.group is None else getgrnam(f.group).gr_gid
            os.chown(output_path, uid, gid)

        # set the permissions appropriately
        os.chmod(output_path, f.permissions)

def install_user_service(home_directory, user, service_file):
    """
    Installs the service file into the systemd user directory for the provided user,
    sets the service to start on boot, and starts the service now.

    Args:
        home_directory: The home directory for the user provided
        user: The user that will run the service
        service_file: The path to the systemd service file to install
    """

    # make user service directory
    service_dir_path = os.path.join(home_directory, ".config", "systemd", "user")
    if not os.path.isdir(service_dir_path):
        os.makedirs(service_dir_path)

    # make target directory for enabled services
    default_target_path = os.path.join(service_dir_path, "default.target.wants")
    if not os.path.isdir(default_target_path):
        os.makedirs(default_target_path)

    userpw = getpwnam(user)
    os.chown(default_target_path, userpw.pw_uid, userpw.pw_gid)

    # copy service file
    service_path = os.path.join(service_dir_path, os.path.basename(service_file))
    shutil.copy2(service_file, service_path)

    # enable automatic starting of user services
    execute("loginctl enable-linger {}".format(user))
    execute("systemctl restart user@{}.service".format(userpw.pw_uid))

    # set environment variable so "su -l problem_user" will correctly populate it
    # this is due to a known issue with su -l
    with open(os.path.join(home_directory, ".profile"), "w") as f:
        f.write("export XDG_RUNTIME_DIR=/run/user/{}\n".format(userpw.pw_uid))

    # enable and restart the service
    execute("su -l {} bash -c 'systemctl --user daemon-reload; systemctl --user enable {}; systemctl --user restart {}'".format(
        user, os.path.basename(service_file), os.path.basename(service_file)))

def generate_instance(problem_object, problem_directory, instance_number, deployment_directory=None):
    """
    Runs the setup functions of Problem in the correct order

    Args:
        problem_object: The contents of the problem.json
        problem_directory: The directory to the problem
        instance_number: The instance number to be generated
        deployment_directory: The directory that will be deployed to. Defaults to the home directory of the user created.

    Returns:
        A tuple containing (problem, staging_directory, home_directory, files)
    """

    username, home_directory = create_instance_user(problem_object['name'], instance_number)
    seed = generate_seed(problem_object['name'], deploy_config.DEPLOY_SECRET, str(instance_number))
    staging_directory = generate_staging_directory()
    copypath = join(staging_directory, PROBLEM_FILES_DIR)
    shutil.copytree(problem_directory, copypath)

    # store cwd to restore later
    cwd = os.getcwd()
    os.chdir(copypath)

    challenge = load_source("challenge", join(copypath, "challenge.py"))

    if deployment_directory is None: deployment_directory = home_directory

    Problem = update_problem_class(challenge.Problem, problem_object, seed, username, deployment_directory)

    # run methods in proper order
    problem = Problem()

    # reseed and generate flag
    problem.flag = problem.generate_flag(Random(seed))

    problem.initialize()


    web_accessible_files = []

    def url_for(web_accessible_files, source_name, display=None):
        source_path = join(copypath, source_name)

        problem_hash = problem_object["name"] + deploy_config.DEPLOY_SECRET + str(instance_number)
        problem_hash = md5(problem_hash.encode("utf-8")).hexdigest()

        destination_path = join(sanitize_name(problem_object["name"]), problem_hash, source_name)

        link_template = "<a href='{}'>{}</a>"

        web_accessible_files.append((source_path, join(deploy_config.WEB_ROOT, destination_path)))
        uri_prefix = "//"
        uri = join(uri_prefix, deploy_config.HOSTNAME, destination_path)

        return link_template.format(uri, source_name if display is None else display)

    problem.url_for = functools.partial(url_for, web_accessible_files)

    template_staging_directory(copypath, problem)

    if isinstance(problem, Compiled):
        problem.compiler_setup()
    if isinstance(problem, Remote):
        problem.remote_setup()
    if isinstance(problem, FlaskApp):
        problem.flask_setup()
    if isinstance(problem, PHPApp):
        problem.php_setup()
    if isinstance(problem, Service):
        problem.service_setup()
    problem.setup()

    os.chdir(cwd)

    all_files = copy(problem.files)

    if isinstance(problem, Compiled):
        all_files.extend(problem.compiled_files)
    if isinstance(problem, Service):
        all_files.extend(problem.service_files)

    assert all([isinstance(f, File) for f in all_files])

    service_file = create_service_file(problem, instance_number, staging_directory)

    # template the description
    problem.description = template_string(problem.description, **get_attributes(problem))

    return {"problem": problem,
            "staging_directory": staging_directory,
            "home_directory": home_directory,
            "files": all_files,
            "web_accessible_files": web_accessible_files,
            "service_file": service_file
            }

def deploy_problem(problem_directory, instances=1, test=False, deployment_directory=None):
    """
    Deploys the problem specified in problem_directory.

    Args:
        problem_directory: The directory storing the problem
        instances: The number of instances to deploy. Defaults to 1.
        test: Whether the instances are test instances or not. Defaults to False.
        deployment_directory: If not None, the challenge will be deployed here instead of their home directory
    """

    global current_problem, current_instance

    problem_object = get_problem(problem_directory)

    current_problem = problem_object["name"]

    instance_list = []

    for instance_number in range(instances):
        current_instance = instance_number
        print("Generating instance {} of \"{}\".".format(instance_number, problem_object["name"]))
        instance = generate_instance(problem_object, problem_directory, instance_number, deployment_directory=deployment_directory)
        instance_list.append(instance)

    deployment_json_dir = os.path.join(DEPLOYED_ROOT, sanitize_name(problem_object["name"]))
    if not os.path.isdir(deployment_json_dir):
        os.makedirs(deployment_json_dir)

    # all instances generated without issue. let's do something with them
    for instance_number, instance in enumerate(instance_list):
        print("Deploying instance {} of \"{}\".".format(instance_number, problem_object["name"]))
        problem_path = os.path.join(instance["staging_directory"], PROBLEM_FILES_DIR)

        problem = instance["problem"]

        if test is True:
            # display what we would do, and clean up the user and home directory
            destination_directory = os.path.join(instance["staging_directory"], "deployed") if deployment_directory is None \
                                    else deployment_directory
            deploy_files(problem_path, destination_directory, instance["files"], problem.user)
            print("\tDescription: {}".format(problem.description))
            print("\tFlag: {}".format(problem.flag))
            print("\tDeployment Directory: {}".format(destination_directory))

            try:
                execute("killall -u {}".format(problem.user))
                sleep(0.1)
            except RunProcessError as e:
                pass

            execute(["userdel", problem.user])
            shutil.rmtree(instance["home_directory"])

            deployment_json_dir = instance["staging_directory"]
        else:
            # let's deploy them now
            destination_directory = instance["home_directory"] if deployment_directory is None else deployment_directory
            problem_path = os.path.join(instance["staging_directory"], PROBLEM_FILES_DIR)
            deploy_files(problem_path, destination_directory, instance["files"], problem.user)

            # copy files to the web root
            for source, destination in instance["web_accessible_files"]:
                if not os.path.isdir(os.path.dirname(destination)):
                    os.makedirs(os.path.dirname(destination))
                shutil.copy2(source, destination)

            install_user_service(instance["home_directory"], problem.user, instance["service_file"])

            # delete staging directory
            shutil.rmtree(instance["staging_directory"])

        deployment_info = {
            "server": problem.server,
            "description": problem.description,
            "flag": problem.flag,
            "iid": instance_number,
        }

        if isinstance(problem, Service):
            deployment_info["port"] = problem.port

        instance_info_path = os.path.join(deployment_json_dir, "{}.json".format(instance_number))
        with open(instance_info_path, "w") as f:
            f.write(json.dumps(deployment_info, indent=4, separators=(", ", ": ")))

        print("The instance deployment information can be found at {}.".format(instance_info_path))

def get_all_problems():
    """ Returns a dictionary of name:object mappings """
    problems = {}
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
                    instances[instance["iid"]] = instance
                except Exception as e:
                    pass

    result = []
    for i in range(len(instances.items())):
        result.append(instances[i])
    return result

def deploy_problems(args, config):
    """ Main entrypoint for problem deployment """

    lock_file = join(HACKSPORTS_ROOT, "deploy.lock")

    if os.path.isfile(lock_file):
        raise Exception("Cannot deploy while other deployment in progress. If you believe this is an error, "
                         "run 'shell_manager clean'")

    with open(lock_file, "w") as f:
        f.write("1")

    global deploy_config, port_map
    deploy_config = config

    try:
        user = getpwnam(deploy_config.DEFAULT_USER)
    except KeyError as e:
        print("DEFAULT_USER {} does not exist. Creating now.".format(deploy_config.DEFAULT_USER))
        create_user(deploy_config.DEFAULT_USER)

    if args.deployment_directory is not None and (len(args.problem_paths) > 1 or args.num_instances > 1):
        raise Exception("Cannot specify deployment directory if deploying multiple problems or instances.")

    problems = args.problem_paths

    if args.bundle:
        bundle_problems = []
        for bundle_path in args.problem_paths:
            if os.path.isfile(bundle_path):
                bundle = get_bundle(bundle_path)
                bundle_problems.extend(bundle["problems"])
            else:
                bundle_sources_path = get_bundle_root(bundle_path, absolute=True)
                if os.path.isdir(bundle_sources_path):
                    bundle = get_bundle(bundle_sources_path)
                    bundle_problems.extend(bundle["problems"])
                else:
                    raise Exception("Could not get bundle.")
        problems = bundle_problems

    # before deploying problems, load in port_map
    for path, problem in get_all_problems().items():
        for instance in get_all_problem_instances(path):
            if "port" in instance:
                port_map[instance["port"]] = (problem["name"], instance["iid"])

    for path in problems:
        if os.path.isdir(path):
            deploy_problem(path, instances=args.num_instances, test=args.dry,
                            deployment_directory=args.deployment_directory)
        elif os.path.isdir(os.path.join(get_problem_root(path, absolute=True))):
            deploy_problem(os.path.join(get_problem_root(path, absolute=True)), instances=args.num_instances,
                            test=args.dry, deployment_directory=args.deployment_directory)
        else:
            raise Exception("Problem path {} cannot be found".format(path))

    os.remove(lock_file)

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
            print("{0}\t - Instance {1}:\n{0}\t\tport: {2}\n{0}\t\tflag: {3}".format(
                            prefix, i, instance["port"] if "port" in instance else None, instance["flag"]))

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
