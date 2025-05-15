variable "ami" {
  description = "Ami ID"
}

variable "instance_type" {
  default = "t2.small"
  description = "EC2 instance Size"
}

variable "key_name" {
  default = "my_work"
  description = "Pem Key"
}

variable "subnet_id" {
  description = "AZ"
}

variable "security_groups" {
  description = "VM SG"
}

variable "Name" {
  description = "Name of VM"
}
variable "Owner" {
  description = "Owner of VM"
}

variable "Expiry_Date" {
  description = "VM deleton date (Expiry date (DD-MM-YYYY))"
}