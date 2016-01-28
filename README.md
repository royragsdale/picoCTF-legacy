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

### Ansible
1. Install
    - <http://docs.ansible.com/ansible/intro_installation.html#getting-ansible> 
    - pip option  
        - `sudo apt-get install python-pip`
        - `sudo pip install ansible`
