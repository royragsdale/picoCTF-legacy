"""
Problem deployment.
"""

from random import Random, randint
from abc import ABCMeta
from hashlib import md5
from imp import load_source
from pwd import getpwnam
from json import loads
from jinja2 import Environment, Template, FileSystemLoader
from hacksport.problem import Remote, Compiled, File, ProtectedFile, ExecutableFile
from hacksport.operations import create_user

import os
import re
import shutil

# TODO: move somewhere else
SECRET = "hacksports2015"

def get_attributes(obj):
    """
    Returns all attributes of an object, excluding those that start with
    an underscore

    Args:
        obj: the object

    Returns:
        A dictionary of attributes
    """

    return {key:getattr(obj, key) if not key.startswith("_") else None for key in dir(obj)}

def sanitize_name(name):
    """
    Sanitize a given name such that it conforms to unix policy.

    Args:
        name: the name to sanitize.

    Returns:
        The sanitized form of name.
    """

    sanitized_name = re.sub(r"[^a-z0-9\+-\.]", "-", name.lower())
    return sanitized_name

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

def update_problem_class(Class, problem_object, seed, user):
    """
    Changes the metaclass of the given class to introduce necessary fields before
    object instantiation.

    Args:
        Class: The problem class to be updated
        problem_name: The problem name
        seed: The seed for the Random object
        user: The linux username for this challenge instance

    Returns:
        The updated class described above
    """

    random = Random(seed)
    attributes = problem_object
    attributes.update({"random": random, "user": user})
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
WantedBy=multi-user.target"""

    problem_service_info = problem.service()
    converted_name = sanitize_name(problem.name)
    content = template.format(problem.name, problem_service_info['Type'], problem_service_info['ExecStart'])
    service_file_path = os.path.join(path, "{}_{}.service".format(converted_name, instance_number))

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
    home_directory = create_user(username)
    return username, home_directory

def generate_seed(*args):
    """
    Generates a seed using the list of string arguments
    """

    return md5("".join(args).encode("utf-8")).hexdigest()

def generate_staging_directory(root="/tmp/staging/"):
    """
    Creates a random, empty staging directory

    Args:
        root: The parent directory for the new directory. Defaults to /tmp/staging/

    Returns:
        The path of the generated directory
    """

    if not os.path.isdir(root):
        os.makedirs(root)

    def get_new_path():
        path = os.path.join(root, str(randint(0, 1e12)))
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

def template_staging_directory(staging_directory, problem):
    """
    Templates every file in the staging directory recursively other than
    problem.json.

    Args:
        staging_directory: The path of the staging directory
        problem: The problem object
    """

    for root, dirnames, filenames in os.walk(staging_directory):
        for filename in filenames:
            if filename == "problem.json":
                continue
            fullpath = os.path.join(root, filename)
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

    # get uid and gid for root and problem user
    user = getpwnam(username)
    root = getpwnam("root")

    for f in file_list:
        output_path = os.path.join(instance_directory, os.path.basename(f.path))
        shutil.copy2(os.path.join(staging_directory, f.path), output_path)

        os.chmod(output_path, f.permissions)

        if isinstance(f, ProtectedFile) or isinstance(f, ExecutableFile):
            os.chown(out_file_path, root.pw_uid, user.pw_gid)
        else:
            os.chown(out_file_path, root.pw_uid, root.pw_gid)

def generate_instance(problem_object, problem_directory, instance_number, test_instance=False):
    """
    Runs the setup functions of Problem in the correct order

    Args:
        problem_object: The contents of the problem.json

    Returns:
        A tuple containing (flag, staging_directory, files)
    """

    username, home_directory = create_instance_user(problem_object['name'], instance_number)
    seed = generate_seed(problem_object['name'], SECRET, str(instance_number))
    staging_directory = generate_staging_directory()
    copypath = os.path.join(staging_directory, "problem_files")
    shutil.copytree(problem_directory, copypath)

    challenge = load_source("challenge", os.path.join(copypath, "challenge.py"))

    Problem = update_problem_class(challenge.Problem, problem_object, seed, username)

    # store cwd to restore later
    cwd = os.getcwd()
    os.chdir(copypath)

    # run methods in proper order
    p = Problem()
    p.initialize()

    # reseed and generate flag
    p.flag = p.generate_flag(Random(seed))

    template_staging_directory(staging_directory, p)

    if isinstance(p, Compiled):
        p.compiler_setup()
    if isinstance(p, Remote):
        p.remote_setup()
    p.setup()

    os.chdir(cwd)

    all_files = p.files

    if isinstance(p, Compiled):
        all_files.extend(p.compiled_files)
    if isinstance(p, Remote):
        all_files.extend(p.remote_files)

    assert all([isinstance(f, File) for f in all_files])

    service = create_service_file(p, instance_number, staging_directory)

    # template the description
    p.description = template_string(p.description, **get_attributes(p))

    return p, staging_directory, all_files

def deploy_problem(problem_directory, instances=1):
    """
    Deploys the problem specified in problem_directory.

    Args:
        problem_directory: The directory storing the problem
        instances: The number of instances to deploy. Defaults to 1.

    Returns:
        TODO
    """

    object_path = os.path.join(problem_directory, "problem.json")

    with open(object_path, "r") as f:
        json_string = f.read()

    problem_object = loads(json_string)

    for instance_number in range(instances):
        print("Generating instance {}".format(instance_number))
        problem, staging_directory, files = generate_instance(problem_object, problem_directory, instance_number)
        print("\tdesc={}\n\tflag={}\n\tstaging_directory={}\n\tfiles={}".format(problem.description, problem.flag, staging_directory, files))
