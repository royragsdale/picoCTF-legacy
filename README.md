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

AJAX API
------------

Database
------------

Setup and Configuration
------------
