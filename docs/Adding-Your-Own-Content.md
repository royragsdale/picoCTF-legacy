This section will cover how to create your own problems and bundles for the
picoCTF Platform. There are some step-by-step examples that you can
follow along with on the [Example Challenges Page](Example-Challenges).

## Creating a Problem

To create a problem, you must set up a directory with the appropriate files and package it
as a `.deb` using the shell\_manager. We will now outline how to do that.

### Problem Specification

A problem specification is a directory consisting of your problem files. The following files
are recognized and used by the shell\_manager.

| File name | Required | Description|
|-----------|----------|------------|
|problem.json| yes | This file will specify the core information about the problem, including the name, category, score, and so forth. The full specification can be found [here](Problem.json)|
|challenge.py| yes | This script will specify how problem generation should occur.  The full documentation for setting up this script can be found [here](Challenge.py).|
|requirements.txt| no |  Specifies pip requirements for your problem|
|install\_dependencies| no | A script that will be executed after installing your problem.|

Any other files in your problem directory are placed into your deb package as-is.

### Testing Your Problem

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

### Deploying Instances

As shown above, you can run `sudo shell_manager deploy my-problem` to deploy an instance of it.
You can use the `-n` parameter to specify the number of instances to deploy.
To make sure that it is running properly, you can run `sudo shell_manager status -p my-problem`.
The picoCTF-platform can be accessed to use `shell_manager` with `vagrant ssh`. 

### Enabling Problems

Deployed instances/bundles are not automatically enabled on the web server. An admin must first login and visit the Admin Management page. As mentioned in the [set up page](Set-Up), the first account you set up will be the site administrator.
Under the 'Shell Server' tab, problems can be added via the 'Load Deployment' button, and the status of such problems (whether they are loaded or not) can be checked via the 'Check Status' button. 
Problems can then be enabled or disabled for the competitors via the 'Manage Problems' tab.

## Creating a Bundle

To create your own bundle of problems, you must first have them installed as described above.
Then, create a `bundle.json` file following the specification described [here](Bundle.json).

Now, run `sudo shell_manager bundle bundle.json` to create your bundle deb file. This can be
distributed and installed in the same way that problems can.

### Deploying a Bundle

You can deploy an entire bundle of challenges by running `sudo shell_manager deploy -b bundle-name`.
The `-n` parameter can be used to specify the number of instances of each problem to deploy.