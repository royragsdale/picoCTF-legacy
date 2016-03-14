# Variables to deploy a production instance of picoCTF to Amazon Web Services

###
# Overload defaults (variables.tf)
# This file allows easy overloading of the default values. Simple uncomment
# a line and make yourt desired change. At present since everything is commented
# out this file has no effect.
###

## AWS Credentials
# There are a number of methods for setting the AWS access credentials, choose
# one that fits your needs. See the authentication section of this page:
# https://www.terraform.io/docs/providers/aws/
#access_key = XXX
#secret_key = XXX

## SSH
#key_name = "pico_production"
#public_key_path = "~/.ssh/pico_production_rsa.pub"

## AWS Configuration
#region = "us-east-1"                   # Choose best for where your CTF is
#availability_zone = "us-east-1d"       # Determin using the AWS CLI
#user = "admin"                         # Default username for Debian AMIs

## Network
#vpc_cidr = "10.0.0.0/16"
#public_subnet_cidr = "10.0.1.0/24"
#web_private_ip = "10.0.1.10"           # Update ansible config if changed
#shell_private_ip = "10.0.1.11"         # Update ansible config if changed

## Instances
#web_instance_type = "t2.micro"         # For a live competition consider upgrading
#shell_instance_type = "t2.micro"       # For a live competition consider upgrading

## EBS Volumes
#db_ebs_data_size = "10"                # Size acordingly
#db_ebs_data_device_name = "/dev/xvdf"  # update ansible config if changed

## Tags                                 # These tags are for convenience
#competition_tag = "picoCTF"            # update acording to your needs
#env_tag = "production"
#web_name  = "picoCTF-web"
#shell_name = "picoCTF-shell"
#db_ebs_data_name = "picoCTF-db-ebs"
