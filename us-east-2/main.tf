terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}


provider "aws" {
  region  = "us-east-2"
}


resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  
   tags = {
    Name = "Jan"
  }
}


resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
  map_public_ip_on_launch = "true" 
  availability_zone = "us-east-2a"

  tags = {
    Name = "Jan-public"
  }
}

resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.2.0/24"
  map_public_ip_on_launch = "true"
  availability_zone = "us-east-2b" 
  
  tags = {
    Name = "Jan-private"
  }
}



resource "aws_security_group" "padrao" {
  name        = "padrao"

  vpc_id = aws_vpc.main.id

  ingress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  tags = {
    Name = "padrao"
  }
}


resource "aws_instance" "J1" {
  ami           = "ami-0a59f0e26c55590e9"
  instance_type = "t2.micro"
  subnet_id = "${aws_subnet.public.id}"
  vpc_security_group_ids = [aws_security_group.padrao.id]

  tags = {
    Name = "J1"
  }
}


resource "aws_instance" "J2" {
  ami           = "ami-0a59f0e26c55590e9"
  instance_type = "t2.micro"
  subnet_id = "${aws_subnet.public.id}"
  vpc_security_group_ids = [aws_security_group.padrao.id]

  tags = {
    Name = "J2"
  }
}


