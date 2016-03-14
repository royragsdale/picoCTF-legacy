# The primary terraform configuration to deploy picoCTF to AWS

###
# This deployment configuration composes the referenced modules into a platform
# fully capable of hosting a CTF. Once deployed these machines should be
# provisioned, configured, and administered with the included ansible playbooks.
###

# AWS Specific config (single region)
provider "aws" {}
#    access_key = "${var.access_key}"
#    secret_key = "${var.secret_key}"
#    region = "${var.region}"
#}

# Add SSH key which will be inserted as authorized in each machine
resource "aws_key_pair" "auth" {
    key_name   = "${var.key_name}"
    public_key = "${file(var.public_key_path)}"
}

# Create virtual network
module "network" {
    source = "../modules/network"

    # Variables from varaibles.tf and terraform.tfvars
    vpc_cidr = "${var.vpc_cidr}"
    public_subnet_cidr = "${var.public_subnet_cidr}"
    availability_zone = "${var.availability_zone}"
}

# Create virtual firewall rules
module "security_groups" {
    source = "../modules/security_groups"

    # Variables output from prior modules
    vpc_id = "${module.network.vpc_id}"
}

# Create virtual machines
module "servers" {
    source = "../modules/servers"

    # Variables from varaibles.tf and terraform.tfvars
    user = "${var.user}"
    key_pair_id = "${aws_key_pair.auth.id}"

    ami = "${lookup(var.amis, var.region)}"
    availability_zone = "${var.availability_zone}"

    web_instance_type = "${var.web_instance_type}"
    web_private_ip = "${var.web_private_ip}"
    web_name = "${var.web_name}"

    shell_instance_type = "${var.shell_instance_type}"
    shell_private_ip = "${var.shell_private_ip}"
    shell_name = "${var.shell_name}"

    competition_tag = "${var.competition_tag}"
    env_tag = "${var.env_tag}"

    # Variables output from prior modules
    subnet_id = "${module.network.public_subnet_id}"
    sg_web_id = "${module.security_groups.sg_web_id}"
    sg_shell_id = "${module.security_groups.sg_shell_id}"
    sg_db_access_id = "${module.security_groups.sg_db_access_id}"
}

# Create persistent IP addresses
module "elastic_ip" {
    source = "../modules/elastic_ip"

    # Variables output from prior modules
    web_id= "${module.servers.web_id}"
    shell_id="${module.servers.shell_id}"
}

# Create persistent data stores
module "ebs_volumes" {
    source = "../modules/ebs_volumes"

    # Variables from varaibles.tf and terraform.tfvars
    availability_zone = "${var.availability_zone}"
    db_ebs_data_size = "${var.db_ebs_data_size}"
    db_ebs_data_device_name = "${var.db_ebs_data_device_name}"

    db_ebs_name = "${var.db_ebs_name}"
    competition_tag = "${var.competition_tag}"
    env_tag = "${var.env_tag}"

    # Variables output from prior modules
    # Host the web server and the database on the same machine
    db_host_id ="${module.servers.web_id}"
}

# Important variables to highlight at the end for provisioning the machines
# These should be added to the appropriate ansible inventory
output "Web Elastic IP address" {
    value = "${module.elastic_ip.web_eip}"
}
output "Shell Elastic IP address" {
    value = "${module.elastic_ip.shell_eip}"
}
