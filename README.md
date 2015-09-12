picoCTF-platform
============================

The picoCTF-platform is the infrastructure which is used to run [picoCTF](https://picoctf.com/). The platform is designed to be easily adapted to other CTF or programming competitions.


Quick Start
------------

1. git clone --recursive https://github.com/picoCTF/picoCTF-platform.git
2. cd picoCTF-platform
3. vagrant up
4. Navigate to http://192.168.2.2/
5. Register an account (this user will be the site administrator)

Current Development
------------

The picoCTF-platform is actively being developed towards version 3 and additional documentation on significant platform changes are located under [documentation](./documentation).

Project Overview
------------

The **picoCTF-platform** is a superproject composed of three distinct git [submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) (this is why you must use --recursive when you clone the project). The submodules are [picoCTF-web](https://github.com/picoCTF/picoCTF-web), [picoCTF-shell-manager](https://github.com/picoCTF/picoCTF-shell-manager), and [picoCTF-problems](https://github.com/picoCTF/picoCTF-problems).  This repository (picoCTF-platform) consists of the necessary scripts and configurations to pull these three components together into a fully functional deployment for demonstration or development. In order to achieve this reproducible environment the project leverages [Vagrant](https://www.vagrantup.com/).

The **picoCTF-web** project consists of the competitor facing web site, the api for running a CTF, as well as management functionality for CTF organizers.  This is deployed (via the [Vagrantfile](./Vagrantfile)) as a virtual machine (web) at http://192.168.2.2/.  For more information on this component of the picoCTF-platform please consult the documentation in the [repository](https://github.com/picoCTF/picoCTF-web).

The **picoCTF-shell-manager** project consists of the hacksport library and the shell_manager utility which are used to create, package, and deploy challenges for use in a CTF. The [Vagrantfile](./Vagrantfile) uses this to deploy a second virtual machine (shell) at 192.168.2.3. This shell-server is where challenge instances will be deployed and is also where competitors are provided an account for use in solving the challenges. For more information on this component of the picoCTF-platform please consult the documentation in the [repository](https://github.com/picoCTF/picoCTF-shell-manager).

The **picoCTF-problems** project consists of CTF challenges that are compatible with picoCTF-platform.  These challenges can be easily shared and deployed, or adapted for use in a CTF. When deployed the picoCTF-platform loads some example problems to demonstrate the features of both the web server and the shell-server. For more information on this component of the picoCTF-platform please consult the documentation in the [repository](https://github.com/picoCTF/picoCTF-problems).

Contact
------------

We are happy to help but no support is guaranteed.

Authors: Tim Becker, Chris Ganas

Copyright: Carnegie Mellon University

License: MIT

Maintainers: Roy Ragsdale

Credits: David Brumley, Tim Becker, Chris Ganas, Peter Chapman, Jonathan Burket

Email: rragsdale@cmu.edu

Additional Credits
------------

v1 Credits: Collin Petty, Tyler Nighswander, Garrett Barboza
