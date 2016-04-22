# Welcome to the picoCTF wiki!
Welcome to the picoCTF platform wiki!

Currently a work in progress as everything is transferred over.

## picoCTF platform Overview

The picoCTF platform has two main components: the shell servers and the web server. The Wiki mainly provides information on [setting up the platform](Set-Up) and [adding your own challenges](Adding-Your-Own-Content).

## Shell Servers

The shell servers are responsible for installing problems and generating instances. The problem
files and services will be available on this server only. A competition can have multiple
shell servers that each have their own sets of problems and instances. The `shell_manager`
utility is used to setup these servers.

Upon installing the `shell_manager`, each shell server will run its own web shell, allowing
users to connect to SSH from the website. The shell server is set up to authenticate users
using the same credentials as the web server.

## Web Server

The web server is responsible for running the web site and storing competition data. Here the
administrator can manage the problems and competition settings and monitor the progress of the
competitors.

The problems are loaded into the web server on the Shell Servers tab of the administrator page.
