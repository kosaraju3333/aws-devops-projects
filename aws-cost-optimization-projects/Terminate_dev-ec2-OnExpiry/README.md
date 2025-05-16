# 🧠 EC2 Auto-Termination System for Dev/Test VMs using Expiry Tag (Terraform + Lambda + EventBridge + SNS)

## 🔍 Problem Statement

In our development workflow, developers often request temporary EC2 VMs to test code or debug issues. These VMs are created using a predefined AMI via Terraform. However, both DevOps and development teams frequently **forget to terminate** these instances after use. As a result, **unused VMs continue to run**, leading to **unnecessary AWS costs**.

---

## 💡 Solution Overview

To resolve this, we created a fully automated lifecycle management system:

- When a Dev EC2 instance is created, it includes a **`Expiry_Date` tag**.
- A **Lambda function** (written in Python) is triggered **daily via EventBridge** at **10 AM UTC**.
- The Lambda function:
  - Scans all EC2 instances with the `Expiry_Date` tag.
  - Terminates any instance where the current date **> Expiry_Date**.
  - Sends email notifications via **SNS**:
    - For instances that are **terminated**.
    - For instances **nearing expiration** (within 1 day).
      
---

## 🧱 Components Used

| Service         | Purpose                                           |
|----------------|---------------------------------------------------|
| **Terraform**   | Infrastructure as Code to provision EC2 instances |
| **EC2**          | Dev/Test VMs with custom AMI and tags            |
| **AWS Lambda**   | Python script to evaluate and terminate expired VMs |
| **Amazon EventBridge** | Cron scheduler to invoke Lambda daily |
| **Amazon SNS**   | Email alerts to DevOps for terminated/expiring VMs |

---

## Screenshots
Eventbridge Trigger Rule:
![Screenshot 2025-05-16 at 8 37 16 AM](https://github.com/user-attachments/assets/3b038e37-f61f-40b3-bbfc-404b090d767b)
Lambda Function:
![Screenshot 2025-05-15 at 1 07 54 PM](https://github.com/user-attachments/assets/708a0cb3-373c-43f5-86af-196e232c7154)
  SNS Sends Email:
![Screenshot 2025-05-16 at 8 14 59 AM](https://github.com/user-attachments/assets/babcf2d7-c55a-49cc-bbed-8921a489d5e2)
