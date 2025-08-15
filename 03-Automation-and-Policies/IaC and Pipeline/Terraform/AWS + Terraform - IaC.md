# Expand Terraform for Cloud IAM — AWS Identity and Access Management

*Using Terraform to provision AWS IAM, S3, and EC2 in a repeatable, auditable way*

> **Scope:**. I used Terraform from Windows PowerShell/VS Code to manage AWS IAM (users, groups, policies), and stood up core services (S3, EC2) in a single region. This captures my exact configs, the errors I hit, and how I fixed them.

---
## I. Objective & Purpose

This lab demonstrates my use of **Terraform** to provision and manage **AWS Identity and Access Management (IAM)** resources, along with foundational AWS services like **S3 buckets** and **EC2 instances**. The primary objective is to showcase Infrastructure as Code (IaC) principles for cloud identity and basic infrastructure, enabling automated, repeatable, and version-controlled management of resources within an AWS account. This is a step towards integrating cloud resources into a broader enterprise IAM strategy.

By using Terraform for AWS IAM and basic resources, I achieve:

- **Automated Resource Provisioning:** Programmatically create and manage AWS IAM entities and core infrastructure.
    
- **Version Control:** Track changes to infrastructure configurations in code, improving auditability and collaboration.
    
- **Consistency & Repeatability:** Ensure consistent configurations across different AWS accounts or environments.
    
- **Least Privilege for Automation:** Establish secure programmatic access for Terraform itself.
    

## II. Technical Thought Process & Evolution of Configuration
AWS is my cloud control plane and execution environment: it hosts the workloads, enforces network boundaries, and ultimately executes whatever identities are allowed to do.
In an enterprise setting, that power demands repeatability, least-privilege, and auditable change—manual clicks won’t satisfy scale or compliance.
Terraform solves this by letting me declare AWS resources and IAM intent as code, so desired state is explicit, idempotent, and reviewable before it ever touches production.
By codifying IAM (users, groups, policies, permission boundaries), I can prove and reproduce least-privilege instead of hoping a console session matched the design.
- S3 becomes both a practical artifact store and, with DynamoDB locking, a durable backend for Terraform state—supporting team collaboration and preventing drift.
- EC2 instance gives me a concrete, low-risk workload to validate access paths, security groups, and federated sign-in from Okta end to end.
- Tying Okta to AWS via SSO and SCIM aligns workforce identity with cloud authorization, so groups and permission sets map cleanly from one system of record.
- The AWS CLI is my verification harness: I exercise temporary credentials, list resources, and confirm that policy outcomes match what the plan predicted.
All configuration lives in Git, which provides history, code review, and rollback so every change has provenance I can cite in audits.
Where appropriate I layer CI/CD to run format/validate/plan gates, require approvals, and apply automatically—closing the loop from design to controlled change.
This approach is exactly why I’m integrating Terraform in the lab: it demonstrates practical, zero-trust-aligned guardrails that scale, are testable, and produce real evidence.
The outcome is a realistic pattern I can extend—same controls, just more modules—when moving from a lab to an enterprise footprint.
The process of setting up Terraform for AWS IAM and basic resources involved extensive troubleshooting, particularly related to the AWS CLI installation, Terraform file management, resource configuration, and persistent regional deployment challenges.
These extensive troubleshooting steps were crucial for establishing a functional and reliable Terraform environment for AWS IAM and core infrastructure.

## III. Prerequisites

Before proceeding, ensure you have the following in place:

- **AWS Account:** An active AWS account with root user access for initial setup.
    
- **AWS CLI:** Successfully installed and configured on your Windows machine (PowerShell/Command Prompt).
    
    - You should be able to run `aws --version` in a new terminal window.
        
    - You should have run `aws configure` to set up your default region and credentials for the `terraform-admin` IAM user.
        
- **Terraform CLI:** Installed and configured on your system.
    
- **VS Code:** Installed with the HashiCorp Terraform extension.
    
- **Project Folders:** Your Terraform project is organized (e.g., `C:\Terraform\terraform-aws-iam-lab`).
    
- **EC2 Key Pair:** An SSH Key Pair named `****` must exist in the `eu-central-1` (Frankfurt) region.
    
    - **How to create:** Log in to AWS Console, switch to `eu-central-1`. Navigate to **EC2** > **Key Pairs**. Click "Create key pair", name it `my-ec2-keypair`, select ".pem", and download.
        

## IV. Configuration Steps: Terraform for AWS IAM and Resources

This section details the successful setup of Terraform to manage AWS IAM and core resources.

### A. AWS Account Setup & Initial Access for Terraform

1. **Create an IAM User for Terraform Programmatic Access:**
    
    - Log in to AWS Management Console as the root user.
        
    - Navigate to **IAM** > **Users**.
        
    - Click **"Add users"**.
        
    - **User name:** `terraform-admin`.
        
    - **AWS access type:** Check **"Access key - Programmatic access"**.
        <img width="952" height="867" alt="Screenshot 2025-07-28 192900" src="https://github.com/user-attachments/assets/f260096a-faeb-460c-bd30-9aeef5772d35" />

    - Click **"Next: Permissions"**.
        
    - **Set Permissions:** Select **"Attach existing policies directly"**, search for `AdministratorAccess`, and check the box for **"AdministratorAccess"**. (For lab simplicity; production environments should use least privilege).
        
    - Click **"Next: Tags"** (skip).
        
    - Click **"Next: Review"**.
        
    - Click **"Create user"**.
        <img width="1894" height="873" alt="Screenshot 2025-07-28 193122" src="https://github.com/user-attachments/assets/6da7c6c6-7b06-4c4c-82d9-88894a17683a" />

    - **Download and Secure Access Keys:** Immediately copy the **"Access key ID"** and **"Secret access key"**, and click **"Download .csv"**. **Save this file securely.**
        <img width="973" height="846" alt="Screenshot 2025-07-28 193920" src="https://github.com/user-attachments/assets/adaf8333-4425-4e46-88c0-4a344f964327" />

2. **Configure AWS CLI on Your Local Machine:**
    
    - Open **PowerShell** or **Command Prompt**.
       <img width="560" height="804" alt="Screenshot 2025-07-28 200853" src="https://github.com/user-attachments/assets/8e6fa95e-5c2d-4205-9d4e-0847af00c604" />
 
    - Run: `aws configure`
        
    - Enter the **Access Key ID**, **Secret Access Key**, and your desired **Default region name** (e.g., `eu-central-1`). Accept default output format.
       <img width="1364" height="418" alt="image" src="https://github.com/user-attachments/assets/d66838d0-3d71-4088-8229-6e4f6fcd15a7" />
 

### B. Create Terraform Project Directory and Configuration Files

1. **Create Project Directory:**
    
    ```
    mkdir C:\Terraform\terraform-aws-iam-lab
    cd C:\Terraform\terraform-aws-iam-lab
    ```
    <img width="1081" height="357" alt="image" src="https://github.com/user-attachments/assets/dda99df3-74b5-469f-9ee1-6873765b3db6" />

2. **Create `versions.tf`:**
    
    - Create a file named `versions.tf` in `C:\Terraform\terraform-aws-iam-lab`.
        
    - Paste the following content:
        
        ```
        # versions.tf
        
        terraform {
          required_version = ">= 1.0.0"
        
          required_providers {
            aws = {
              source  = "hashicorp/aws"
              version = "~> 5.0"
            }
          }
        }
        ```
        
    - **Save the file** ensuring it has the `.tf` extension.
        
3. **Create `main.tf`:**
    
    - Create a file named `main.tf` in `C:\Terraform\terraform-aws-iam-lab`.
        
    - Paste the following content (ensure `region` and `bucket` name are correct):
        
        ```
        # main.tf
        
        # Configure the AWS Provider
        # This block tells Terraform to use the AWS provider and specifies the region.
        # Terraform will automatically pick up credentials from 'aws configure'
        provider "aws" {
          region = "eu-central-1" # Set to Europe (Frankfurt) - All new resources will deploy here
        }
        
        # Define an AWS IAM Group
        # This resource creates a new IAM group named 'TerraformManagedAWSGroup'.
        resource "aws_iam_group" "terraform_managed_aws_group" {
          name = "TerraformManagedAWSGroup"
          path = "/" # Default path
        }
        
        # Define an AWS IAM User
        # This resource creates a new IAM user named 'terraform-test-user'.
        resource "aws_iam_user" "terraform_test_user" {
          name = "terraform-test-user"
          path = "/" # Default path
          # Optional: Force password reset on next login
          # force_destroy = true # Uncomment carefully: allows deletion of user even if they have active access keys
        }
        
        # Attach a policy to the IAM Group (Example: Read-only access)
        # This resource attaches the AWS managed 'ReadOnlyAccess' policy to our new group.
        resource "aws_iam_group_policy_attachment" "terraform_managed_aws_group_read_only_policy" {
          group      = aws_iam_group.terraform_managed_aws_group.name
          policy_arn = "arn:aws:iam::aws:policy/ReadOnlyAccess" # AWS managed policy ARN
        }
        
        # Add the IAM User to the IAM Group
        # This resource adds the 'terraform-test-user' to the 'TerraformManagedAWSGroup'.
        # This resource is specifically for managing a user's membership in one or more groups.
        resource "aws_iam_user_group_membership" "terraform_test_user_to_group" {
          user     = aws_iam_user.terraform_test_user.name
          groups   = [aws_iam_group.terraform_managed_aws_group.name]
        }
        
        # Output the IAM Group Name
        # This output will display the the name of the created IAM group after 'terraform apply'.
        output "iam_group_name" {
          value       = aws_iam_group.terraform_managed_aws_group.name
          description = "The name of the IAM group created by Terraform."
        }
        
        # Output the IAM User Name
        # This output will display the the name of the created IAM user after 'terraform apply'.
        output "iam_user_name" {
          value       = aws_iam_user.terraform_test_user.name
          description = "The name of the IAM user created by Terraform."
        }
        
        # Define an AWS S3 Bucket
        # This resource creates a new S3 bucket.
        # Bucket names must be globally unique across all AWS accounts.
        resource "aws_s3_bucket" "mellonryon_federated_access_test_bucket" {
          bucket = "mellonryon-fed-access-test-***" # IMPORTANT: CHOOSE A NEW, GLOBALLY UNIQUE NAME!
          acl    = "private"
          tags = {
            Name        = "MellonFederatedAccessTestBucket"
            Environment = "Dev"
            ManagedBy   = "Terraform"
          }
        }
        
        # Output the S3 Bucket Name
        output "s3_bucket_name" {
          value       = aws_s3_bucket.mellonryon_f*****.id
          description = "The name of the S3 bucket created by Terraform."
        }
        
        # --- EC2 Instance and Networking Resources ---
        
        # Data source to find the latest Amazon Linux 2 AMI in the current region (eu-central-1)
        data "aws_ami" "amazon_linux_2" {
          most_recent = true
          owners      = ["amazon"]
        
          filter {
            name   = "name"
            values = ["amzn2-ami-hvm-*-x86_64-gp2"]
          }
        
          filter {
            name   = "virtualization-type"
            values = ["hvm"]
          }
        }
        
        # Data source to get the default VPC (Virtual Private Cloud) in eu-central-1
        data "aws_vpc" "default" {
          default = true
        }
        
        # Define a Security Group for the EC2 Instance
        # This security group allows SSH access (port 22) from anywhere.
        resource "aws_security_group" "mellonryon_ec2_sg" {
          name        = "mellonryon-ec2-sg"
          description = "Allow SSH access"
          vpc_id      = data.aws_vpc.default.id # Reference the default VPC
        
          ingress {
            from_port   = 22
            to_port     = 22
            protocol    = "tcp"
            cidr_blocks = ["0.0.0.0/0"] # WARNING: 0.0.0.0/0 is for lab only, restrict in production
          }
        
          egress {
            from_port   = 0
            to_port     = 0
            protocol    = "-1" # All protocols
            cidr_blocks = ["0.0.0.0/0"]
          }
        
          tags = {
            Name = "MellonryonEC2SecurityGroup"
          }
        }
        
        # Define an AWS EC2 Instance (Free Tier Eligible)
        resource "aws_instance" "mellonryon_server" {
          ami           = data.aws_ami.amazon_linux_2.id # Dynamically get the latest Amazon Linux 2 AMI ID for eu-central-1
          instance_type = "t3.micro" # Free Tier eligible instance type
          key_name      = "my-ec2-keypair" # IMPORTANT: Ensure this Key Pair exists in eu-central-1 or create one manually
        
          vpc_security_group_ids = [aws_security_group.mellonryon_ec2_sg.id] # Attach the security group
        
          tags = {
            Name        = "MellonryonServer"
            Environment = "Dev"
            ManagedBy   = "Terraform"
          }
        }
        
        # Output the EC2 Instance ID
        output "ec2_instance_id" {
          value       = aws_instance.mellonryon_server.id
          description = "The ID of the EC2 instance created by Terraform."
        }
        
        # Output the EC2 Public IP
        output "ec2_public_ip" {
          value       = aws_instance.mellonryon_server.public_ip
          description = "The public IP address of the EC2 instance."
        }
        ```
        
    - **Save the file** ensuring it has the `.tf` extension.
        

### C. Initialize, Plan, and Apply Terraform Configuration

1. **Initialize Terraform:**
    
    - In your terminal (in `C:\Terraform\terraform-aws-iam-lab`), run:
        
        ```
        terraform init -upgrade
        ```
        
    - _Expected:_ `Terraform has been successfully initialized!`
        <img width="1167" height="743" alt="Screenshot 2025-07-28 203112" src="https://github.com/user-attachments/assets/149f18b2-071b-42fb-869f-3b6717f43671" />

2. **Generate the Plan:**
    
    - Run:
        
        ```
        terraform plan
        ```
        
    - _Expected:_ `Plan: * to add, 0 to change, 0 to destroy.` (Confirming creation of the new S3 bucket and the EC2 instance/security group).
        <img width="1881" height="1057" alt="Screenshot 2025-07-28 204238" src="https://github.com/user-attachments/assets/7646de77-404d-44ce-acd2-4967e8a826ab" />

3. **Apply the Plan:**
    
    - Run:
        
        ```
        terraform apply
        ```
        
    - Type `yes` when prompted.
        
    - _Expected:_ `Apply complete! Resources: * added, 0 changed, 0 destroyed.`
        <img width="1873" height="837" alt="Screenshot 2025-07-28 204354" src="https://github.com/user-attachments/assets/dfeb55d3-ea77-4c9a-b4b9-82636e180cbc" />


## V. Verification: AWS Management Console

1. **Log in to your AWS Management Console.**
    
2. Navigate to **IAM**.
    
3. **Verify User:** Click on **"Users"** in the left navigation. Confirm `terraform-test-user` exists.
    
4. **Verify User Group:** Click on **"User groups"** in the left navigation. Confirm `TerraformManagedAWSGroup` exists.
    
5. **Verify Group Permissions:** Click on `TerraformManagedAWSGroup`. Go to the **"Permissions"** tab. Confirm `ReadOnlyAccess` policy is attached.
    
6. **Verify Group Membership:** Go to the **"Users"** tab within `TerraformManagedAWSGroup`. Confirm `terraform-test-user` is a member.
    <img width="979" height="865" alt="image" src="https://github.com/user-attachments/assets/1bb3d302-b5c9-405a-9876-822830d4554a" />

7. **Verify S3 Bucket:** Navigate to **S3**. Confirm your new S3 bucket (e.g., `mellonryon-fed-access-test-bucket-*****`) exists.
    <img width="655" height="384" alt="image" src="https://github.com/user-attachments/assets/60510443-e963-4f7a-8278-8db36142c10d" />

8. **Verify EC2 Instance & Security Group:** Navigate to **EC2**.
    
    - Click **"Instances"**. Confirm `MellonryonServer` instance exists and is running.
        <img width="726" height="354" alt="Screenshot 2025-07-29 224332" src="https://github.com/user-attachments/assets/a3a96fd0-01c5-4fb1-afdf-d31c8bc36a1e" />

    - Click **"Security Groups"**. Confirm `mellonryon-ec2-sg` exists.
  

## VI. Troubleshooting & Lessons Learned

This section highlights the challenges encountered and their resolutions.

- **AWS CLI Installation Issues:**
    
    - **Problem:** `aws` command not recognized.
        
    - **Root Cause:** Incomplete installation (missing `aws.exe` or `bin` folder), or PATH environment variable not updated.
        
    - **Resolution:** Multiple re-installations, ensuring "Run as administrator", and verifying file presence. The final successful installation correctly placed the executable and updated the PATH.
        
    - **Lesson:** Verify installation paths and `aws.exe` presence. Use "Run as administrator" for installers.
        
- **Terraform Configuration File Extensions:**
    
    - **Problem:** `terraform init` reported "empty directory."
        
    - **Root Cause:** `main.tf` and `versions.tf` were saved as `.txt` files.
        
    - **Resolution:** Renamed files to correct `.tf` extension, explicitly using double quotes and "All Files (_._)" in Notepad's "Save As" dialog.
        
    - **Lesson:** Terraform requires `.tf` file extensions. Be mindful of text editor defaults.
        
- **Incorrect `aws_iam_group_membership` Resource:**
    
    - **Problem:** `terraform plan` failed with errors like "Missing required argument: name" and "Unsupported argument: user" for `aws_iam_group_membership`.
        
    - **Root Cause:** Used the incorrect Terraform resource for adding individual users to a group. `aws_iam_group_membership` is for managing _all_ members of a group, not individual additions.
        
    - **Resolution:** Replaced `aws_iam_group_membership` with `aws_iam_user_group_membership`, which is designed for individual user-to-group assignments.
        
    - **Lesson:** Understand the specific purpose and arguments of Terraform resources. Choose the most appropriate resource for the desired outcome.
        
- **Persistent S3 Bucket Creation Issues:**
    
    - **Problem:** `terraform apply` repeatedly failed with `BucketAlreadyOwnedByYou` (StatusCode: 409) for the S3 bucket.
        
    - **Root Cause:** S3 bucket names are **globally unique**. The name was already taken by a previously created (and possibly deleted) bucket.
        
    - **Resolution:** Manually deleted the previous S3 bucket in AWS, and then used a **brand new, highly unique global name** for the S3 bucket in `main.tf`.
        
    - **Lesson:** S3 bucket names are globally unique. Always use a highly unique naming convention, especially in shared environments.
        
- **Persistent EC2 Instance Deployment Issues:**
    
    - **Problem:** `terraform apply` consistently failed with `Unsupported: The requested configuration is currently not supported` errors, or `InvalidKeyPair.NotFound`.
        
    - **Root Cause 1:** AMI/Instance Type/Region incompatibility. Specific AMIs (like Ubuntu) or instance types (`t2.micro`) might have limited support or capacity in certain regions (e.g., `eu-north-1`).
        
    - **Root Cause 2:** EC2 Key Pairs are region-specific. If the `key_name` in `main.tf` didn't exist in the target region, deployment failed.
        
    - **Resolution:**
        
        - Standardized the deployment region for _all_ new resources (S3 and EC2) to `eu-central-1` (Frankfurt), a stable and well-supported region.
            
        - Used the `t3.micro` instance type (free tier eligible).
            
        - Dynamically sourced the **latest Amazon Linux 2 AMI** for `eu-central-1` (most compatible).
            
        - **Ensured an EC2 Key Pair (`my-ec2-keypair`) was explicitly created in the `eu-central-1` region.**
            
    - **Lesson:** Ensure AMI, instance type, and key pair are compatible and present in the _exact_ target region. Standardizing on a single, well-supported region for initial deployments simplifies troubleshooting.
    - **Optional PowerShell tips:**

```powershell
$env:TF_LOG = "INFO"   # or DEBUG/TRACE for deep troubleshooting
terraform plan
$env:TF_LOG = ""       # clear when done

terraform init -upgrade  # refresh provider plugins if needed
```
      

## VII. Next Steps & Enhancements

With basic AWS IAM and infrastructure (S3, EC2) management via Terraform successfully demonstrated, future enhancements for the Enterprise IAM Lab could include:

- **Automated AWS IAM Identity Center Management:** Explore using Terraform to manage AWS IAM Identity Center Permission Sets and Account Assignments (using `aws_ssoadmin_*` resources) to fully automate the federation setup.
    
- **Provision More AWS Resources:** Use Terraform to provision other AWS free tier resources (e.g., RDS databases, Lambda functions) and manage their IAM policies.
    
- **State Management:** Implement Terraform remote state management (e.g., using an S3 bucket with DynamoDB locking) for collaborative and secure state.
    
- **Automated Deployment:** Integrate Terraform into a CI/CD pipeline for automated AWS IAM and infrastructure deployments.
    
- **HashiCorp Vault PAM:** Revisit advanced PAM features like dynamic secrets and JIT access.

- **Secrets:** Store creds in a secrets manager (e.g., Vault) instead of local env.
