# Adding Your Own Content

This section will cover how to create your own problems and bundles for the
picoCTF Platform. There are some step-by-step examples that you can
follow along with on the [Example Challenges Page](examples/README.md).

## Creating a Problem

To create a problem, you must set up a directory with the appropriate files and package it
as a `.deb` using the shell\_manager. We will now outline how to do that.

### Problem Specification

A problem specification is a directory consisting of your problem files. The following files
are recognized and used by the shell\_manager.

| File name | Required | Description|
|-----------|----------|------------|
|problem.json| yes | This file will specify the core information about the problem, including the name, category, score, and so forth. The full specification can be found [here](problem-json-spec.md)|
|challenge.py| yes | This script will specify how problem generation should occur.  The full documentation for setting up this script can be found [here](challenge-py-spec.md).|
|requirements.txt| no |  Specifies pip requirements for your problem|
|install\_dependencies| no | A script that will be executed after installing your problem.|

Any other files in your problem directory are placed into your deb package as-is.

### Testing Your problem

When you think your challenge is ready, you should test it before packaging it as a deb file.
You can run `sudo shell_manager deploy -d my-problem-dir` to generate a test instance of the
problem. This test instance will not have an running services, but all of the files will be
generated and placed in a temporary directory. This deployment directory will be output
by the previous command, so you should verify that it looks as it should.

### Packaging Your Problem

Once you have your directory set up, you can run `sudo shell_manager package directory_name` to create
a deb package with your problem inside.

### Installing Your Problem

Since your problem is now just a deb package, you can now easily share your problem with others.
It can be installed by running `sudo dpkg -i my-problem.deb`.

### Deploying instances

As shown above, you can run `sudo shell_manager deploy my-problem` to deploy an instance of it.
You can use the `-n` parameter to specify the number of instances to deploy.
To make sure that it is running properly, you can run `sudo shell_manager status -p my-problem`.

## Creating a Bundle

To create your own bundle of problems, you must first have them installed as described above.
Then, create a `bundle.json` file following the specification described [here](bundle-json-spec.md).

Now, run `sudo shell_manager bundle bundle.json` to create your bundle deb file. This can be
distributed and installed in the same way that problems can.

### Deploying a Bundle

You can deploy an entire bundle of challenges by running `sudo shell_manager deploy -b bundle-name`.
The `-n` parameter can be used to specify the number of instances of each problem to deploy.
