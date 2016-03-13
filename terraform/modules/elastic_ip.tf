# This module configures persistent public IP addresses running picoCTF on AWS

###
# Elastic IP:
# This simplifies configuration and administration by allowing us to rebuild
# and recreate the servers while maintaining the same public ip.
###

# Create Elastic IP for web server
resource "aws_eip" "web" {
    instance = "${aws_instance.web.id}"
    vpc = true
}

# Create Elastic IP for shell server
resource "aws_eip" "shell" {
    instance = "${aws_instance.shell.id}"
    vpc = true
}
