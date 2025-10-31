resource "aws_instance" "e2-instance" {
    ami = var.ami
    instance_type = var.instance_type
    subnet_id = var.subnet_id
    key_name = var.key_name
    security_groups = [ var.security_groups ]
    tags = {
      Name = var.Name
      Owner = var.Owner
      Expiry_Date = var.Expiry_Date
    }

}