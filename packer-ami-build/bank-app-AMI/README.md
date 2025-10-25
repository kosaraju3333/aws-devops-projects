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
├── main.pkr.hcl
├── variables.pkr.hcl
│
├── scripts/
│   ├── java_installation.sh
│   ├── aws_installation.sh
│   └── bank-app-start.sh        ✅ (below)
│
├── service-files/
│   └── bankapp.service          ✅ (below)
│
└── README.md


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

## 🏗️ How to Build the AMI

1️⃣ Initialize Packer
```bash
packer init .
```

2️⃣ Validate Configuration
```bash
packer validate .
```

3️⃣ Build AMI
```bash
packer build .
```


## ✅ Once successful, Packer will output the AMI ID at the end:

```bash==> Builds finished. The artifacts of successful builds are:
--> amazon-ebs: AMIs were created:
us-east-1: ami-0abcd12345efgh678
```
* <img width="1548" height="784" alt="Screenshot 2025-10-25 at 11 10 41 AM" src="https://github.com/user-attachments/assets/0492a499-dff3-4eae-a66a-24dae43259a7" />


## 🧩 How the Service Works

* The systemd unit (bankapp.service) starts automatically on boot.

* It runs your Bank App using:

```bash/usr/bin/java -jar /home/ubuntu/bank-app/bankapp-0.0.1-SNAPSHOT.jar >> /var/log/bank-app/app.log 2>&1```


* Logs are stored in /var/log/bank-app/app.log.
