

output "web server address" {
    value = "${aws_instance.web.public_ip}"
}

output "backend server address" {
    value = "${aws_instance.backend.public_ip}"
}
