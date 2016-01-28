# Ansible Notes

These notes cover how we use Ansible to provision, configure, and administer our infrastructure on AWS. As a general rule of thumb, nothing should have to be done as a one off on the command line. Every dependency, configuration, process should be documented in code or a configuration and then applied using ansible.  This presumes that Terraform has already taken care of creating and hooking the necessary systems and services together.

Simply this takes blank boxes and makes them pico. Also manages running a competition.

## Current Status

We are working towards stage 1 with 2 and 3 in necessarily short order.

1. Staging infrastructure fully automated by Ansible.
    - MongoDB
    - picoCTF-web
    - picoCTF-shell
2. Play-test challenges deployed to staging infrastructure via Ansible.
3. Production infrastructure for picoCTF-3 automated by Ansible.
4. Production infrastructure for picoCTF 2014 automated by Ansible.
5. Production infrastructure for picoCTF 2013 automated by Ansible.

## Requirements
1. Necessary instances running (Terraform)
2. Inventory information (Terraform)
    - IP / SSH Key

## Setup 
1. Install
    - <http://docs.ansible.com/ansible/intro_installation.html#getting-ansible> 
    - pip option  
        - `sudo apt-get install python-pip`
        - `sudo pip install ansible`

