import os
import getpass
import openssh_wrapper
from shutil import copy2

shell_server_ip = ''
problem_server_ip = ''
private_key = ''

def token():
  """Generate a token, should be random but does not have to be secure necessarily. Speed is a priority."""
  import uuid
  return str(uuid.uuid4().hex)

class Server:

  def __init__(self, url = '', port = 22, cwd='/'):
    self.remote = url != ''
    self.url = url
    self.port = port
    # This is path on target machine; useful for dropping things in home folders
    self.path = cwd
    self.user = getpass.getuser()

    if self.remote:
      self.conn = openssh_wrapper.SSHConnection(url,login='root', timeout = 240)

  def run(self, cmd):
    if self.remote:
      resp = self.conn.run('cd %s;%s'%(self.path,cmd))
      if resp.stdout:
        print(resp.stdout)
      if resp.stderr:
        print(resp.stderr)
    else:
      savedcwd = os.getcwd() # I'm not really happy with the way we handle working dirs locally
      os.chdir(self.path)    # could bite us in the ass during local test deployments
      retval = os.system(cmd)
      os.chdir(savedcwd)
      return retval

  def add_user(self, user, password = None):
    if password == None:
      password = token()
    user = user.lower()
    self.run('useradd %s -b /home -m' % user)
    self.run('echo -e "%s\n%s" | (passwd %s) &> /dev/null' % (password, password, user))
    self.run('chown -R %s:%s /home/%s' % (user, user, user))
    self.run('chsh -s /bin/bash %s' % user)

  def add_group(self, name):
    return self.run('addgroup %s' % name.lower())

  def install_package(self, package):
    return self.run("dpkg -s %s &>/dev/null || apt-get install -y %s" % (package,package))

  def chmod(self, path, perms):
    return self.run('chmod %s %s' % (perms, path))

  def chown(self, path, user, group):
    if user == None:
      user = self.user
    if group == None:
      group = self.user
    return self.run('chown %s:%s %s' % (user, group, path))

  def push_file(self, local_path, remote_path, perm = '0755', owner = None, group = None):
    if self.remote:
      if not isinstance(local_path,list):
        local_path = [local_path]
      if group is not None:
        if owner is None:
          owner = self.user
        owner = owner+":"+group
      self.conn.scp(local_path,remote_path,mode=perm,owner=owner)
    else:
      return self.run('cp %s %s' % (local_path, remote_path))

  def push_fo(self, f, remote_path, perm = '0755', owner = None, group = None):
    if self.remote:
      if not isinstance(f,list):
        f = [f]
      if group is not None:
        if owner is None:
          owner = self.user
        owner = owner+":"+group
      self.conn.scp(f,remote_path,mode=perm,owner=owner)
    else:
      assert(False)

  def push_folder(self, local, remote, perm = '0711', owner = None, group = None):
    return self.push_file(local,remote,perm,owner)

  def makedirs(self, dir):
    self.run('mkdir -p %s' % dir)
