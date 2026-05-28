provider "aws" {
  region = var.region
}

# Динамічний пошук найсвіжішого образу Ubuntu 22.04 для твого поточного регіону
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Офіційний акаунт Canonical (творці Ubuntu)

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

# 1. Network (VPC) and Subnetwork (Subnet)
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true # Automatically issues public IP
}

# In AWS the Internet Gateway is needed so the server has Internet access
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public_rt.id
}

# 2. Security Group - NSG analogy
resource "aws_security_group" "web_sg" {
  name        = "${var.prefix}-sg"
  description = "Allow SSH and HTTP"
  vpc_id      = aws_vpc.main.id

  # Open port 22 for SSH
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Open port 5000 for web app
  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow access to Grafana
  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow access to Prometheus
  ingress {
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 30500
    to_port     = 30500
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 30080
    to_port     = 30080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow server to access Internet (downloading Docker etc)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 3. Server (EC2 Instance)
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id  # Тепер Terraform сам підставить правильний ID!
  instance_type = "m7i-flex.large"              # Безкоштовний сервер для регіону eu-north-1
  subnet_id     = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.web_sg.id]

root_block_device {
  volume_size           = 30
  volume_type           = "gp3"
  delete_on_termination = true # Диск видалиться разом із сервером
}

  # cloud-init transfer
  user_data = file("cloud-init.yaml")

  tags = {
    Name = "${var.prefix}-vm"
  }
}