import os
import random
from ioctf import server
import string
import StringIO
import random
from werkzeug.utils import secure_filename

website = False

def shell_server():
  return server.Server(server.shell_server_ip)

# pushes to webserver
def publish_file(problem_name, file_path, subfolder = '', name=''):
  c = ''
  with open(file_path) as f:
    c = f.read()
  deploy_name = name if name else os.path.basename(file_path)
  return publish(problem_name, deploy_name, c, subfolder)

# pushes to webserver
def publish(problem_name, name, contents, subfolder = ''):
  if not website:
    return 'file://' + os.path.join(subfolder, name)
  else:
    from werkzeug.utils import secure_filename
    import problem
    problem_name = secure_filename(problem_name)

    path = os.path.join(problem.root_web_path, 'problems', problem_name, subfolder, name)

    try:
      os.makedirs(os.path.dirname(path))
    except:
      pass
    print(path)
    with open(path, 'w+') as f:
      f.write(contents)
    return path[len(problem.root_web_path):]


network_problem_folder = '/network-problems/'

def register_port(problem_name, port_number):
  """ Assigns a *single* port to a problem, port_number is ignored """
  """"from common import db
  low_port = 50000
  high_port = 50500
  problem_name = normalize_name(problem_name)

  with common.setup_lock:

    previous_port = db.ports.find_one({'problem_name': problem_name})
    if previous_port:
      port_number = previous_port['number']
    else:
      allocated_ports = set([port['number'] for port in list(db.ports.find())])
      port_number = random.randint(low_port, high_port)
      while port_number in allocated_ports:
        port_number = random.randint(low_port, high_port)

    # Remove other ports that may be assigned to this problem
    db.ports.remove({'problem_name': problem_name})
    db.ports.save({'number': port_number, 'problem_name': problem_name})"""

  port_number = random.randint(10000, 60000)
  return port_number

def port_for_problem(problem_name):
  from common import db
  problem_name = normalize_name(problem_name)
  port = db.ports.find_one({'problem_name': normalize_name(problem_name)})
  return None if not port else port['number']

def normalize_name(problem_name):
  return secure_filename(problem_name).lower()

def setup_network_problem(problem_name, port):
  problem_name = normalize_name(problem_name)
  port = register_port(problem_name, port)
  problem_path = os.path.join(network_problem_folder, problem_name)
  remote_demultiplexer_path = os.path.join(network_problem_folder, 'demultiplexer.py')

  xinetd_config = StringIO.StringIO("""service %s
{
    disable = no
    socket_type = stream
    protocol    = tcp
    wait        = no
    user        = root
    bind        = 0.0.0.0
    server      = %s
    type        = UNLISTED
    port        = %d
    log_on_failure  += USERID
    server_args = %s
}""" % (problem_name, remote_demultiplexer_path, port, problem_path))

  server = shell_server()
  server.makedirs(problem_path)
  server.run('chmod 0700 %s' % problem_path)

  server.push_fo(xinetd_config, '/etc/xinetd.d/%s' % problem_name, perm = '0744')
  server.run('service xinetd restart')

  return True

def setup_remote_python():
  return

def add_network_problem_instance(problem_name, token, script_path, user):
  problem_name = normalize_name(problem_name)
  token = secure_filename(token)

  problem_path = os.path.join(network_problem_folder, problem_name)
  token_path = os.path.join(problem_path, token)

  server = shell_server()
  server.push_fo(StringIO.StringIO(user), token_path + '_user', '0700')
  server.push_fo(StringIO.StringIO(script_path), token_path + '_script', '0700')

def load_template(path, replacements):
  template = ''
  with open(path) as f:
    template = f.read()

  for k,v in replacements.iteritems():
    template = string.replace(template, k, v)

  return template

def setup_flask_app(problem_name, web_server, port, extra_files = None, problem_user = None):
  if not extra_files: extra_files = []
  shell = shell_server()

  problem_name = normalize_name(problem_name)
  port = register_port(problem_name, port)

  if not problem_user:
    problem_user = problem_name

  problem_path = os.path.join('/home', problem_user)

  xinetd_config = StringIO.StringIO("""service %s
{
    disable     = no
    type        = UNLISTED
    socket_type = stream
    server      = /usr/local/bin/uwsgi
    server_args = --chdir %s -w web_server:app --protocol=http --logto /dev/null
    port        = %d
    bind        = 0.0.0.0
    wait        = yes
    user        = %s
    log_on_failure  += USERID
}""" % (problem_name, problem_path, port, problem_user))

  shell.add_user(problem_user)
  shell.push_fo(StringIO.StringIO(web_server), os.path.join(problem_path, 'web_server.py'), '0711', problem_user, problem_user)
  shell.push_folder('templates', problem_path, '0700', problem_user, problem_user)

  for path, perm in extra_files:
    shell.push_file(path, os.path.join(problem_path, path), perm, problem_user, problem_user)

  shell.push_fo(xinetd_config, '/etc/xinetd.d/%s' % problem_name, perm = '0744')
  shell.run('service xinetd restart')
  return problem_user, port
