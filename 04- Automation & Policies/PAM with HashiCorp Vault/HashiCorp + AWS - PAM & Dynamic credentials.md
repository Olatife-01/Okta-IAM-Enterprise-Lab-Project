# PAM — HashiCorp Vault Dynamic AWS IAM Credentials

> **Scope:** I enabled Vault’s AWS Secrets Engine to mint short-lived AWS IAM credentials on demand. This demonstrates modern PAM patterns (JIT access, least privilege) without static keys.

---
## I. Objective & Purpose

This lab demonstrates the implementation of **Dynamic AWS IAM Credentials** using **HashiCorp Vault**. The primary objective is to showcase a core component of modern Privileged Access Management (PAM) and the concept of Just-in-Time (JIT) access for cloud resources.

By integrating Vault with AWS to generate dynamic credentials, we aim to:

- **Eliminate Static Credentials:** Replace long-lived, static AWS access keys with short-lived, on-demand credentials, drastically reducing the attack surface.
    
- **Enforce Least Privilege:** Dynamically issue credentials with precisely the permissions needed for a specific task or duration.
    
- **Automate Credential Lifecycle:** Vault automatically creates and revokes temporary credentials, removing manual management overhead.
    
- **Improve Auditability:** Every credential generation and revocation is logged in Vault, providing a clear audit trail.
    
- **Demonstrate JIT Access:** Users or applications receive credentials only when they need them, for a limited time.
    

## II. Technical Thought Process & Evolution of Configuration

Implementing dynamic AWS credentials involved configuring Vault's AWS Secrets Engine and defining roles that govern credential generation. The process required careful attention to permissions and Vault's UI.

**Key Design Decisions:**

- **AWS Secrets Engine:** Utilized Vault's built-in AWS Secrets Engine, designed specifically for managing AWS credentials.
    
- **IAM User Credential Type:** Opted to generate temporary AWS IAM Users (with access keys) via Vault, as opposed to IAM Roles, for a clear demonstration of individual dynamic access.
    
- **Read-Only Access:** Focused on generating credentials with `ReadOnlyAccess` to demonstrate least privilege.
            

## II. Prerequisites

Before proceeding, ensure you have the following in place:

- **HashiCorp Vault Instance:** Your running and unsealed Vault instance. You have successfully configured Okta authentication for Vault.
    
- **Vault CLI:** Configured in your PowerShell/Command Prompt terminal, with `VAULT_ADDR` set to your public Vault address (e.g., `$env:VAULT_ADDR = "https://my-okta-vault-lab-public-vault-51b9f454.ee46d4f2.z1.hashicorp.cloud:8200"`).
    
- **Vault Root Token:** The initial root token generated during Vault initialization.
    
- **AWS Account:** Your active AWS account (the same one used for Terraform/EC2).
    
- **AWS IAM User for Vault (`vault-aws-iam-user`):** A dedicated AWS IAM user with programmatic access (Access Key ID and Secret Access Key) and `AdministratorAccess` policy attached (for lab simplicity).
    

## III. Configuration Steps: HashiCorp Vault Dynamic AWS IAM Credentials

This section details the step-by-step process for setting up dynamic AWS credentials.

### A. Phase 1: Create AWS IAM User for Vault's Root Credentials (In AWS Management Console)

This user provides Vault with the necessary permissions to manage dynamic AWS IAM entities.

1. **Log in to AWS Management Console** as the root user or an IAM administrator.
    
2. **Navigate to IAM** > **Users**.
    
3. Click **"Add users"**.
    
4. **User name:** `vault-aws-iam-user`.
    <img width="972" height="587" alt="Screenshot 2025-07-30 203509" src="https://github.com/user-attachments/assets/7a91f908-a1d4-4863-a990-704d71a09980" />

5. **AWS access type:** Check **"Access key - Programmatic access"**.
    
6. **Do NOT** check "Provide user access to the AWS Management Console".
    
7. Click **"Next: Permissions"**.
    
8. **Set Permissions:** Select **"Attach existing policies directly"**, search for `AdministratorAccess`, and check **"AdministratorAccess"**.
    <img width="959" height="735" alt="Screenshot 2025-07-30 203732" src="https://github.com/user-attachments/assets/370a1852-1137-4b91-9fb5-cdd64de044da" />

9. Click **"Next: Tags"** (skip) > **"Next: Review"** > **"Create user"**.
    
10. **Download and Secure Access Keys:** Immediately copy the **"Access key ID"** and **"Secret access key"**, and click **"Download .csv"**. **Save this file securely.**
    
11. **Create Access Key Use Case:** When prompted, select **"Third-party service"** as the use case for this access key.
    <img width="952" height="734" alt="Screenshot 2025-07-30 204148" src="https://github.com/user-attachments/assets/cf99034b-0d2b-4ef9-8844-506afc755149" />


### B. Phase 2: Enable and Configure the AWS Secrets Engine (In Vault UI)

This step activates the AWS secrets engine in Vault and provides it with the `vault-aws-iam-user` credentials.

1. **Log in to your HashiCorp Vault UI** (e.g., `https://*****.z1.hashicorp.cloud***`).
    
    - **Log in using your Vault Root Token.**
        
2. **Enable the AWS Secrets Engine:**
    
    - In the left-hand navigation, click **"Secrets"**.
        <img width="901" height="556" alt="Screenshot 2025-07-30 212015" src="https://github.com/user-attachments/assets/68b21323-9514-46db-bdaa-c4831bad22f1" />

    - Click **"Enable new engine"**.
        
    - Select **"AWS"**. Click **"Next"**.
        <img width="877" height="871" alt="Screenshot 2025-07-30 212059" src="https://github.com/user-attachments/assets/f857d80c-6d11-426c-bf34-e711a1ed52e2" />

    - **Path:** Leave as `aws`.
        
    - **Ignore all other options** on this page.
        
    - Click **"Enable engine"**.
        <img width="781" height="318" alt="Screenshot 2025-07-30 212354" src="https://github.com/user-attachments/assets/0f63c104-8c9e-499f-a13b-6fe467d862b2" />

3. **Configure the AWS Secrets Engine with Root Credentials:**
    
    - You will be redirected to the "Configure AWS" page.
        
    - **Access key:** Paste the **Access Key ID** of your `vault-aws-iam-user`.
        
    - **Secret key:** Paste the **Secret Access Key** of your `vault-aws-iam-user`.
        
    - **Region:** Select **`eu-central-1` (Europe - Frankfurt)** from the dropdown (to align with your S3/EC2 resources).
        
    - Leave other options as default.
        
    - Click **"Save"**.
        <img width="866" height="909" alt="image" src="https://github.com/user-attachments/assets/c7cdc980-4ed5-45ae-9087-688fdb024857" />


### C. Phase 3: Define Roles for Dynamic AWS IAM Credentials (In Vault UI)

This step defines the type of dynamic credentials Vault will generate.

1. **Navigate to Roles:**
    
    - In the Vault UI, within the `aws` secrets engine view, click on the **"Roles"** tab.
        
2. **Create a New Role:**
    
    - Click **"Create role"**.
        
    - **Role name:** `my-aws-read-only-role`.
        
    - **Credential Type:** Select **"IAM User"**.
        
    - **Policy ARNs:**
        
        - In the input field, type: `arn:aws:iam::aws:policy/ReadOnlyAccess`
            
        - **Crucially, click the "Add" button** next to the ARN to confirm it.
            
    - **Policy document:** Ensure this section is **empty**.
        
    - **Max TTL, Default TTL:** These options are not present on this UI page; Vault will use its default lease durations.
        
    - Click **"Create role"**.
        <img width="897" height="877" alt="Screenshot 2025-07-30 213631" src="https://github.com/user-attachments/assets/bf3ace07-459f-4ad3-8735-5b4f747bbe35" />
        <img width="888" height="417" alt="Screenshot 2025-07-30 214012" src="https://github.com/user-attachments/assets/5863607d-c6ae-48e2-9c99-86df77892a72" />


### D. Phase 4: Test Dynamic Credential Generation

This is the final verification of the dynamic credential functionality.

1. **Generate Credentials in Vault UI:**
    
    - You are on the detail page for `my-aws-read-only-role`.
        
    - Click the **"Generate credentials"** button.
        <img width="882" height="337" alt="Screenshot 2025-07-30 214140" src="https://github.com/user-attachments/assets/28794b98-ec1f-457e-9286-0b14c4ec700f" />

    - You can specify a "Lease Duration" (e.g., `30m`) or leave blank.
        
    - Click **"Generate"**.
        
    - **IMMEDIATELY copy** the **Access Key** and **Secret Key** displayed.
        <img width="872" height="625" alt="Screenshot 2025-07-30 214258" src="https://github.com/user-attachments/assets/5ba72c08-fc3c-4cac-a3a0-ec1ee7a1846e" />

2. **Configure AWS CLI with Temporary Credentials (PowerShell):**
    
    - **Open a new PowerShell or Command Prompt terminal.**
        
    - Set environment variables for the temporary credentials (replace placeholders):
        
        ```
        $env:AWS_ACCESS_KEY_ID = "<GENERATED_ACCESS_KEY_ID>"
        $env:AWS_SECRET_ACCESS_KEY = "<GENERATED_SECRET_ACCESS_KEY>"
        $env:AWS_DEFAULT_REGION = "eu-central-1" # Use the region you configured in Vault
        ```
        
3. **Test AWS Access with Dynamic Credentials (PowerShell):**
    
    - In the same PowerShell terminal, run:
        
        ```
        aws s3 ls
        ```
        
        - **Expected Outcome:** You should see a list of your S3 buckets (e.g., `mel***-fed-access-test-*****`). This confirms **read access**.
            
    - Try to create an S3 bucket (which should be denied):
        
        ```
        aws s3 mb s3://my-temp-test-bucket-12345
        ```
        
        - **Expected Outcome:** You should receive an **"Access Denied"** error. This confirms the `ReadOnlyAccess` policy is correctly enforced and prevents write operations.
            <img width="1878" height="449" alt="image" src="https://github.com/user-attachments/assets/55d37987-f8c6-4bb8-aca9-e470e3dc1064" />

4. **Observe Automatic Credential Revocation:**
    
    - After the lease duration (e.g., 30 minutes) expires, the dynamically generated AWS IAM user and its access keys will be automatically deleted by Vault.
        
    - If you try `aws s3 ls` again after expiration, you will receive an "InvalidAccessKeyId" or "SignatureDoesNotMatch" error, confirming the credentials are no longer valid.
        

## IV. Troubleshooting & Lessons Learned

This section highlights challenges encountered and the resolutions.

- **Vault CLI Authentication & Permissions:**
    
    - **Problem:** `vault login` failed (connection refused) or `vault secrets enable` resulted in "permission denied."
        
    - **Root Cause:** `VAULT_ADDR` was unset (defaulting to localhost), and the Okta-federated user lacked sufficient permissions for administrative tasks.
        
    - **Resolution:** Explicitly set `VAULT_ADDR` to the public Vault URL. Authenticated using the **initial Vault Root Token** for administrative operations.
        
    - **Lesson:** Always set `VAULT_ADDR`. Administrative tasks require highly privileged tokens.
        
- **AWS IAM User for Vault Setup:**
    
    - **Problem:** Uncertainty about granting console access or selecting use case for `vault-aws-iam-user`.
        
    - **Resolution:** Confirmed **no console access** for this programmatic user. Selected **"Third-party service"** as the access key use case.
        
    - **Lesson:** Adhere to principle of least privilege for programmatic users.

## V. Next Steps & Enhancements

With dynamic AWS IAM credential generation successfully implemented, future enhancements for the Enterprise IAM Lab could include:

- **Integrate with Applications:** Demonstrate how an application (e.g., a simple Python script or a server) can programmatically request dynamic credentials from Vault.
    
- **Dynamic IAM Roles:** Configure Vault to generate temporary AWS IAM Roles (for EC2 instances or Lambda functions to assume) instead of IAM Users.
    
- **SSH Certificate Authority:** Configure Vault to act as an SSH CA, issuing short-lived SSH certificates for server access.
    
- **Other Secrets Engines:** Explore other dynamic secrets engines (e.g., databases, Kubernetes, Azure, GCP).
    
- **Policy Granularity:** Create more granular AWS IAM policies for Vault roles beyond `ReadOnlyAccess`.
---
