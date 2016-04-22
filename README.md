# picoCTF fork

This an experimental fork of the [picoCTF-platform](https://github.com/picoCTF/picoCTF-platform).  For official updates please see the [picoCTF](https://github.com/picoCTF/) GitHub.

The major additions in this fork are automation for provisioning and deployment.  Additionally this repository unifies the git submodules into a single repository. For more information on how the repository was created please see the notes on [repository linage](./docs/Repository-linage.md) in the `docs` folder.

## Development Environment Quick Start

The following steps will use [Vagrant](https://www.vagrantup.com/) to get you  quickly up and running with the picoCTF platform by deploying the code base to two local virtual machines.

1. `git clone https://github.com/picoCTF/picoCTF.git`
2. `cd picoCTF`
3. `vagrant up`
4. Navigate to <http://192.168.2.2/>
5. Register an account (this user will be the site administrator)

This is a fork of the current development work on the  picoCTF platform, version 3.


## Project Overview

This project is broken down into a few discreet components that compose to build a robust and full featured CTF platform. Specifically the project is consists of the following:

1. [picoCTF-web](./picoCTF-web)
2. [picoCTF-shell](./picoCTF-shell)
3. [problems](./problems)
4. [ansible](./ansible)
5. [terraform](./terraform)
5. [vagrant examples](./vagrant)

### picoCTF-web
The competitor facing web site, the API for running a CTF, and the management functionality for CTF organizers.  The development [Vagrantfile](./Vagrantfile)) deploys picoCTF-web to a virtual machine (`web`) at <http://192.168.2.2/>. If you want to modify the look and feel of the website, this is the place to start.

### picoCTF-shell-manager
The tools to create, package, and deploy challenges for use with the picoCTF platform. This supports the deployment of auto-generated challenge instances and provides competitors shell access to aid in challenge solving. The development [Vagrantfile](./Vagrantfile) deploys the shell-server as a second virtual machine (`shell`) at <http://192.168.2.3/>. If you want to modify challenge deployment primitives, this is the place to start.

### picoCTF Compatible Problems
Example challenges that are compatible with the picoCTF platform.  These challenges can be easily shared, deployed, or adapted for use in a CTF.  The development [Vagrantfile](./Vagrantfile) installs these examples to the shell server and loads them into the web interface.  If you want to see how to create challenges or leverage the hacksport library, this is the place to start.

### Ansible for Automated System Administration
The tool we use to install, configure, deploy, and administer the picoCTF platform is [Ansible](https://www.ansible.com/).  This allows us to create flexible, parameterized, automated playbooks and roles that apply across development, staging, and production environments.  If you want to modify way the platform is configured, this is the place to start.

### Terraform for automated AWS deployment
The tool we use to codify our infrastructure as code is [Terraform](https://www.terraform.io/). This allows a simple process for creating, destroying, and managing a public deployment of the platform.  If you want to run a live competition on AWS, this is the place to start.

## Credits

This fork builds on the great work of the following:

- Authors: Tim Becker, Chris Ganas
- Credits: David Brumley, Tim Becker, Chris Ganas, Peter Chapman, Jonathan Burket
- Copyright: Carnegie Mellon University
- License: [MIT](./LICENSE)
