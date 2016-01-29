# picoCTF Deploy

This is a collection of scripts and tools to deploy the picoCTF platform to production for live competitions. It will roughly be a re-implementation of the [picoCTF-platform](https://github.com/picoCTF/picoCTF-platform) with the goal being that the robust standardization of configuration and automation of deployment will eventually be usable and releasable.

## Goals
1. Automated
2. Robust
3. Configurable

## Technology
1. AWS: Infrastructure
2. Terrafrom: Infrastructure Orchestration
3. Ansible: Provisioning/Configuration/Administration

## Status

Work in progress.

### Current
Working on building out the staging environment.  Even within that the only system with a relatively reasonable configuration is the database.

### Next
Whip web+shell code base into shape with regards to configuration and deployment.

## Setup

### AWS
1. IAM (Access Management)
    - Groups
        - admin: Admin access to web console with password
        - deploy: Command line access with ACCESS_KEY_ID and SECRET_ACCESS_KEY
    - Users
2. EC2 (Servers)
   - Based on the following code bases
        - web : <https://github.com/picoCTF/picoCTF-web>
        - shell : <https://github.com/picoCTF/picoCTF-shell-manager>
        - db : [mongoDB](https://docs.mongodb.org/ecosystem/platforms/amazon-ec2/)
        - coco : <https://github.com/codecombat/codecombat>
3. Route 53 (DNS)
4. CloudWatch (Alarms)


## Other Notes

### Bugs and Fixes

Temporarily placed here until there is a better place

#### DB auth fails

- Check client version, we are using MongoDB 3.2 which changed auth from "MONGODB-CR" to "SCRAM-SHA-1" and changed the auth schema
    - MongoDB shell version: 3.2.1 should work
    - latest pymongo should work [TODO] verify version
    - mongod.log will have a line like the following if this is the issue
       - `Failed to authenticate cocoAdmin@admin with mechanism MONGODB-CR: AuthenticationFailed MONGODB-CR credentials missing in the user document`
    - relevant [Stack Overflow](http://stackoverflow.com/questions/29006887/mongodb-cr-authentication-failed)


