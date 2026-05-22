provider "aws" {
  region = var.region
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
  ami           = "ami-04f76ebf532020fa0" # Ubuntu 22.04 in region eu-central-1
  instance_type = "t2.micro"              # AWS Free Tier
  subnet_id     = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  # cloud-init transfer
  user_data = file("cloud-init.yaml")

  tags = {
    Name = "${var.prefix}-vm"
  }
}