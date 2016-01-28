

output "Staging Web IP address" {
    value = "${aws_instance.web.public_ip}"
}

output "Staging DB IP address" {
    value = "${aws_instance.db.public_ip}"
}
