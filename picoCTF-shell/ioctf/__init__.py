import argparse
import os
import random
from ioctf import server
import string
from subprocess import Popen, STDOUT, PIPE
import tempfile

def local_pipe(cmd, input=''):
    #return Popen(cmd.split(" "), stdin=PIPE, stdout=PIPE, stderr=STDOUT).communicate(input=input)[0]
    return Popen(['/bin/bash','-c',cmd], stdin=PIPE, stdout=PIPE, stderr=STDOUT).communicate(input=input)[0]

def local_install(package):
    """ Legacy function, package installation taken care of by deb packages. """
    pass

def local_exec(cmd):
    os.system(cmd)

def local_deploy(setup, generate):
  parser = argparse.ArgumentParser(description='IOCTF challenge deployment')
  parser.add_argument('--setup', help="Install required packages", action="store_true")
  parser.add_argument('--token', type=str, help="Provide random token", default='cafebabe')
  parser.add_argument('--deploy', help="Deploy a new challenge instance", action="store_true")
  args = parser.parse_args()

  if args.setup or args.deploy:
    setup("test")
  if args.deploy:
    local_server = server.Server("localhost")
    generate(args.token, local_server)

deploy = local_deploy

def generate_key(problem_name, token, size=16, seed = ''):
  """ Generate IOCTF-specific keys given a problem name and a token """
  random.seed(problem_name + token + seed)
  chars = string.ascii_lowercase + string.digits
  return ''.join(random.choice(chars) for _ in range(size))

class TempFile:

    def __init__(self, prefix='', suffix=''):
        self.file = tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix, delete=False).name

    def __enter__(self):
        return self.file

    def __exit__(self, type, value, traceback):
        os.system('sudo rm -f %s' % self.file)
