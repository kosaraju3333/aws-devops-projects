packer {
  required_plugins {
    amazon = {
      version = ">= 1.6.0"
      source  = "github.com/hashicorp/amazon"
    }
  }
}


# --- Builder section ---
source "amazon-ebs" "ubuntu" {
  ami_name      = var.ami_name
  ami_description  = "Custom Bank-app AMI built with Packer"
  instance_type = var.instance_type
  region        = var.region

  source_ami_filter {
    filters = {
      name                = "ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = ["099720109477"]
  }
  ssh_username = var.ssh_username

  tags = {
    Name        = var.ami_name
    Environment = "Development"
    CreatedBy   = "Packer"
  }
}

build {
  name    = "BankApp-AMI-build-packer"
  sources = ["source.amazon-ebs.ubuntu"]


  provisioner "shell" {
    script = "scripts/java_installation.sh"
  }

  provisioner "shell" {
    script = "scripts/aws_installation.sh"
  }

  provisioner "shell" {
    script = "scripts/codedeploy_agent_installation.sh"
  }
  

  provisioner "file" {
    source = "scripts/bank-app-start.sh"
    destination = "/tmp/bank-app-start.sh"
  }

  provisioner "shell" {
    inline = [
      "sudo mv /tmp/bank-app-start.sh /opt/bank-app-start.sh",
      "sudo chmod +x /opt/bank-app-start.sh",
      "sudo mkdir /var/log/bank-app"
    ]
  }

   provisioner "file" {
    source = "service-files/bankapp.service"
    destination = "/tmp/bankapp.service"
  }

  provisioner "shell" {
    inline = [
      "sudo mv /tmp/bankapp.service /etc/systemd/system/bankapp.service"
    ]
  }

  provisioner "shell" {
    inline = [
      "sudo systemctl daemon-reload",
      "sudo systemctl enable bankapp.service"
    ]
  }
}
