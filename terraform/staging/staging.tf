# This config is largely influenced by the AWS Two Tier Example
# https://github.com/hashicorp/terraform/blob/master/examples/aws-two-tier/main.tf

# AWS Specific config (single region)
provider "aws" {
    access_key = "${var.access_key}"
    secret_key = "${var.secret_key}"
    region = "${var.region}"
}

# Create a VPC (private netork ) to launch our instances into
resource "aws_vpc" "staging" {
    cidr_block = "${var.vpc_cidr}"
}

# Create an internet gateway to give our subnet access to the outside world
resource "aws_internet_gateway" "staging" {
    vpc_id = "${aws_vpc.staging.id}"
}

# Grant the VPC internet access on its main route table
resource "aws_route" "internet_access" {
    route_table_id         = "${aws_vpc.staging.main_route_table_id}"
    destination_cidr_block = "0.0.0.0/0"
    gateway_id             = "${aws_internet_gateway.staging.id}"
}

# Create a public facing subnet to launch our instances into
# Maps public ip automatically (every instance gets a public ip)
resource "aws_subnet" "staging_public" {
    vpc_id                  = "${aws_vpc.staging.id}"
    cidr_block              = "${var.public_subnet_cidr}"
    map_public_ip_on_launch = true
}

# Default security group to access instances over SSH, HTTP, and HTTPS
resource "aws_security_group" "staging_web" {
    name        = "staging_web"
    description = "Allows SSH, HTTP, HTTPS to staging web servers"
    vpc_id      = "${aws_vpc.staging.id}"

    # SSH access from anywhere
    ingress {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    # HTTP access from anywhere
    ingress {
        from_port   = 80
        to_port     = 80
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    # HTTPS access from anywhere
    ingress {
        from_port   = 443
        to_port     = 443
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    # outbound internet access
    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

# Security group for webservers to access to database servers
resource "aws_security_group" "staging_db_access" {
    name        = "staging_db_access"
    description = "Identifies webservers allowed acess the database"
    vpc_id      = "${aws_vpc.staging.id}"
}

# Database security group. Only allows SSH, Mongo, outbound
resource "aws_security_group" "staging_db" {
    name        = "staging_db"
    description = "Allows SSH from web, and Mongo access from web servers"
    vpc_id      = "${aws_vpc.staging.id}"

    # SSH access from anywhere
    ingress {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    
    # Mongo access only from webservers
    ingress {
        from_port   = 27017
        to_port     = 27017
        protocol    = "tcp"
        security_groups = ["${aws_security_group.staging_db_access.id}"]
    }

    # outbound internet access
    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

# Key which will be inserted in the instances
resource "aws_key_pair" "auth" {
    key_name   = "${var.key_name}"
    public_key = "${file(var.public_key_path)}"
}

# Create Elastic IP for web server
resource "aws_eip" "web" {
    instance = "${aws_instance.web.id}"
    vpc = true
}

resource "aws_instance" "web" {
    # The connection block tells our provisioner how to communicate with the
    # instance.  Will use the local SSH agent for authentication.
    connection {
        user = "${var.user}"
    }

    ami = "${lookup(var.amis, var.region)}"
    instance_type = "${var.web_instance_type}"
    availability_zone = "${var.availability_zone}"

    # The name of our SSH keypair we created above.
    key_name = "${aws_key_pair.auth.id}"

    # Public Security group to allow HTTP, HTTPS and SSH access
    vpc_security_group_ids = ["${aws_security_group.staging_web.id}",
        "${aws_security_group.staging_db_access.id}"]

    # Launch into the internet facing subnet
    subnet_id = "${aws_subnet.staging_public.id}"

    # Fix private_ip
    private_ip = "${var.web_private_ip}"

    tags {
        Name = "${var.web_name}"
        Year = "${var.year}"
    }
}


# Create Elastic IP for db server to simplify configuration
resource "aws_eip" "db" {
    instance = "${aws_instance.db.id}"
    vpc = true
}


# Create EBS volume for MongoDB data and journal
# having them on the same device allows backup with --journal
resource "aws_ebs_volume" "db_data_journal" {
    availability_zone = "${var.availability_zone}"
    size = "${var.db_ebs_data_size}"
    tags {
        Name = "${var.db_ebs_data_name}"
        Year = "${var.year}"
    }
}

# Attach data and journal volume to the db instance
resource "aws_volume_attachment" "db_data_journal" {
  device_name = "${var.db_ebs_data_device_name}"
  volume_id = "${aws_ebs_volume.db_data_journal.id}"
  instance_id = "${aws_instance.db.id}"
}


resource "aws_instance" "db" {
    connection {
        user = "${var.user}"
    }

    ami = "${lookup(var.amis, var.region)}"
    instance_type = "${var.db_instance_type}"
    availability_zone = "${var.availability_zone}"
    key_name = "${aws_key_pair.auth.id}"
    vpc_security_group_ids = ["${aws_security_group.staging_db.id}"]
    subnet_id = "${aws_subnet.staging_public.id}"
    private_ip = "${var.db_private_ip}"

    tags {
        Name = "${var.db_name}"
        Year = "${var.year}"
    }

}
