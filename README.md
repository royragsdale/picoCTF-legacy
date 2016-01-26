# picoCTF Deploy

This is a collection of scripts and tools to deploy the picoCTF platform to production for live competitions. It will roughly be a re-implementation of the [picoCTF-platform](https://github.com/picoCTF/picoCTF-platform) with the goal being that the robust standardization of configuration and automation of deployment will eventually be usable and releasable.

## Goals
1. Automated
2. Robust
3. Configurable

## Technology
1. AWS
    - EC2 (Servers)
    - Route 53 (DNS)
    - IAM (Access Management)
2. Ansible
    - provisioning
    - administration
    - configuration
3. Terrafrom
    - infrastructure control 
