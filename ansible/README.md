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

## Work Flow

### Provisioning (Staging)
This will be necessary after first brining up the infrastructure with Terraform
1. Check that the inventory (`staging`) matches what terraform has deployed.
    - This is required until we pull a dynamic inventory. 
    - `terraform show`
2. Check that syntax is correct and that playbooks and roles will all run
    - `ansible-playbook site.yml --check -i staging`
3. Run the playbook for the site with on the staging hosts
    - `ansible-playbook site.yml -i staging`

## Setup 
1. Install
    - <http://docs.ansible.com/ansible/intro_installation.html#getting-ansible> 
    - pip option  
        - `sudo apt-get install python-pip`
        - `sudo pip install ansible`

## Notes
- A side goal of using Ansible to automate the deployment of picoCTF is to clean up the configuration and development environment by contributing back to picoCTF-platform.
- A completely fresh deployment --check will fail on Install MongoDB meta package
    - this is because we are adding a new repository
