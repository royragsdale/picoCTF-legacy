# Terrafrom Notes

These notes cover how we use Terraform to orchestrate our infrastructure on AWS. As a general rule of thumb, nothing should be created, configured, modified or changed in the web console. Every change should be codified, captured, version controlled and put into action with Terraform.

Simply this creates the boxes and wires them up, but does not configure them.

## Requirements
1. AWS account
2. Deployment specific IAM with `ACCESS_KEY_ID` and `SECRET_ACCESS_KEY`
3. Deployment account has access to the necessary permissions
    - AmazonEC2FullAccess

## Overview of Files
Within each environment (production, staging) you will find the following files.

### Terraform Configuration (`*.tf`)

Each primary Terraform configuration file creates and manages the following elements on AWS:

1. AWS configuration
2. Virtual Private Cloud (VPC) aka private network
3. Internet Gateway, Routes, Subnets
4. Security Groups aka firewall
5. Instances aka servers
6. Instance Related things like Elastic IP, and keys

### Other Files
- `outputs.tf` : a place to put important actionable attribute information you want readily at hand about the deployed infrastructure. Like IP addresses. These are shown at the end of every `terraform apply` or `terraform show`
- `terraform.tfvars` : tracks non-sensitive configuration variables.
- `variables.tf` : captures all the possible configurations. These will be filled in by the various `*.tfvars` files.

## Setup
1. Install
    - <https://www.terraform.io/intro/getting-started/install.html>
    - `unzip ~/down/terraform_0.6.9_linux_amd64.zip -d /usr/local/terraform`
    - Add to path

## Other Notes
- Error waiting for Volume (vol-XYZABC) to detach from Instance
    - This is caused when an instance with an attached volume attempts to mutate
    - Use `terrafrom taint aws_instance.XXX` to cause a full deletion and recreation
    - Check with `terraform plan` then if it makes sense apply with `terraform apply` 

## Staging Infrastructure

- This infrastructure will be used for play testing, integration, and development.
- It will allow a full end to end test that should match the publicly deployed environment.
- It will be internet accessible but is intended to be access controlled to prevent any compromise of the competition.

## Workflow
1. Make edits to the appropriate configuration file
2. Check what changes it will have
    - `terraform plan -var-file="secret.tfvars"`
    - look for things like improperly templated/applied variables
3. If everything looks good commit code explaining the changes
4. Apply the changes
    - `terraform apply -var-file="secret.tfvars"` 
5. Commit the newly modified `terraform.tfstate`

Note:  This will create the necessary server instances and configures networking but does not further provision or configure the servers.

## Common Tasks

### Rebuild a single server

1. Find resource name
    - `terraform show`
    - ex: `aws_instance.web`
2. Taint the resource
    - `terraform taint aws_instance.web`
    - this will only mark the server for recreation
3. Capture the plan
    - `terraform plan -var-file="secret.tfvars"`
    - this should show only the deletion of the instance and perhaps the modification of attached resources (eg: Elastic IP (eip), Elastic Block Storage (ebs)) that rely on the instance id
4. Commit the plan
    - `git add terraform.tfstate*`
    - `git commit -m "[PLAN ] - rebuild server aws_instance.web"`
    - this ensures that changes to infrastructure are tracked
5. Apply the plan
    - `terraform apply -var-file="secret.tfvars"`
    - this is the step that actually destroys the server and creates a new instance
6. Commit the results 
    - `git add terraform.tfstate*`
    - `git commit -m "[APPLY] - success rebuilding server aws_instance.web"`
    - this ensures that changes to infrastructure are tracked
7. Test ssh
    - `ssh -i ~/.ssh/pico_staging_rsa admin@52.72.97.197`
    - should likely fail due to host key change
8. Remove stale host key
    - `ssh-keygen -f "/home/user/.ssh/known_hosts" -R 52.72.97.197`
9. Re-provision/Configure
    - run the relevant ansible playbooks

### Quick Start
1. Generate SSH deployment key
    - `ssh-keygen -f ~/.ssh/picoCTF_production_rsa -C "admin@picoCTF_production" -N ""`
