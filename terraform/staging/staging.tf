# This config is largely influenced by the AWS Two Tier Example
# https://github.com/hashicorp/terraform/blob/master/examples/aws-two-tier/main.tf

# AWS Specific config (single region)
provider "aws" {
    access_key = "${var.access_key}"
    secret_key = "${var.secret_key}"
    region = "us-east-1"
}

# Create a VPC to launch our instances into
# This is the private network where our instances will be created
resource "aws_vpc" "projectA" {
    cidr_block = "10.0.0.0/16"
}

# Create an internet gateway to give our subnet access to the outside world
# Otherwise they would not be internet accessible. GW is pointed to in vpc_route
resource "aws_internet_gateway" "projectA_gw" {
    vpc_id = "${aws_vpc.projectA.id}"
}

# Grant the VPC internet access on its main route table
resource "aws_route" "internet_access" {
    route_table_id         = "${aws_vpc.projectA.main_route_table_id}"
    destination_cidr_block = "0.0.0.0/0"
    gateway_id             = "${aws_internet_gateway.projectA_gw.id}"
}

# Create a public facing subnet to launch our web-accessible instances into
# This is also what we will use to apply security groups (aka fw rules)
# Maps public ip automatically
resource "aws_subnet" "projectA_public" {
    vpc_id                  = "${aws_vpc.projectA.id}"
    cidr_block              = "10.0.1.0/24"
    map_public_ip_on_launch = true
}

# Default security group to access instances over SSH and HTTP
resource "aws_security_group" "projectA_public" {
    name        = "projectA_public"
    description = "Allows SSH and HTTP to projectA public servers"
    vpc_id      = "${aws_vpc.projectA.id}"

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

    # outbound internet access
    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

# Security group id webservers to access to backend servers
resource "aws_security_group" "projectA_web" {
    name        = "projectA_web"
    description = "Identifies webservers to allow acess to backend"
    vpc_id      = "${aws_vpc.projectA.id}"
}

# Backend security group. Only allows SSH and outbound
resource "aws_security_group" "projectA_backend" {
    name        = "projectA_backend"
    description = "Allows SSH only"
    vpc_id      = "${aws_vpc.projectA.id}"

    # SSH access from anywhere
    ingress {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    
    # "Server" access only from webserver
    ingress {
        from_port   = 80
        to_port     = 80
        protocol    = "tcp"
        security_groups = ["${aws_security_group.projectA_web.id}"]
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

# Create Elastic IP for web
resource "aws_eip" "web" {
    instance = "${aws_instance.web.id}"
    vpc = true
}

resource "aws_instance" "web" {
    # The connection block tells our provisioner how to communicate with the
    # instance.  Will use the local SSH agent for authentication.
    connection {
        # The default username for our AMI
        user = "admin"
    }

    # Debian Jessie
    ami = "ami-116d857a"
    instance_type = "t2.micro"

    # The name of our SSH keypair we created above.
    key_name = "${aws_key_pair.auth.id}"

    # Public Security group to allow HTTP and SSH access
    vpc_security_group_ids = ["${aws_security_group.projectA_public.id}",
        "${aws_security_group.projectA_web.id}"]

    # Launch into the internet facing subnet
    subnet_id = "${aws_subnet.projectA_public.id}"

    # Run a remote provisioner on instance after creating it to install
    # install nginx and start it (port 80)
    provisioner "remote-exec" {
        inline = [
          "sudo apt-get -y update",
          "sudo apt-get -y install nginx",
          "sudo service nginx start"
        ]
    }
}

resource "aws_instance" "backend" {
    connection {
        user = "admin"
    }

    ami = "ami-116d857a"
    instance_type = "t2.micro"
    key_name = "${aws_key_pair.auth.id}"

    # Public Security group to allow HTTP and SSH access
    vpc_security_group_ids = ["${aws_security_group.projectA_backend.id}"]

    # Launch into the internet facing subnet
    subnet_id = "${aws_subnet.projectA_public.id}"
}
