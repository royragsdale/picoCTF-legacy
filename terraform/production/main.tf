# The primary terraform configuration to deploy picoCTF to AWS

###
# This deployment configuration pull in the top level modules and composes
# then into a platform fully capable of hosting a CTF.
###

# AWS Specific config (single region)
provider "aws" {
    access_key = "${var.access_key}"
    secret_key = "${var.secret_key}"
    region = "${var.region}"
}

# SSH key which will be inserted as authorized in each machine
resource "aws_key_pair" "auth" {
    key_name   = "${var.key_name}"
    public_key = "${file(var.public_key_path)}"
}



module "network" {
    source = "../modules/network.tf"
}

module "security_groups" {
    source = "../modules/security_groups.tf"
}

module "servers" {
    source = "../modules/servers.tf"
}

module "elastic_ip" {
    source = "../modules/elastic_ip.tf"
}

module "ebs_volumes" {
    source = "../modules/ebs_volumes.tf"
}

