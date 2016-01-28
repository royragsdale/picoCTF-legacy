
output "Staging Web Elastic IP address" {
    value = "${aws_eip.web.public_ip}"
}

output "Staging DB IP address" {
    value = "${aws_instance.db.public_ip}"
}
