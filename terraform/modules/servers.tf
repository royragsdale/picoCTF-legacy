# This module configures the virtual machines for running picoCTF on AWS

###
# Instance Configuration:
# There are two primary servers nessecary to run picoCTF (web, shell). This is
# the same configuration used in the default development setup.
###

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

resource "aws_instance" "shell" {
    connection {
        user = "${var.user}"
    }

    ami = "${lookup(var.amis, var.region)}"
    instance_type = "${var.shell_instance_type}"
    availability_zone = "${var.availability_zone}"
    key_name = "${aws_key_pair.auth.id}"

    # Public Security group to allow unfetttered acess from the internet
    vpc_security_group_ids = ["${aws_security_group.staging_shell.id}"]

    # Launch into the internet facing subnet
    subnet_id = "${aws_subnet.staging_public.id}"
    private_ip = "${var.shell_private_ip}"

    tags {
        Name = "${var.shell_name}"
        Year = "${var.year}"
    }
}

