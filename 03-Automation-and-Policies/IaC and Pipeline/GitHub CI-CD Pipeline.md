Absolutely—here’s your note with the **minor edits applied**: added `fmt/validate` + PR-aware conditions to the workflow, fixed typos and casing, aligned backend key names, and added a brief safeguard note around `prevent_destroy`. I kept your structure and images in place.

---

# CI-CD Pipeline Implementation

## I. Objective & Purpose

This lab details how I established a robust Continuous Integration/Continuous Delivery (CI/CD) pipeline for the Enterprise IAM Lab. The goal is to automate the provisioning and management of Terraform-defined infrastructure for **Okta** and **AWS**, producing a secure, repeatable, and **idempotent** workflow. The pipeline replaces manual runs with automated **format/validate/plan/apply** stages, uses a remote Terraform state (**S3 + DynamoDB lock**) as the single source of truth, injects secrets securely via GitHub Actions, and gates changes by branch so AWS and Okta paths run independently but live in one repo.
By implementing this CI/CD pipeline, the project aimed to:

* **Automate Deployments**: Replace manual infrastructure provisioning with reliable, automated processes.
* **Ensure Idempotency**: Guarantee that applying the same configuration multiple times consistently yields the desired state without errors.
* **Enhance Consistency**: Standardize infrastructure deployments and reduce configuration drift.
* **Improve Security & Auditability**: Integrate secure credential management and provide a clear audit trail for all infrastructure changes.
* **Facilitate Collaboration**: Enable multiple contributors to safely manage infrastructure changes from a shared source of truth.

## II. Technical Thought Process & Evolution of Configuration

AWS and Okta are the two control planes I’m automating; both demand repeatability, least-privilege, and an audit trail strong enough for compliance. Manual CLI runs don’t scale or satisfy evidence needs, so I moved the execution to CI/CD where every plan and apply is logged, attributable, and reproducible. Terraform gives me **declarative, idempotent infrastructure**, but only if runners share a **remote state**—hence S3 for state and DynamoDB for locks to prevent concurrent corruption. I adopted a **mono-repo** with clear subfolders for AWS and Okta, then used **conditional jobs** so each path triggers only when its branch changes (e.g., `main` → AWS; `okta-configs` → Okta). Secrets never land in code; they’re injected at runtime from GitHub Secrets as environment variables that match Terraform’s expectations exactly. Early failures taught me to be precise with **working-directory** paths, case-sensitive TF vars, and `.gitignore` hygiene to keep provider binaries and state out of Git. I iterated through “already exists” errors until the backend was authoritative; from there, plans stabilized, applies were idempotent, and the pipeline became a reliable control point rather than another source of drift.

**Key Design Decisions:**

* **Mono-Repository Strategy**: A single GitHub repository (`terraform-iam-lab`) was adopted to host Terraform configurations for both AWS (`terraform-aws-lab`) and Okta (`okta-terraform-lab`). This centralizes code management and simplifies cross-project visibility.
* **Remote Terraform State**: To ensure a single, authoritative source of truth for infrastructure state across local development and CI/CD environments, an **AWS S3 bucket** (`iam-terraform-state-bucket`) was chosen for state storage. This was paired with an **AWS DynamoDB table** (`iam-terraform-state-lock`) for state locking, preventing concurrent operations from corrupting the state file.
* **Conditional Workflow Execution**: GitHub Actions was selected as the CI/CD platform. The `terraform.yml` workflow was designed with explicit conditional logic so AWS operations execute when the target is `main`, and Okta operations execute when the target is `okta-configs`. This provides logical separation and efficient execution within the mono-repo.
* **Secure Credential Management**: Sensitive API tokens and access keys are stored as **GitHub Secrets** and securely injected into the pipeline's environment using `env` variables, preventing hardcoding and exposure.

## III. Prerequisites

Before configuring the CI/CD pipeline, ensure the following components and configurations are in place:

* **GitHub Account & Repository**: An active GitHub account with a private repository named `terraform-iam-lab`.
* **AWS Account**: An active AWS account with an IAM user configured for programmatic access (Access Key ID and Secret Access Key) with `AdministratorAccess` policy (for lab simplicity).
* **Okta Developer Organization**: An active Okta Developer Org with an Administrator account and a generated Okta API Token with sufficient permissions.
* **AWS S3 Bucket for Terraform State**: A dedicated S3 bucket named `iam-terraform-state-bucket` (in `eu-central-1`), with versioning, block public access, and default encryption enabled.
* **AWS DynamoDB Table for State Locking**: A DynamoDB table named `iam-terraform-state-lock` (in `eu-central-1`), with a primary key named `LockID` (String type).
* **Terraform CLI**: Installed and configured locally.
* **Git**: Installed and configured locally.
* **GitHub Repository Secrets** (`Settings > Secrets and variables > Actions`):

  * `OKTA_API_TOKEN`: Your Okta API Token. *(Matches Terraform env var `TF_VAR_OKTA_API_TOKEN` used below.)*
  * `AWS_ACCESS_KEY_ID_ADMIN`: Your AWS IAM user Access Key ID.
  * `AWS_SECRET_ACCESS_KEY_ADMIN`: Your AWS IAM user Secret Access Key.

## IV. Configuration Steps: CI/CD Pipeline Setup

This section outlines the steps to establish the CI/CD pipeline.

### A. Local Repository Setup & Synchronization

1. **Create GitHub repository and ensure a Clean Local Repository**:

   Create proper local repository file structure

```
terraform-iam-lab/
├─ terraform-aws-lab/
│  ├─ versions.tf
│  └─ main.tf
├─ okta-terraform-lab/
│  ├─ versions.tf
│  └─ main.tf
└─ .github/workflows/terraform.yml
```

* **Create repository in GitHub** <img width="792" height="813" alt="Screenshot 2025-08-02 232223" src="https://github.com/user-attachments/assets/40d838c4-8d34-4792-877b-2dbad10e894d" /> <img width="621" height="498" alt="image" src="https://github.com/user-attachments/assets/7154ec5c-0aec-46e6-98ed-5e36018321e1" />

* **Securely store API credentials as GitHub secrets**
  **Repo settings > Security > Secrets and variables > Actions > New repository secret** <img width="888" height="957" alt="Screenshot 2025-08-03 011449" src="https://github.com/user-attachments/assets/9bf03106-4657-4f1d-8700-86ca6f793e52" /> <img width="605" height="826" alt="Screenshot 2025-08-03 012824" src="https://github.com/user-attachments/assets/65ad1e22-cb89-4eaa-840a-becffb16db5d" />

* **Initialize Git and create `.gitignore`** <img width="931" height="312" alt="Screenshot 2025-08-03 000051" src="https://github.com/user-attachments/assets/214fb28b-cd26-4912-9cdb-6fbcf762b3ff" /> <img width="1110" height="592" alt="Screenshot 2025-08-03 000130" src="https://github.com/user-attachments/assets/e99b6710-58f0-4c14-a668-4df3c1d74742" />

* **Initialize changes on the correct branch, add and commit** <img width="686" height="232" alt="Screenshot 2025-08-03 004730" src="https://github.com/user-attachments/assets/865426c1-83f6-4787-9d30-585c7562d44e" /> <img width="601" height="209" alt="Screenshot 2025-08-03 004831" src="https://github.com/user-attachments/assets/7f8f80a3-4d33-440a-813b-6e2c6443494b" />

> I made some error in my file structure, causing mismatch between my local repo and GitHub repository (GitHub repository was correct).

* Delete any existing local `terraform-iam-lab` folder to ensure a completely clean slate.
* Open your terminal and navigate to your desired parent directory (e.g., `C:/Terraform`).
* Clone the repository: `git clone https://github.com/Olatife-01/terraform-iam-lab.git`

2. **Navigate to Repository Root**: `cd terraform-iam-lab`

3. **Verify Branch and Pull Latest**:

   * Ensure you are on the `main` branch: `git checkout main`
   * Pull latest changes: `git pull origin main --rebase` (to ensure local is up-to-date with remote history). <img width="623" height="308" alt="Screenshot 2025-08-03 004905" src="https://github.com/user-attachments/assets/afb9f4ac-e9a3-436e-a53c-ed91c1860aa5" />

> If there is a conflict message, open the file, resolve the conflict markers, save, then continue the rebase with `git rebase --continue`.

<img width="641" height="185" alt="Screenshot 2025-08-03 004950" src="https://github.com/user-attachments/assets/a3c932af-7fed-451c-9851-2ed8df9b304c" />
<img width="549" height="224" alt="Screenshot 2025-08-03 005056" src="https://github.com/user-attachments/assets/749c3f04-0b8c-4e0b-b195-52810010ebb4" />

4. **Update `.gitignore`**:

Ensure it contains:

```
# Ignore Terraform provider and state files
.terraform/
*.tfstate
*.tfstate.backup
.terraform.lock.hcl
# Other sensitive files
.env
```

> After fixing any conflict, press `Esc`, type `:wq` to save in Vim, run `git rebase --continue`, then push to GitHub.

<img width="1892" height="1094" alt="Screenshot 2025-08-03 003546" src="https://github.com/user-attachments/assets/66ca7446-c11f-4e81-838f-cbea7150927a" />
<img width="550" height="121" alt="Screenshot 2025-08-03 005336" src="https://github.com/user-attachments/assets/7d3b270f-35d0-45d0-bf92-bda36892fbde" />
<img width="660" height="245" alt="Screenshot 2025-08-03 005454" src="https://github.com/user-attachments/assets/cd8fc127-6f56-42ba-9bab-cfa0862022b3" />

### B. Remote State Backend (S3 + DynamoDB) — Quick Steps

1. **Create S3 state bucket**
   Create a private, versioned bucket in `eu-central-1` (e.g., `iam-terraform-state-bucket`). Enable **Block public access** and **Default encryption**. <img width="1841" height="674" alt="Screenshot 2025-08-05 110419" src="https://github.com/user-attachments/assets/44717115-4f26-4664-9ddd-7fa1c0b686a4" />

2. **Create DynamoDB lock table**
   Create table `iam-terraform-state-lock` with **Partition key** `LockID (String)`; keep default (on-demand) capacity. <img width="1899" height="1095" alt="Screenshot 2025-08-05 110954" src="https://github.com/user-attachments/assets/b1e50346-7678-44c5-a32a-4b7d33ae9a5f" />

3. **Point Terraform to the backend**
   Add this to each project’s `versions.tf`, then run `terraform init -reconfigure` in each folder to migrate local state:

   **AWS (`terraform-aws-lab/versions.tf`)**

   ```hcl
   terraform {
     backend "s3" {
       bucket         = "iam-terraform-state-bucket"
       key            = "aws-project/terraform.tfstate"
       region         = "eu-central-1"
       encrypt        = true
       dynamodb_table = "iam-terraform-state-lock"
     }
   }
   ```

   **Okta (`okta-terraform-lab/versions.tf`)**

   ```hcl
   terraform {
     backend "s3" {
       bucket         = "iam-terraform-state-bucket"
       key            = "okta-project/terraform.tfstate"
       region         = "eu-central-1"
       encrypt        = true
       dynamodb_table = "iam-terraform-state-lock"
     }
   }
   ```

   (You’ll see Terraform acquire the state **lock** during plan/apply.) <img width="1981" height="754" alt="Screenshot 2025-08-05 112811" src="https://github.com/user-attachments/assets/a3258d45-0f25-41c4-9924-516b94560223" />

4. **Verify state + locks**
   Confirm the two state objects exist in S3 and corresponding **LockID** items appear in DynamoDB when plans run. <img width="1817" height="1254" alt="Screenshot 2025-08-05 115008" src="https://github.com/user-attachments/assets/e513076b-7572-4ff2-96cb-4c8e56fd9b02" />

5. **Commit & trigger pipeline**
   Commit the backend changes and push; watch GitHub Actions run `init/fmt/validate/plan/apply` using the shared backend. <img width="728" height="760" alt="Screenshot 2025-08-05 124821" src="https://github.com/user-attachments/assets/f0dc69cf-b454-49cf-8d59-d769652197b0" />

### C. Terraform Configuration Updates (Local) to avoid Terraform trying to destroy and recreate the already existing resources

1. **For `terraform-aws-lab`**:

   * Open `versions.tf` and ensure the S3 backend block (shown above) is present.
   * Open `main.tf`. Add `lifecycle { prevent_destroy = true }` to critical resources (e.g., `aws_iam_group`, `aws_iam_user`, `aws_s3_bucket`, `aws_security_group`, `aws_instance`).
     *Note:* This is an extra safety rail for the lab. In production, use with care as it can block legitimate refactors; remote state + imports typically prevent unintended re-creates.
   * Run `terraform init` (to initialize the backend and migrate local state to S3).

2. **For `okta-terraform-lab`**:

   * Open `versions.tf` and ensure the S3 backend block (shown above) is present.
   * Open `main.tf`. Add `lifecycle { prevent_destroy = true }` to `okta_group` and `okta_user` resources (same caution as above).
   * Run `terraform init` (to initialize the backend and migrate local state to S3).

### D. GitHub Actions Workflow File (`.github/workflows/terraform.yml`)

1. **Create the Workflow Directory**: from repo root: `mkdir -p .github/workflows`
2. **Create `terraform.yml`** with PR-aware conditions and fmt/validate stages:

```yaml
name: "Terraform CI/CD"

on:
  push:
    branches: [ main, okta-configs ]
  pull_request:
    branches: [ main, okta-configs ]

permissions:
  contents: read

jobs:
  terraform:
    name: "Run Terraform Plan and Apply"
    runs-on: ubuntu-latest
    env:
      TF_IN_AUTOMATION: "true"
      TF_VAR_OKTA_API_TOKEN: ${{ secrets.OKTA_API_TOKEN }}
      AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID_ADMIN }}
      AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY_ADMIN }}
      AWS_DEFAULT_REGION: eu-central-1

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Terraform CLI
        uses: hashicorp/setup-terraform@v1
        with:
          terraform_version: 1.x.x

      # --- AWS (main) ---
      - name: Terraform Format (AWS)
        if: github.ref == 'refs/heads/main' || (github.event_name == 'pull_request' && github.base_ref == 'main')
        run: terraform fmt -check -recursive
        working-directory: terraform-aws-lab

      - name: Terraform Validate (AWS)
        if: github.ref == 'refs/heads/main' || (github.event_name == 'pull_request' && github.base_ref == 'main')
        run: terraform validate
        working-directory: terraform-aws-lab

      - name: Initialize AWS Terraform
        if: github.ref == 'refs/heads/main' || (github.event_name == 'pull_request' && github.base_ref == 'main')
        run: terraform init -input=false -no-color
        working-directory: terraform-aws-lab

      - name: Terraform Plan (AWS)
        if: github.ref == 'refs/heads/main' || (github.event_name == 'pull_request' && github.base_ref == 'main')
        run: terraform plan -input=false -lock-timeout=5m -no-color
        working-directory: terraform-aws-lab

      - name: Terraform Apply (AWS)
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        run: terraform apply -auto-approve -input=false -lock-timeout=5m -no-color
        working-directory: terraform-aws-lab

      # --- Okta (okta-configs) ---
      - name: Terraform Format (Okta)
        if: github.ref == 'refs/heads/okta-configs' || (github.event_name == 'pull_request' && github.base_ref == 'okta-configs')
        run: terraform fmt -check -recursive
        working-directory: okta-terraform-lab

      - name: Terraform Validate (Okta)
        if: github.ref == 'refs/heads/okta-configs' || (github.event_name == 'pull_request' && github.base_ref == 'okta-configs')
        run: terraform validate
        working-directory: okta-terraform-lab

      - name: Initialize Okta Terraform
        if: github.ref == 'refs/heads/okta-configs' || (github.event_name == 'pull_request' && github.base_ref == 'okta-configs')
        run: terraform init -input=false -no-color
        working-directory: okta-terraform-lab

      - name: Terraform Plan (Okta)
        if: github.ref == 'refs/heads/okta-configs' || (github.event_name == 'pull_request' && github.base_ref == 'okta-configs')
        run: terraform plan -input=false -lock-timeout=5m -no-color
        working-directory: okta-terraform-lab

      - name: Terraform Apply (Okta)
        if: github.ref == 'refs/heads/okta-configs' && github.event_name == 'push'
        run: terraform apply -auto-approve -input=false -lock-timeout=5m -no-color
        working-directory: okta-terraform-lab
```

### E. Final Git Commit and Push

1. **Navigate to Repository Root**: `cd C:/Terraform/terraform-iam-lab`
2. **Stage all changes**: `git add .`
3. **Commit changes**: `git commit -m "feat: CI/CD with remote backend, fmt/validate, and PR-aware conditions"`
4. **Push to `main` branch**: `git push origin main`
5. **Push `okta-configs` branch**: `git push origin okta-configs` (if not already pushed) <img width="874" height="430" alt="Screenshot 2025-08-03 014923" src="https://github.com/user-attachments/assets/6d5d884e-dc92-450b-b2ff-7d850e9390f8" />

## V. General Analysis

The successful implementation of this CI/CD pipeline marks a significant milestone for the Enterprise IAM Lab Project. It validates the project's ability to manage infrastructure as code in an automated, secure, and idempotent manner. The mono-repo strategy, combined with conditional execution, provides a scalable and maintainable framework for future IAM deployments.

## VI. Lessons Learned

* **Idempotency & Remote State are Foundational**: The recurring "already exists" errors underscored the absolute necessity of a shared, persistent remote state (S3 + DynamoDB) for idempotent deployments in CI/CD environments.
* **Precision in Pathing**: GitHub Actions `working-directory` paths must be meticulously defined and relative to the repository root. Subtle errors in pathing were a consistent source of pipeline failures.
* **Git Discipline is Paramount**: Complex scenarios involving multiple branches, manual file movements, and diverging histories necessitate strict adherence to Git commands (`git pull --rebase`, `git reset --hard`, `git rm --cached`, `git push -u origin <local>:<remote>`).
* **Case-Sensitivity Across Platforms**: Keep Terraform variables and environment variables exactly aligned (e.g., `variable "OKTA_API_TOKEN"` ↔ `TF_VAR_OKTA_API_TOKEN`).
* **`.gitignore` is a Security Control**: Exclude `.terraform/`, provider binaries, and all `*.tfstate*` files.
* **Conditional Logic for Mono-Repos**: Branch-aware `if:` conditions let each path run only when it should.
* **Troubleshooting Requires Patience & Systemic Approach**: Isolate variables, verify each step, and keep the backend authoritative.

# Advanced CI/CD: Implementing a Git Workflow for Okta IaC

## I. Objective & Purpose

The pipeline is the guardrail; Git is the change ledger. I protect `main`, require PRs, and let Actions run `fmt/validate/plan` on every PR so reviewers see **exactly** what Terraform intends to do. Only after approval do I merge, which triggers a dedicated `apply`. That sequence gives me attribution, repeatability, and an approval trail suitable for audits.

## II. Technical Thought Process & Design Decisions

* **Main Branch Protection**: The `main` branch, which represents the live state of our Okta tenant, must be protected. No changes should be pushed directly to it.
* **Peer Review**: All code changes must be reviewed by at least one other team member.
* **Automated Validation**: The CI/CD pipeline checks every proposed change for formatting, syntax, and planned impact.
* **Auditability**: Every step—from commit to merge—is recorded in Git history and PRs.

## III. Conceptual Workflow: Step-by-Step

### Step 1: Create a Feature Branch

```
git checkout -b feature/add-new-admin-group
```

### Step 2: Write the Terraform Code

```hcl
resource "okta_group" "admin_support" {
  name        = "Admin_Support"
  description = "Group for administrative support personnel."
}
```

### Step 3: Commit and Push the Changes

```
git add main.tf
git commit -m "feat: Add new 'Admin_Support' group"
git push origin feature/add-new-admin-group
```

<img width="878" height="433" alt="Screenshot 2025-08-03 010944" src="https://github.com/user-attachments/assets/23ebc982-5966-4ef2-a992-002598b36a63" />
<img width="882" height="675" alt="Screenshot 2025-08-03 010701" src="https://github.com/user-attachments/assets/d2097d47-4066-407b-b84e-146d055419e4" />

### Step 4: Create a Pull Request (PR)

Open a PR to merge `feature/add-new-admin-group` into `main`.

### Step 5: Automated Validation (CI/CD Pipeline)

* `terraform fmt --check`
* `terraform validate`
* `terraform plan` (posted as a PR comment or visible in logs)

### Step 6: Peer Review & Approval

A teammate reviews the code and plan output, then approves.

### Step 7: Merge and Deploy

Merging to `main` triggers a dedicated `apply` job, deploying the approved changes. <img width="1293" height="573" alt="Screenshot 2025-08-06 133531" src="https://github.com/user-attachments/assets/71e839c2-1f74-4dcf-bf03-5579e957cab6" />

**Alerting for failed Action jobs** <img width="1227" height="783" alt="Screenshot 2025-08-06 134924" src="https://github.com/user-attachments/assets/7604f051-3faa-4bcc-9c4b-2a993980294d" />

> I keep **AWS** changes on `main` and **Okta** changes on `okta-configs`. You can tighten this further with branch protection + required checks.

### D) Commit & push

```bash
git add .
git commit -m "feat: CI/CD with S3+DynamoDB backend and branch-scoped jobs"
git push origin main
git push origin okta-configs
```

## V. **Challenges Encountered & Resolutions (Evolution of Configuration):**

1. **Initial "Resource Already Exists" Errors**
   **Resolution**: Implemented the **S3 + DynamoDB** remote backend so runners always start from the current state.
2. **Incorrect Working Directory Paths**
   **Resolution**: Corrected `working-directory` to top-level subfolders (`terraform-aws-lab`, `okta-terraform-lab`).
3. **Git Repository Structure & Synchronization Issues**
   **Resolution**: Reset problematic local histories, re-cloned, and used clear feature branches with clean staging/commits.
4. **Terraform Variable Case-Sensitivity**
   **Resolution**: Matched env var and variable names exactly (`TF_VAR_OKTA_API_TOKEN` ↔ `variable "OKTA_API_TOKEN"`).
5. **State Locking Failures**
   **Resolution**: Deleted stale lock items in DynamoDB when needed; added `-lock-timeout=5m` to plan/apply.
6. **Large Files in Git**
   **Resolution**: `.gitignore` excludes `.terraform/` and all state files.

## VI. Next Steps & Enhancements

* **Expand Terraform Scope** across more Okta/AWS resources.
* **Integrate Policy-as-Code** (Sentinel/OPA) before apply.
* **Advanced Secrets Management** with Vault-generated credentials for Terraform.
* **Automated Tests** for IAM policies and access paths.
* **Drift Detection** scheduled against live environments.

---

If you want, I can also drop in a tiny OIDC note (GitHub Actions → AWS role) next time—keeps secrets even tighter—with no other structural changes.
