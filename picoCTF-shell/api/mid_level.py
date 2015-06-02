from abc import ABCMeta, abstractmethod, abstractproperty
from os import system
from api.low_level import give_port, exec_cmd

hexdigits = "0123456789abcdef"

class Challenge(object, metaclass=ABCMeta):
    """
    Abstract base class for all challenges.

    Abstract methods:
        setup
    """

    @abstractmethod
    def setup(self):
        pass

    def initialize(self):
        pass

    def service(self):
        pass

    # default flag generation
    def generate_flag(self):
        return "".join([self.random.choice(hexdigits) for i in range(64)])

class Remote(Challenge):
    """
    Base class for remote challenges
    Subclasses must specify executable_name field
    """

    def setup(self):
        pass

    @property
    def port(self):
        if not hasattr(self, '_port'):
            self._port = give_port()
        return self._port


    def service(self):
        #TODO: use full path of binary for EXEC:
        return {"Type":"simple",
                "ExecStart":"socat tcp-listen:{},fork,reuseaddr,su={} EXEC:./{}".format(
                    self.port, self.user, self.executable_name)
               }

    def setup_remote(self):
        #TODO: setup permissions
        pass

class Compiled(Challenge):
    """
    Base class for Compiled challenges
    """

    def setup(self):
        pass

    def setup_compiled(self):
        exec_cmd("make")
        #TODO: setup permissions

class Static(Challenge):
    """
    Abstract base class for static challenges

    Abstract properties:
        flag

    Abstract methods:
        -
    """

    @abstractproperty
    def flag():
        pass
