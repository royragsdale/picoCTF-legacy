picoCTF-shell-manager
=============

The picoCTF-shell-manager project consists of the hacksport library and the shell_manager utility which are used to create, package, and deploy challenges for use in a CTF.  During a competition these components can be used to run a shell-server where competitors are given access to the necessary command line tools and challenge related files.

This project has two goals:

1. To reduce the overhead associated with CTF challenges. Both prior to a competition in the challenge creation phase as well as during a competition in the system administration and management phase.
2. To allow reproducible challenge sharing and reuse.

Quick Start
------------
Though it is possible to use picoCTF-shell-manager as a stand alone component, it is best integrated with the rest of the [picoCTF-platform](https://github.com/picoCTF/picoCTF-platform). Please consult the Quick Start section of that repository for the simplest way to begin using this component.

Components
--------------

### hacksport

The hacksport library consists of a number of convenience functions related to challenge creations.  Specifically it provides the following features:

- Templating to support auto-generated challenge instances from a single problem source.
- Creation of Debian packages (.deb) from problem sources to ease sharing and reuse.
- Dependency management for challenges.
- Common challenge functionality such as random flags, file permissions, and remotely accessible services.

Examples of how to use the hacksport library to create picoCTF-platform compatible challenges are available in the [picoCTF-problems](https://github.com/picoCTF/picoCTF-problems) project as well as end-to-end examples in the [picoCTF-platform](https://github.com/picoCTF/picoCTF-platform) documentation.

### shell_manager

The shell_manager is the utility that a competition organizer would use to package, deploy, and manage challenge instances on a picoCTF-platform shell-server.  This tool builds on the hacksport library and problem specification metadata to turn challenge sources into deployed instances which a competitor will face in a CTF.

The [picoCTF-web](https://github.com/picoCTF/picoCTF-web) project integrates with the shell_manager utility to expose deployed challenges to competitors.

Contact
------------

We are happy to help but no support is guaranteed.

Authors: Tim Becker, Chris Ganas

Copyright: Carnegie Mellon University

License: MIT

Maintainers: Roy Ragsdale

Credits: David Brumley, Tim Becker, Chris Ganas

Email: rragsdale@cmu.edu

