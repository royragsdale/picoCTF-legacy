# Deployment Notes

Some notes that are relevant to deploying with Terraform and Ansible.

## Goals
1. Automated
2. Robust
3. Configurable

## Technology
1. AWS: Infrastructure
2. Terrafrom: Infrastructure Orchestration
3. Ansible: Provisioning/Configuration/Administration

#### DB auth fails

- Check client version, we are using MongoDB 3.2 which changed auth from "MONGODB-CR" to "SCRAM-SHA-1" and changed the auth schema
    - MongoDB shell version: 3.2.1 should work
    - latest pymongo should work
    - mongod.log will have a line like the following if this is the issue
       - `Failed to authenticate cocoAdmin@admin with mechanism MONGODB-CR: AuthenticationFailed MONGODB-CR credentials missing in the user document`
    - relevant [Stack Overflow](http://stackoverflow.com/questions/29006887/mongodb-cr-authentication-failed)

#### Ansible host unreachable

- There are a few possible reasons ansible may be unable to ssh to the specified hosts
    - Check the public Elastic IP Address has not changed by comparing the output of terraform (ground truth on infrastructure) with the ansible inventory.
        - `terrraform show`
        - If there is a difference, update the inventory with the corret value from the `terraform` output, and retry.
    - If the IP addresses are correct, it may be that host keys are incorrect as in the case of a new server being created.
        - ansible error: `UNREACHABLE! => {"changed": false, "msg": "ERROR! SSH encountered an unknown error during the connection.`
        - confirm with a manual ssh connection
            - `ssh -i ~/.ssh/pico_staging_rsa admin@<IP ADDRESS>`
            - gives: `REMOTE HOST IDENTIFICATION HAS CHANGED!`
        - Fix by removing the offending key:
            - `ssh-keygen -f "/home/roy/.ssh/known_hosts" -R <IP ADDRESS>`
        - confirm with another manual ssh (accept the new host key)
