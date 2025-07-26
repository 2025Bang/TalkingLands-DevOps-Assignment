provider "aws" {
  region = var.region
}

resource "aws_instance" "nginx_server" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name

  user_data = <<-EOF
              #!/bin/bash
              sudo apt update
              sudo apt install -y nginx
              echo "Deployed via Terraform." > /var/www/html/index.html
              systemctl start nginx
              EOF

  vpc_security_group_ids = [aws_security_group.nginx_sg.id]
  tags = {
    Name = "Terraform-Nginx"
  }
}

resource "aws_security_group" "nginx_sg" {
  name_prefix = "nginx-sg-"
  description = "Allow HTTP and SSH"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
