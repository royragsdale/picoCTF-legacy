from os.path import join

# secret used for deterministic deployment
DEPLOY_SECRET = "qwertyuiop"

# the externally accessable address of this server
HOSTNAME = "127.0.0.1"

# the url of the web server
WEB_SERVER = "http://127.0.0.1"

# the default username for files to be owned by
DEFAULT_USER = "hacksports"

# the root of the web server running to serve static files
# make sure this is consistent with what config/shell.nginx
# specifies.
WEB_ROOT = "/usr/share/nginx/html/"

# the root of the home directories for the problem instances
HOME_DIRECTORY_ROOT = "/home/problems/"

# list of ports that should not be assigned to any instances
# this bans the first ports 0-999 and 4242 for shellinaboxd
BANNED_PORTS = list(range(1000))+[4242]
