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

    def __init__(self, path, permissions=0o664, user=None, group=None):
        self.path = path
        self.permissions = permissions
        self.user = user
        self.group = group

    def __repr__(self):
        return "{}({},{})".format(self.__class__.__name__, repr(self.path), oct(self.permissions))

class ExecutableFile(File):
    """
    Wrapper for executable files that will make them setgid and owned
    by the problem's group.
    """

    def __init__(self, path, permissions=0o2755):
        super().__init__(path, permissions=permissions)

class ProtectedFile(File):
    """
    Wrapper for protected files, i.e. files that can only be read after
    escalating privileges. These will be owned by the problem's group.
    """

    def __init__(self, path, permissions=0o0440):
        super().__init__(path, permissions=permissions)

def files_from_directory(directory, recurse=True, permissions=0o664):
    """
    Returns a list of File objects for every file in a directory. Can recurse optionally.

    Args:
        directory: The directory to add files from
        recurse: Whether or not to recursively add files. Defaults to true
        permissions: The default permissions for the files. Defaults to 0o664.
    """

    result = []

    for root, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            result.append(File(os.path.join(root, filename), permissions))
        if not recurse:
            break

    return result


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
            "ExecStart": "/bin/bash -c 'echo started'"
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

    compiled_files = []

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

class Service(Challenge):
    """
    Base class for challenges that are remote services.
    """

    service_files = []

    def setup(self):
        """
        No-op implementation of setup
        """

        pass

    def service_setup(self):
        if self.start_cmd is None:
            raise Exception("Must specify start_cmd for services.")

    @property
    def port(self):
        """
        Provides port on-demand with caching
        """
        if not hasattr(self, '_port'):
            self._port = give_port()
        return self._port


    def service(self):
        return {"Type":"simple",
                "ExecStart":"/bin/bash -c \"cd {}; {}\"".format(
                    self.directory, self.start_cmd)
               }

class Remote(Service):
    """
    Base behavior for remote challenges that use stdin/stdout.
    """

    def remote_setup(self):
        """
        Setup function for remote challenges
        """

        if self.program_name is None:
            raise Exception("Must specify program_name for remote challenge.")

        self.service_files = [ExecutableFile(self.program_name)]

        program_path = os.path.join(self.directory, self.program_name)
        self.start_cmd = "socat tcp-listen:{},fork,reuseaddr EXEC:{}".format(
                self.port, program_path)

class FlaskApp(Service):
    """
    Class for python Flask web apps
    """

    app = "server:app"

    def flask_setup(self):
        """
        Setup for flask apps
        """

        self.app_file = "{}.py".format(self.app.split(":")[0])
        assert os.path.isfile(self.app_file), "module must exist"

        self.service_files = [File(self.app_file)]
        self.start_cmd = "gunicorn --bind 0.0.0.0:{} -w 1 {}".format(self.port, self.app)

class PHPApp(Service):
    """
    Class for PHP web apps
    """

    php_root = ""

    def php_setup(self):
        """
        Setup for php apps
        """

        web_root = os.path.join(self.directory, self.php_root)
        self.start_cmd = "php -S 0.0.0.0:{} -t {}".format(self.port, web_root)
