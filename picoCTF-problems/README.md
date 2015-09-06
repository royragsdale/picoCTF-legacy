Problem Creation Guidelines
===========================

Problem Style Guide
-------------------
* Use full category names for both problem.json and directory structure, e.g. binary => Binary Exploitation
* Your problem's directory name should match the DEBIAN naming translation of your problem name, e.g. "CrashMe 1" => "crashme-1". This is useful as it becomes obvious how you would install the package from apt. The crashme-1 problem directory is then installed by apt install crashme-1.
* Your problem should have a **solve.py** script if possible. In the future we will be able to incorporate these as health checks for shell server deployments.
* Your problem must have a README.md that gives a brief description of the problem. This should contain some spoilers and give indication as to how the problem could be solved.


How to Test Problems
--------------------

* Bring up an instance of the shell server.


* Package your problem as a deb.


```sudo shell_manager package ~/problems/PROBLEM_NAME```

* Install your problem package.


```sudo dpkg -i ./PROBLEM.deb```


_If you have unmet dependencies run `sudo apt-get install -f`. dpkg won't manage this for you._

* Deploy a test instance of your problem.


```sudo shell_manager deploy -d PROBLEM_NAME```


You'll get a message similar to this:


```
Generating instance 0 of "simplecrash1".
Deploying instance 0 of "simplecrash1".
	Description: A vulnerable service is running on 1.1.1.1:62857.  If you can crash it, it will yield the key.  Source is available at <a href='//1.1.1.1/static/24ed9f1177224b4deb99d481c7be1640/simplecrash1.c'>simplecrash1.c</a>.
	Flag: 0c728d41472cb349decc90504aa4f4b3
	Deployment Directory: /opt/hacksports/staging/686786222331/deployed
The instance deployment information can be found at /opt/hacksports/staging/686786222331/0.json.
```

You should be particularly interested in the Deployment Directory.

* Interact with it and make sure it's working!


You are going to need root to access the deployment directory. It's also not unreasonable to do this whole process as root. Your solve.py script should also be working on this if applicable.

Problem Submission Guide
------------------------
Every problem should be created on a seperate branch. To submit your problem:


  1. Deploy an instance on the dev server for real. sudo shell_manager deploy PROBLEM_NAME
  2. Ensure your **solve.py** script works if applicable.
  3. Submit a pull request.

Problem Merge Guide
-------------------
1. Assign yourself the merge request.
3. Solve the problem on the shell server.
4. Review the problem.json
  1. Ensure the score is reasonable.
  2. Check for typos.
5. Merge into master.
