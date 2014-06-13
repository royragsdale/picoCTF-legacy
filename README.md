CTF-Platform
============

A genericized version of picoCTF 2013 that can be easily adapted to host 
CTF or programming competitions.

picoCTF has been tested extensively on Ubuntu 12.04 LTS but should work 
on just about any "standard" Linux distribution. It would probably even 
work on Windows. MongoDB must be installed; all default configurations 
should work. There is no schema.

Web Server
------------

Nginx was our web server of choice for hosting picoCTF. Apache would 
work just fine as the configuration is quite simple. All of the pages on 
the site are static .html files with corresponding javascript files. 
These should all be served by Nginx from a standard web server directory 
such as /srv/http/main-site/ or /var/www/main-site/ etc. Our 
configuration involved aliasing so that links such as picoctf.com/about 
would actually serve picoctf.com/about.html; this isn't essential to get 
the site running, but if it isn't configured that way most of the links 
in the site won't load the correct page.

The simplest way to view problems is on the problems.html page. It is a 
text-based display of all the problems a user has unlocked. These 
problems are ordered by the point value that each problem is worth.

AJAX API
------------

A Python API handles all interaction with the database (MongoDB). The 
API is built on top of the Flask microframework. The main API file is 
api.py which can be started by running 'python api.py'. We have only 
tested and deployed the service under Python 2.7 but plan to move to 3.0 
in the near future. We suspect the changes should be minimal. 

In a production environment you will want to configure a WSGI wrapper 
service such as gunicorn to manage the API for you. This supports 
multithreading and crash resilience. For testing, invoking 'python 
api.py' is perfectly acceptable.

The most important step in running the API is changing the 
SESSION_COOKIE_DOMAIN and secret_key in mister.config, the main 
configuration file. The secret key should be a valid HEX string such as 
3f53ec2a47. This is the key that will encrypt the cookies that are sent 
to the users; this key should be secret. The session domain is by 
default 127.0.0.1 . This will be fine if you are testing on your local 
machine, but if you deploy it to a server it will have to either be set 
to the server's IP address or the FQDN of the server. In our case the 
session cookie domain was 'picoctf.com'.

Ensure that the SESSION_COOKIE_DOMAIN matches the domain on which 
users access the site according to the same-origin policy. 127.0.0.1 is 
not compatible with localhost.


Database
------------

Problems are defined in the MongoDB collection 'problems'. A collection 
in MongoDB is analogous to a table in SQL-based systems. You can see 
some examples of these in the 2013-Problems repository (the JSON files). 
Keep in mind that you do not necessarily need to transfer these files to 
your server. They are descriptions of documents to add to the problems 
collection (MongoDB stores documents as [BSON](http://bsonspec.org/) 
which is a superset of JSON). See the below example for how to add one 
of these problem to an instance of the CTF Platform.

The required information for each problem document is the 'basescore' 
(number of points it is worth), 'desc', 'displayname', 'hint', 'pid' 
(any unique string will work), and 'grader'. The 'grader' field is the 
name of a script that should be located in api/graders/ that the api 
invokes to grade whether or not a submitted key is correct. The grader 
should have a function in it called 'grade' that takes the 'tid' of the 
team and the submitted key as its 2 parameters and returns a boolean and 
a string message as the return value. Looking at line 95 of problem.py 
should clear things up if you are confused.

An example problem document:

    {
        "autogen" : false,
        "basescore" : 20,
        "desc" : "<p>\nAfter opening the robot's front panel...</p>",
        "displayname" : "Failure to Boot",
        "grader" : "bluescreen.py",
        "hint" : "It might be helpful to Google™ the error.",
        "pid" : "512a8622b393a33f2cf9b37f",
        "threshold" : 0,
        "weightmap" : {}
    }

Where bluescreen.py might be:

    def grade(team,key):
        if key.upper().find('FAT') != -1:
            return True, 'Correct'
        else:
            return False, 'Incorrect'                        
                                              
So to insert this problem and be able to view it in the Basic Problem 
Viewer you need to 1) insert the problem document into the problems 
collection and 2) add bluescreen.py to the folder api/graders . If you 
are unfamiliar with using the mongo shell, here's how you would add the 
document under the simplest configuration:

     $ mongo ctf
        > db.problems.insert({"autogen" : false,
        "basescore" : 20,
        "desc" : "<p>\nAfter opening the robot's front panel...</p>",
        "displayname" : "Failure to Boot",
        "grader" : "bluescreen.py",
        "hint" : "It might be helpful to Google™ the error.",
        "pid" : "512a8622b393a33f2cf9b37f",
        "threshold" : 0,
        "weightmap" : {}
        });

Problem descriptions are cached in Memcached for each user for an hour 
by default. So for all users to see the newly added problem you may need 
to restart Memcached:

    $ sudo service memcached restart

Setup and Configuration
------------

To install all the dependencies run scripts/install_deps.sh . 

For a sample Nginx configuration, check out config/main-site . This 
configuration is typically placed in /etc/nginx/sites-enabled/ . Check 
out the official [Nginx Beginner's 
Guide](http://nginx.org/en/docs/beginners_guide.html) for more 
information. Nginx must be properly configured in order to route /api/ 
requests to the Python API.

To get the indexes up for MongoDB, use the init_mongo.js script. If the 
database is called "ctf", you would run: mongo ctf init_mongo.js

Contact
------------

We are happy to help, but no support is guaranteed.

Authors: Collin Petty, Peter Chapman

Copyright: Carnegie Mellon University

License: MIT

Maintainers: Collin Petty, Peter Chapman, Jonathan Burket

Credits: David Brumley, Collin Petty, Peter Chapman, Tyler Nighswander, Garrett Barboza

Email: collin@cmu.edu, peter@cmu.edu, jburket@cmu.edu


