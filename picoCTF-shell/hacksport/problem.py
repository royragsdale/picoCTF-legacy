"""
Challenge deployment and problem types.
"""

from abc import ABCMeta, abstractmethod, abstractproperty
from hashlib import md5
from hacksport.operations import give_port, execute

import os

class File(object):
    """
    Wraps files with default permissions
    """

    def __init__(self, path, permissions=0o664):
        self.path = path
        self.permissions = permissions

    def __repr__(self):
        return "{}({},{})".format(self.__class__.__name__, repr(self.path), oct(self.permissions))

class ExecutableFile(File):
    """
    Wrapper for executable files that will make them setgid and owned
    by the problem's group.
    """

    def __init__(self, path):
        super().__init__(path, permissions=0o2755)

class ProtectedFile(File):
    """
    Wrapper for protected files, i.e. files that can only be read after
    escalating privileges. These will be owned by the problem's group.
    """

    def __init__(self, path):
        super().__init__(path, permissions=0o0440)

class Challenge(metaclass=ABCMeta):
    """
    The most hands off, low level approach to creating challenges.
    Requires manual setup and generation.
    """

    files = []

    def generate_flag(self, random):
        """
        Default generation of flags.

        Args:
            random: seeded random module.
        """

        token = str(random.randint(1, 1e12))
        hash_token = md5(token.encode("utf-8")).hexdigest()

        return hash_token

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

        return {
            "Type": "oneshot",
            "ExecStart": ""
        }

class Compiled(Challenge):
    """
    Sensible behavior for compiled challenges.
    """

    compiler = "gcc"
    compiler_flags = []
    compiler_sources = []

    makefile = None

    program_name = None

    def setup(self):
        """ No-op implementation for Challenge. """
        pass

    def compiler_setup(self):
        """
        Setup function for compiled challenges
        """

        if self.program_name is None:
            raise Exception("Must specify program_name for compiled challenge.")

        if self.makefile is not None:
            execute(["make", "-f", self.makefile])
        elif len(self.compiler_sources) > 0:
            compile_cmd = [self.compiler] + self.compiler_flags + self.compiler_sources
            compile_cmd += ["-o", self.program_name]
            execute(compile_cmd)

        self.compiled_files = [ExecutableFile(self.program_name)]

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

        if self.program_name is None:
            raise Exception("Must specify program_name for remote challenge.")

        self.remote_files = [ExecutableFile(self.program_name)]

    def service(self):
        return {"Type":"simple",
                "ExecStart":"socat tcp-listen:{},fork,reuseaddr,su={} EXEC:{}".format(
                    self.port, self.user, os.path.join(self.directory, self.program_name))
               }
