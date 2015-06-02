from random import Random
from abc import ABCMeta
from api.mid_level import Remote, Compiled

def challenge_meta(seed, user):
    """
    Returns a metaclass that will introduce a self.random object seeded
    to the given seed, self.user set to the linux username for this instance,
    etc.

    Args:
        seed: The seed for the Random object
        user: The linux username for this challenge instance

    Returns:
        The metaclass described above
    """

    class ChallengeMeta(ABCMeta):
        def __new__(cls, name, bases, attr):
            attributes = dict(attr)
            attributes['random'] = Random(seed)
            attributes['user'] = user
            return super().__new__(cls, name, bases, attributes)
    return ChallengeMeta

def get_updated_problem_class(Class, seed, user):
    """
    Changes the metaclass of the given class to introduce necessary fields before
    object instantiation.

    Args:
        Class: The problem class to be updated
        seed: The seed for the Random object
        user: The linux username for this challenge instance

    Returns:
        The updated class described above
    """

    return challenge_meta(seed, user)(Class.__name__, Class.__bases__, Class.__dict__)

def generate(Problem, seed):
    """
    Runs the setup functions of Problem in the correct order

    Args:
        Problem: The Problem class to be generated
        seed: The string to seed the Random object with

    Returns:
        The flag of the generated instance
    """

    Problem = get_updated_problem_class(Problem, seed, "user1")

    # run methods in proper order
    p = Problem()
    p.initialize()
    if isinstance(p, Compiled):
        p.setup_compiled()
    if isinstance(p, Remote):
        p.setup_remote()
    p.setup()

    #TODO: add staging directory, user creation, and copying files

    # reseed and generate flag
    p.random.seed(seed)
    return p.generate_flag()
