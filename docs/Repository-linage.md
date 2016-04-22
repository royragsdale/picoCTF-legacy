# Repository Lineage
This document captures some of the history behind the various picoCTF repositories and provides recommendations for transitioning.

## Background
Over it's history the picoCTF platform has evolved and been developed in a number of different settings. This has involved a number of different contributors and two competitions.  Between picoCTF 2013 and picoCTF 2014, the platform was re-written and re-released (as picoCTF-Platform-1 and picoCTF-Platform-2 respectively).

Following the 2014 competition significant functionality was added in order to support challenge deployment and a "shell_manager". This resulted in a proliferation of repositories, picoCTF-web, picoCTF-shell-manager, picoCTF-problems, all of which where pulled together as git submodules of picoCTF-platform. This made sense during the initial development of the discreet components, but introduced a significant amount of friction.  This complicated onboarding new contributors as well as managing a private version for live picoCTF competitions.

In order to reduce this friction and the confusingly large number of picoCTF repositories, we have unified the majority of existing code into this single repository, while making every attempt possible to preserve history. This includes:
1. picoCTF 2013 (version 1.0)
2. picoCTF 2014 (version 2.0)
3. Current Development (working towards 3.0)
    - picoCTF-platform
    - picoCTF-web
    - picoCTF-shell-manager
    - picoCTF-problems

## Transitioning
This should greatly simplify working with the picoCTF codebase, but here are some specific use cases to alleviate any difficulty in transitioning.

### Existing non-merged branches from old submodules
Since all the history is preserved and there are common commits across all possible repositories this is relatively straight forward. The high level steps are as follows:

1. Clone/Fork this repository
2. Add your "old" submodule repository as a remote
3. Re-write the paths in your fork
4. Rebase off of master
5. Push and submit a pull request

A concrete example:

    ```
    # 1. Clone your fork of the new picoCTF unified repository
    git clone git@github.com:royragsdale/picoCTF.git
    cd picoCTF

    # 2. Add "old" submodule repository as a remote and checkout the non-merged branch 
    git remote add old-picoCTF-web git@github.com:royragsdale/picoCTF-web.git
    git fetch old-picoCTF-web
    git checkout -b refactor_config old-picoCTF-web/refactor_config

    # 3. Use the appropriate `filter-branch` to re-write as a subdirectory (see below)
    git filter-branch --prune-empty --tree-filter 'if [ ! -e picoCTF-web ]; then mkdir picoCTF-web; git ls-tree --name-only $GIT_COMMIT | grep -v ^picoCTF-web$ | xargs -I files mv files picoCTF-web; fi'

    # 4. Rebase off of master
    rebase -i master

    # 5. Push the branch up to your copy of the new picoCTF unified repository
    push -u origin refactor_config

    # 6. Submit a pull request on github.com to <https://github.com/picoCTF/picoCTF>
    ```

### Forks of picoCTF-Platform-2
This version of the platform has been deprecated and is no longer receiving active development.  We certainly encourage anyone interested in the platform to try the latest version (`master`).  If you have an existing fork you should be unaffected by this repository consolidation. The state of the old repository has been preserved and can be easily accessed by checking out the `release-2.0` branch. Any bug fixes or not yet merged pull requests should be easily applied to that branch following a similar process to that listed above (rebasing off of `release-2.0` and no need to `filter-branch`).


## Unification process
Since this involved a large number of repositories and some non-standard git techniques, here are the primary steps that merged all this history together. Captured for historical purposes and to clarify what this change actually includes.

    ```
    # Start with the initial repository (2013)
    git clone https://github.com/picoCTF/picoCTF-Platform-1.git picoCTF
    cd picoCTF
    
    # "Release" it to a branch in case any future modifications are nessecary
    git checkout -b release-1.0

    # Clear the directory and merge in 2014
    git checkout master
    git rm -rf *
    gc -m 'Clean slate after picoCTF-Platform-1 "release"'
    git remote add pico2 https://github.com/picoCTF/picoCTF-Platform-2.git
    git fetch pico2
    git merge pico2/master
    # "Relase" it and clear directory for latest version
    git checkout -b release-2.0
    git rm -rf *
    git rm .gitignore
    gc -m 'Clean slate after picoCTF-Platform-2 "release"'

    # Pull the latest version and convert submodules to directories
    git remote add platform https://github.com/picoCTF/picoCTF-platform.git
    git fetch platform
    git merge platform/master
    git submodule deinit picoCTF-web
    git submodule deinit picoCTF-shell-manager
    git submodule deinit picoCTF-problems
    git rm picoCTF-*
    git commit -m "Removed all submodules with deinit"
    git rm .gitmodules
    git commit -m "Removed empty .gitmodules in preparation for unification"
    cd ..

    # For each submodule re-write the history to be as if it where always in a sub directory
    git clone https://github.com/picoCTF/picoCTF-web.git
    cd picoCTF-web
    git filter-branch --prune-empty --tree-filter 'if [ ! -e picoCTF-web ]; then mkdir picoCTF-web; git ls-tree --name-only $GIT_COMMIT | grep -v ^picoCTF-web$ | xargs -I files mv files picoCTF-web; fi'
    cd ..
    git clone https://github.com/picoCTF/picoCTF-shell-manager.git
    cd picoCTF-shell-manager
    git filter-branch --prune-empty --tree-filter 'if [ ! -e picoCTF-shell ]; then mkdir picoCTF-shell; git ls-tree --name-only $GIT_COMMIT | grep -v ^picoCTF-shell$ | xargs -I files mv files picoCTF-shell; fi'
    cd ..
    git clone https://github.com/picoCTF/picoCTF-problems.git
    cd picoCTF-problems
    git filter-branch --prune-empty --tree-filter 'if [ ! -e picoCTF-problems ]; then mkdir picoCTF-problems; git ls-tree --name-only $GIT_COMMIT | grep -v ^picoCTF-problems$ | xargs -I files mv files picoCTF-problems; fi'
    cd ../picoCTF

    # Merge the consituant sub directories back in (preserving history)
    git remote add web ../picoCTF-web/
    git fetch web
    git merge web/master
    git remote add shell ../picoCTF-shell-manager/
    git fetch shell
    git merge shell/master
    git remote add problems ../picoCTF-problems/
    git fetch problems
    git merge problems/master
    ga .
    gc -m "Normalize line endings as a part of repository unification"

    # Publish the repository and branches
    git remote add origin git@github.com:picoCTF/picoCTF.git
    git push -u origin master 
    git push --all origin
    ```

References:
- [Rewrite as subdirectory](http://stackoverflow.com/questions/4042816/how-can-i-rewrite-history-so-that-all-files-except-the-ones-i-already-moved-ar)
- [Work with submodules](http://stackoverflow.com/questions/1759587/un-submodule-a-git-submodule)
