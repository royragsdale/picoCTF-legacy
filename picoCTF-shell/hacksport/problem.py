"""
Challenge deployment and problem types.
"""

from abc import ABCMeta, abstractmethod, abstractproperty
from hashlib import md5
from hacksport.operations import give_port, execute

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
        hash_token = md5(token.encode("utf-8")).hexdigest()

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

class Compiled(Challenge):
    """
    Sensible behavior for compiled challenges.
    """

    compiler = "gcc"
    compiler_flags = []
    compiler_options = ""

    makefile = None

    def compiler_sources(self):
        pass

    def setup(self):
        pass

    def compiler_setup(self):
        """
        Setup function for compiled challenges
        """

        if self.makefile is not None:
            execute(["make", "-f", self.makefile])

class Remote(Challenge):
    """
    Base behavior for remote challenges.
    """

    @property
    def port(self):
        """
        Provides port on-demand with caching
        """
        if not hasattr(self, '_port'):
            self._port = give_port()
        return self._port

    def remote_setup(self):
        """
        Setup function for remote challenges
        """
        pass

    def service(self):
        #TODO: use full path of binary for EXEC:
        return {"Type":"simple",
                "ExecStart":"socat tcp-listen:{},fork,reuseaddr,su={} EXEC:./{}".format(
                    self.port, self.user, self.program_name)
               }
