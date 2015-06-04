"""
Challenge deployment and problem types.
"""

from abc import ABCMeta, abstractmethod, abstractproperty
from hashlib import md5

class Challenge(metaclass=ABCMeta):
    """
    The most hands off, low level approach to creating challenges.
    Requires manual setup and generation.
    """

    def generate_flag(self, random):
        """
        Default generation of flags.

        Args:
            random: seeded random module.
        """

        token = str(random.randint(1, 1e12))
        hash_token = md5(token.encode("utf-8"))

        return hash_token

    def generate_description(problem, environment):
        """
        Generate challenge's description.

        Args:
            problem: the challenge's problem object.
            environment: variables about the shell server that can be templated.

        Returns:
            The description for the problem instance.
        """

        pass

    def initialize(self):
        """
        Initial setup function that runs before any other.
        """

        pass

    @abstractmethod
    def setup(self):
        """
        Main setup method for the challenge.
        This is implemented by many of the more specific problem types.
        """

        pass

    def service(self):
        """
        No-op service file values.
        """

class Compiled(Challenge, metaclass=ABCMeta):
    """
    Sensible behavior for compiled challenges.
    """

    compiler = "gcc"
    compiler_flags = []
    compiler_options = ""

    makefile = None

    @abstractproperty
    def compiler_sources(self):
        pass

    @abstractproperty
    def program_name(self):
        pass

    def setup(self):
        pass

    def compiler_setup(self):
        pass

class Remote(Challenge, metaclass=ABCMeta):
    """
    Base behavior for remote challenges.
    """

    @abstractproperty
    def port(self):
        pass

    @abstractproperty
    def program_name(self):
        pass
