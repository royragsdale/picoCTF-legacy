from random import Random, randint
from abc import ABCMeta
from api.mid_level import Remote, Compiled
from api.low_level import exec_cmd

def challenge_meta(problem_name, seed, user):
    """
    Returns a metaclass that will introduce a self.random object seeded
    to the given seed, self.user set to the linux username for this instance,
    etc.

    Args:
        problem_name: The problem name
        seed: The seed for the Random object
        user: The linux username for this challenge instance

    Returns:
        The metaclass described above
    """

    class ChallengeMeta(ABCMeta):
        def __new__(cls, name, bases, attr):
            attributes = dict(attr)
            attributes['name'] = problem_name
            attributes['random'] = Random(seed)
            attributes['user'] = user
            return super().__new__(cls, name, bases, attributes)
    return ChallengeMeta

def get_updated_problem_class(Class, problem_name, seed, user):
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

    return challenge_meta(problem_name, seed, user)(Class.__name__, Class.__bases__, Class.__dict__)

def create_service(problem):
    """
    Creates a systemd service file for the given problem

    Args:
        problem: the instantiated problem object
    Returns:
        A string containing the service configuration
    """

    template = """[Unit]
Description={} instance

[Service]
Type={}
ExecStart={}

[Install]
WantedBy=multi-user.target"""

    problem_service_info = problem.service()
    return template.format(problem.name, problem_service_info['Type'], problem_service_info['ExecStart'])

def get_random_user_for_problem(problem_name):
    """
    Generates a random username based on the problem name. The username returned is guaranteed to
    not exist.

    Args:
        problem_name: The name of the problem
    Returns:
        The username generated
    """

    converted_name = problem_name.replace(" ","_").lower()

    username = "{}{}".format(converted_name, randint(0, 100000))
    cmd = "id {}\n".format(username)
    result = str(exec_cmd(cmd)[1], "utf-8")
    if "no such user" not in result:
        return get_random_user_for_problem(problem_name)
    return username


def generate_instance(Problem, problem_object):
    """
    Runs the setup functions of Problem in the correct order

    Args:
        Problem: The Problem class to be generated
        problem_object: The contents of the problem.json

    Returns:
        A tuple containing the service string and the flag of the generated instance
    """

    # TODO: make username, seed deterministic
    username = get_random_user_for_problem(problem_object['name'])
    seed = username

    Problem = get_updated_problem_class(Problem, problem_object['name'], seed, username)

    #TODO: add templating

    # run methods in proper order
    p = Problem()
    p.initialize()
    if isinstance(p, Compiled):
        p.setup_compiled()
    if isinstance(p, Remote):
        p.setup_remote()
    p.setup()


    #TODO: add staging directory, user creation, and copying files

    service = create_service(p)

    # reseed and generate flag
    p.random.seed(seed)
    flag = p.generate_flag()

    return service, flag
