# Terrafrom Notes

These notes cover how we use Terraform to orchestrate our infrastructure on AWS. As a general rule of thumb, nothing should be created, configured, modified or changed in the web console. Every change should be codified, captured, version controlled and put into action with Terraform.

Simply this creates the boxes and wires them up, but does not configure them.

## Current Status

We are working towards stage 1.

1. Staging infrastructure fully controlled by Terraform.
2. Production infrastructure for picoCTF-3 controlled by Terrafrom.
3. Production infrastructure for picoCTF 2014 controlled by Terraform.
3. Production infrastructure for picoCTF 2013 controlled by Terraform.

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
- `secret.tfvars.example` : tracks the secret configuration variables that are kept out of version control. This can be copied to `secret.tfvars` and filled in to actually deploy this infrastructure.
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
