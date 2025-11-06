variable "ami_name" {
  description = "Name of the AMI to be created"
  type        = string
  default     = "bank-app-Codedeploy-packer-AMI-V2"
}

variable "instance_type" {
  description = "Instance type to use for building the AMI"
  type        = string
  default     = "t2.small"
}

variable "region" {
  description = "AWS region to use"
  type        = string
  default     = "us-east-1"
}

variable "ssh_username" {
  description = "SSH username for the instance"
  type        = string
  default     = "ubuntu"
}