""" The common module contains general-purpose functions potentially used by multiple modules in the system."""
__author__ = "Peter Chapman"
__copyright__ = "Carnegie Mellon University"
__license__ = "MIT"
__maintainer__ = ["Collin Petty", "Peter Chapman"]
__credits__ = ["David Brumely", "Collin Petty", "Peter Chapman", "Tyler Nighswander", "Garrett Barboza"]
__email__ = ["collin@cmu.edu", "peter@cmu.edu"]
__status__ = "Production"


from pymongo import MongoClient
from werkzeug.contrib.cache import MemcachedCache
import string, random

db = MongoClient('localhost', 27017)['ctf']
cache = MemcachedCache(['127.0.0.1:11211'])
admin_emails = None

log_output = 'print'  # 'print', or 'email'
log_level = ['ERROR']  # ERROR, INFO, or NONE


def esc(s):
    """Escapes a string to prevent html injection

    Returns a string with special HTML characters replaced.
    Used to sanitize output to prevent XSS. We looked at 
    alternatives but there wasn't anything of an appropriate 
    scope that we could find. In the long-term this should be 
    replaced with a proper sanitization function written by 
    someone else."""
    return unicode(s)\
        .replace('&', '&amp;')\
        .replace('<', '&lt;')\
        .replace('>', '&gt;')\
        .replace('"', '&quot;')\
        .replace("'", '&#39;')


def token():
    """Generate a token, should be random but does not have to be secure necessarily. Speed is a priority.
    """
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))


def sec_token():
    """Generate a secure token that is cryptographically secure.
    """
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))


def _write_log(msg, output):
    if output is 'print':
        print msg


def log(msg, level='ERROR', output='print'):
    if level in log_level:
        _write_log("%s - %s" %(level, msg), output)