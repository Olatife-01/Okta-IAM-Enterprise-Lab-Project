# 04 — Automation & Policies

Infrastructure-as-Code, CI/CD, PAM, security policies, and no-code automations used to run the lab like a real program.

## Contents
### IaC & Pipeline
- **Terraform**
  - [AWS + Terraform — IaC](./IaC%20%26%20Pipeline/Terraform/AWS%20%2B%20Terraform%20-%20IaC.md)
  - [Okta + Terraform](./IaC%20%26%20Pipeline/Terraform/Okta%20%2B%20Terraform.md)
  - [GitHub CI–CD Pipeline](./IaC%20%26%20Pipeline/Terraform/GitHub%20CI-CD%20Pipeline.md)

### PAM with HashiCorp Vault
- [HashiCorp + AWS — PAM & Dynamic credentials](./PAM%20with%20Harshicorp%20Vault/HarshiCorp%20%2B%20AWS%20-%20PAM%20%26%20Dynamic%20credentials....md)
- [Okta + HashiCorp Vault](./PAM%20with%20Harshicorp%20Vault/Okta%20%2B%20HarshiCorp%20Vault.md)

### Policies
<img width="1536" height="1024" alt="ChatGPT Image Aug 20, 2025, 09_59_59 AM" src="https://github.com/user-attachments/assets/440d4854-a84b-41d8-87ab-1d6e7e5cd862" />

- **MFA**
  - [Okta Verify](./Policies/MFA/Okta%20Verify.md)
- [Contextual Access Policies](./Policies/Contextual%20Access%20Policies.md)
- [Device Assurance, CAP, Endpoint Security](./Policies/Device%20Assurance,%20CAP,%20Endpoint%20Security.md)

### Workflows
- [Automated Identity Lifecycle & Conditional Logic](./Workflows/Automated%20Identity%20Lifecycle%20%26%20Conditional%20Logic....md)
- [Okta Workflows & Automated AWS S3-Folder Creation](./Workflows/Okta%20Workflows%20%26%20Automated%20AWS%20S3-Folder%20Cre....md)

## What this section covers
- Remote Terraform state (S3 + DynamoDB), branch-scoped workflows in GitHub Actions
- Principle of least privilege and separation of duties through SCIM mastering and policies
- Passwordless/MFA, contextual access, device assurance, and workflow automation
