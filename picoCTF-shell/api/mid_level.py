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

    def setup(self):
        pass

    @property
    def port(self):
        if not hasattr(self, 'port'):
            self.port = give_port()
        return port


    def service(self):
        return {"Type":"simple",
                "ExecStart":"socat tcp-listen:{},fork,reuseaddr,su={} EXEC:./{}".format(
                    self.port, self.user, self.executable_name)
               }

    def setup_remote(self):
        #TODO: setup permissions
        pass

class Compiled(Challenge):

    def setup(self):
        pass

    def setup_compiled(self):
        exec_cmd("make")
        #TODO: setup permissions
