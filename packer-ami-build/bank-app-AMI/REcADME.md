# 🧱 Packer - Custom AWS AMI for Bank App

This project uses **HashiCorp Packer** to build a custom **Ubuntu AMI** for deploying the **Bank Application**.  
The AMI comes preinstalled with Java, AWS CLI, and a systemd service that automatically runs the Bank App on startup.

---

## 🚀 Overview

**Goal:** Create a reusable, production-ready AMI with all the dependencies and configurations required for the Bank Application.

This AMI includes:
- Java 17 Runtime
- AWS CLI v2
- Custom startup script for the Bank App
- Preconfigured systemd service (`bankapp.service`)
- Log directory under `/var/log/bank-app/`

---

## 🧩 Folder Structure

packer-project/
│
├── main.pkr.hcl # Main Packer configuration file
├── variables.pkr.hcl # Variable definitions
│
├── scripts/
│ ├── java_installation.sh # Installs Java 17
│ ├── aws_installation.sh # Installs AWS CLI v2
│ └── bank-app-start.sh # Bank app startup script
│
├── service-files/
│ └── bankapp.service # systemd unit file for app startup
│
└── README.md # Project documentation


---

## ⚙️ Prerequisites

Before building the AMI, ensure you have the following installed locally:

- [Packer](https://developer.hashicorp.com/packer/downloads)
- [AWS CLI](https://aws.amazon.com/cli/)
- Valid AWS credentials configured (via `aws configure`)
- IAM user/role with permissions:
  - `AmazonEC2FullAccess`
  - `IAMReadOnlyAccess`

---

## 🧠 What This Packer Template Does

1. **Uses Ubuntu 22.04 LTS (Jammy Jellyfish)** as base AMI.
2. Installs:
   - Java 17 (`openjdk-17-jre`)
   - AWS CLI v2
3. Copies and configures startup script:
   - Copies `bank-app-start.sh` → `/opt/bank-app-start.sh`
   - Sets executable permissions
   - Creates `/var/log/bank-app/` for logs
4. Installs and enables systemd service:
   - Copies `bankapp.service` → `/etc/systemd/system/bankapp.service`
   - Reloads systemd daemon
   - Enables the service at boot

---

## 🔧 Variables

Edit or provide the following in `variables.pkr.hcl`:

```hcl
variable "ami_name" {
  type    = string
  default = "bank-app-custom-ami"
}

variable "instance_type" {
  type    = string
  default = "t2.micro"
}

variable "region" {
  type    = string
  default = "us-east-1"
}

variable "ssh_username" {
  type    = string
  default = "ubuntu"
}
