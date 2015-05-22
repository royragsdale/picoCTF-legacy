import ioctf

import os
import problem_api
import time
import server
import StringIO
import hashlib
from werkzeug.utils import secure_filename

class DeployContext:

  def __init__(self, server, teamuser, token, problemname,port=None,seed=''):
    self.server = server # a Server object; specifies where we're deploying to
    self.teamuser = teamuser # shell server account name of team deploying for
    self.token = secure_filename(token) # token for this problem instance
    self.probname = problem_api.normalize_name(problemname) # displayname of problem
    self.port = port # port for network problem, if necessary
    self.seed = hashlib.sha256(self.token + self.probname + seed).hexdigest()
     #secure seed to use in problems for random number generation

  # deploy_static
  # deploys a list of files to
  # /home/teamuser/problems/problemname_token/ on server
  # with teamuser:teamuser 770 perms
  # files may be either:
  # * a path to a local file, which will be deployed with the same basename
  # * a StringIO object with a .name attribute specifying the remote basename
  # returns:
  # * a mapping from original filenames to the file names used in the
  #   problem instance
  def deploy_static(self, files, rename = None):

    if not rename: rename = {}
    instname = self.probname # instance name
    instdir = os.path.join('/home',self.teamuser, 'problems',instname)
    self.server.makedirs(instdir)
    self.server.chown(instdir, 'root', self.teamuser)
    self.server.chmod(instdir, '755')

    print("deploy static start")
    mapping = {}
    for n in files:
      if isinstance(n,StringIO.StringIO):
        mapping[n.name] = os.path.join(instdir,rename[n.name] if n.name in rename else n.name)
        self.server.push_file(n,mapping[n.name],perm="550",owner=self.teamuser)
      else:
        mapping[n] = os.path.join(instdir,rename[n] if n in rename else n)
        self.server.push_file(n,mapping[n],perm="550",owner=self.teamuser)

    print(mapping)
    print("deploy static okay")

    return mapping

  # deploy_service
  # creates a new user for the service
  # copies servicebin and servicefiles into serviceuser's homedir on server
  # with perms 640
  # deploy_static's teamfiles, which may or may not include servicebin
  # registers the copy of servicebin in /home/serviceuser with xinetd
  # returns the name of the serviceuser, so that
  # generator can tweak file perms of files in serviceuser's homedir
  # (eg, set setuid bits)

  def deploy_service(self, servicebin, servicefiles, teamfiles, rename = None):
    if not rename: rename = {}
    start = time.time()
    print("deploy static %f"%(time.time() - start))
    static_mapping = self.deploy_static(teamfiles, rename=rename)
    service_mapping = {}
    serviceuser = secure_filename('%s_%s' % (self.probname,self.token))
    print("add user %f"%(time.time() - start))
    self.server.add_user(serviceuser)
    instdir = os.path.join('/home',serviceuser)
    if not servicebin in servicefiles:
      servicefiles.append(servicebin)

    print("push files %f"%(time.time() - start))
    for f in servicefiles:
      if isinstance(f,StringIO.StringIO):
        if hasattr(f,"name"):
          name = rename[f.name] if f.name in rename else f.name
          deployedto = os.path.join(instdir,name)
          self.server.push_fo(f,deployedto)
        else:
          raise Exception("StringIO object with no name field(required)")

      else: # path string to file to push
        name = rename[f] if f in rename else f
        deployedto = os.path.join(instdir,os.path.basename(name))
        self.server.push_file(f,deployedto)

      service_mapping[name] = deployedto
      self.server.chown(deployedto,serviceuser,serviceuser)
      self.server.chmod(deployedto,"540")

    # do network problem setup stuff
    # copied with modification from
    # problem_api.py:add_network_problem_instance
    problem_path = os.path.join(problem_api.network_problem_folder, self.probname)
    token_path = os.path.join(problem_path, self.token)
    servicebinname = servicebin.name if isinstance(servicebin, StringIO.StringIO) else servicebin
    servicebinname = rename[servicebinname] if servicebinname in rename else servicebinname
    servicebinname = os.path.basename(servicebinname)

    binpath = os.path.join(instdir,servicebinname)

    print("push other things %f"%(time.time() - start))
    self.server.push_fo(StringIO.StringIO(serviceuser), token_path + '_user', '0700')
    self.server.push_fo(StringIO.StringIO(binpath), token_path + '_script', '0700')

    return serviceuser, service_mapping, static_mapping


  def deploy_remote_c(self, source = None, key = None, flags = None, share_binary = True, share_source = False):
    if not flags: flags = []
    if source is None:
      source = self.probname + '.c'
    if key is None:
      key = ioctf.generate_key(self.probname, self.token)


    flagstr = " ".join(flags)

    with ioctf.TempFile(prefix=self.probname) as binary:
      ioctf.local_exec('gcc %s -o %s %s' % (source, binary, flagstr))

      keyfile = StringIO.StringIO(key)
      keyfile.name = 'key'

      shared_files = []
      shared_files += [binary] if share_binary else []
      shared_files += [source] if share_source else []

      _, mapping, team_mapping = self.deploy_service(binary, [keyfile], shared_files, rename={binary: self.probname})

      replacements = {
        'server': self.server.url,
        'port': str(self.port),
        'servicebinary': mapping[self.probname]
      }

      if share_binary:
        binarystr = problem_api.load_template(binary, {})
        replacements['binary'] = problem_api.publish(self.probname, self.probname, binarystr)
        replacements['shellbin'] = team_mapping[binary]
      if share_source:
        sourcestr = problem_api.load_template(source, {})
        replacements['source'] = problem_api.publish(self.probname, source, sourcestr)
        replacements['shellsrc'] = team_mapping[source]

    return {
      'key': key,
      'replacements': replacements
    }

  def deploy_remote_python(self, realkey = None, keypattern = None, defaultkey = None, source = None,
                           shownsource = None, replacements = None, share_source = True, servicefiles = None):
    if not replacements: replacements = {}
    if not servicefiles: servicefiles = []
    assert(realkey != None)
    assert(keypattern != None)
    assert(defaultkey != None)
    if source is None:
      source = self.probname + '.py'
    if shownsource is None:
      shownsource = source

    key = ioctf.generate_key(self.probname, self.token, size=16)
    realkey = realkey % key
    key = keypattern % key

    replacements[defaultkey] = key
    script = problem_api.load_template(source, replacements)

    scriptfile = StringIO.StringIO(script)
    scriptfile.name = source

    generic_script = problem_api.load_template(source, {})
    generic_scriptfile = StringIO.StringIO(generic_script)
    generic_scriptfile.name = shownsource

    replacements = {
      'server': self.server.url,
      'port': str(self.port)
      }

    print("deploy_service start")
    _,_,mapping = self.deploy_service(scriptfile, servicefiles, [generic_scriptfile] if share_source else [])
    print("deploy_service end")

    print("share_source start")
    if share_source:
      source_link = problem_api.publish(self.probname, generic_scriptfile.name, generic_script)
      replacements['source'] = source_link
      replacements['shellsrc'] = mapping[generic_scriptfile.name]
    print("share_source end")

    return {
      'key': realkey,
      'replacements': replacements
    }
