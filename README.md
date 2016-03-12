# picoCTF

The picoCTF platform is the infrastructure which is used to run [picoCTF](https://picoctf.com/). The platform is designed to be easily adapted to other CTF or programming competitions.

Additional documentation can be found on the [wiki](https://github.com/picoCTF/picoCTF/wiki).

## Quick Start
1. `git clone https://github.com/picoCTF/picoCTF.git`
2. `cd picoCTF`
3. `vagrant up`
4. Navigate to http://192.168.2.2/
5. Register an account (this user will be the site administrator)

## Current Development

The picoCTF platform is actively being developed towards version 3 and additional documentation on significant platform changes are located on the [wiki](https://github.com/picoCTF/picoCTF/wiki).

If you are coming from [picoCTF-Platform-2](https://github.com/picoCTF/picoCTF-platform-2) please read the documentation on the wiki for [forks of picoCTF-Platform-2](https://github.com/picoCTF/picoCTF/wiki/Repository-linage#forks-of-picoctf-platform-2).

## Project Overview

This project is broken down into a few discreet components that compose to build a robust and featureful CTF platform that remains flexible for adaptation. Specifically the project is consists of the following:

1. [picoCTF-web](./picoCTF-web)
2. [picoCTF-shell](.//picoCTF-shell)
3. [picoCTF-problems](./picoCTF-problems)
4. automation for [provisioning](./ansible) and [AWS deployment](./terraform)
5. local deployment [examples](./vagrant)

### picoCTF-web
The competitor facing web site, the API for running a CTF, and the management functionality for CTF organizers.  The development [Vagrantfile](./Vagrantfile)) deploys picoCTF-web to a virtual machine (web) at http://192.168.2.2/.

### picoCTF-shell-manager
The tools to create, package, and deploy challenges for use with the picoCTF platform. This supports the deployment of auto-generated challenge instances and provides competitors shell access to aid in challenge solving. The development [Vagrantfile](./Vagrantfile) deploys the shell-server as a second virtual machine (shell) at http://192.168.2.3/. 

### picoCTF-problems
Example challenges that are compatible with the picoCTF platform.  These challenges can be easily shared, deployed, or adapted for use in a CTF.  The development [Vagrantfile](./Vagrantfile) installs these examples to the shell server and loads them into the web interface.

## Contact

We are happy to help but no support is guaranteed.

Authors: Tim Becker, Chris Ganas, Roy Ragsdale

Copyright: Carnegie Mellon University

License: [MIT](./LICENSE)

Credits: David Brumley, Tim Becker, Chris Ganas, Peter Chapman, Jonathan Burket

## Additional Credits

v1 Credits: Collin Petty, Tyler Nighswander, Garrett Barboza
