# Audit & Compliance Evidence Pack

**Enterprise IAM Lab — Okta · AWS · AD · BambooHR · Vault · Terraform · GitHub Actions · Splunk**

## 1) Executive Summary

This pack consolidates **auditable evidence** showing how my Enterprise IAM Lab enforces identity, access, and change controls across **workforce identity (Okta)**, **cloud infrastructure (AWS)**, **on-prem identity (Active Directory)**, **HRIS (BambooHR)**, **secrets/PAM (HashiCorp Vault)**, **IaC (Terraform)**, **CI/CD (GitHub Actions)**, and **centralized logging (Splunk Cloud)**. It maps implemented controls to **ISO/IEC 27001** Annex A, supports **SOX (ITGC)** objectives, and aligns to **SOC 2** / **NIST CSF** practices.
Scope includes SSO & federation, JML automation, access reviews, change management, logging/alerting, and secrets governance—plus **Okta IGA** (Access Requests & Certifications) and **Okta PAM** program integrations.

---

## 2) Systems in Scope & Control Roles

| Domain                | System                                                                          | Role in Control Environment                                                                                        | Primary Owner |
| --------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------- |
| Workforce IAM         | **Okta**                                                                        | IdP, MFA, SSO, policy enforcement, group model, IGA (Access Requests, Access Certifications), Workflows automation | IAM Admin     |
| Cloud IAM & Workloads | **AWS** + **IAM Identity Center**                                               | Federated access (SAML), SCIM provisioning, permission sets (least-privilege), EC2/S3 resources for testing        | Cloud/IAM     |
| Directory Services    | **Active Directory**                                                            | Directory source for Windows assets; integrated to Okta via AD Agent; scoped Lab OU                                | IAM/IT Ops    |
| HRIS                  | **BambooHR**                                                                    | **System of Record** for Joiner/Mover/Leaver; feeds Okta via Workflows/connector                                   | HR + IAM      |
| PAM & Secrets         | **HashiCorp Vault**                                                             | Okta Auth Method (policy mapping), dynamic AWS IAM creds (JIT), KV secrets                                         | SecOps        |
| IaC                   | **Terraform**                                                                   | Declarative infra for Okta & AWS; remote state (S3) + lock (DynamoDB)                                              | DevOps        |
| CI/CD                 | **GitHub Actions**                                                              | Fmt/validate/plan/apply; branch-scoped jobs (AWS on `main`, Okta on `okta-configs`); PR approvals                  | DevOps        |
| SIEM                  | **Splunk Cloud**                                                                | Centralized Okta System Logs (Splunk Add-on pull), dashboards, alerts, scheduled reports                           | SecOps        |
| Integrated Apps       | **Google Workspace (custom SAML)**, **Salesforce**, **Zendesk ** | SSO + (where applicable) SCIM; federated access visibility                                                         | App Owners    |

> **Note:** Google Workspace SSO is via **custom SAML** (prebuilt connector was unreliable; GCP policy blocked P12 key creation for provisioning). AWS federation is via **IAM Identity Center** with **SAML + SCIM**, tested end-to-end..

---

## 3) Control Objectives & Framework Mapping

### 3.1 ISO/IEC 27001 Annex A (2013/2022) — Summary Map

| Control                                          | Objective                                      | Implementation (Evidence)                                                                     |
| ------------------------------------------------ | ---------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **A.5/A.6** Organization of Information Security | Roles, responsibilities, segregation of duties | RACI in §8; distinct GitHub roles (developer/reviewer), IAM Admin vs SecOps in Okta/AWS       |
| **A.8** Asset Management                         | Identify information assets                    | System inventory §2; Terraform state in S3 (versioned); indexes in Splunk                     |
| **A.9** Access Control                           | Policy, provisioning, MFA, least-privilege     | Okta sign-on/password/MFA policies; IGA requests; SCIM to AWS SSO; permission sets; Vault JIT |
| **A.12.1 / A.12.2** Change Management & Capacity | Controlled changes, tooling                    | GitHub PRs + protected branches; Actions logs; DynamoDB locks                                 |
| **A.12.4** Logging & Monitoring                  | Log security events & admin actions            | Splunk Add-on for Okta; dashboards; alerts; scheduled report                                  |
| **A.13** Communications Security                 | Secure channels                                | SAML, SCIM, HTTPS; secrets via GitHub Secrets; Vault for runtime secrets                      |
| **A.14** System Acquisition/Dev                  | Security in SDLC/IaC                           | Terraform fmt/validate/plan gates; policy-as-code roadmap                                     |
| **A.18** Compliance                              | Records protection; audit                      | S3 versioning; Splunk export; PR history; monthly evidence schedule                           |

### 3.2 SOX (ITGC) — Focus Areas

| ITGC Area                     | What We Demonstrate                                                        | Evidence                                                                              |
| ----------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **Access to Programs & Data** | Joiner/Mover/Leaver from **BambooHR → Okta → AWS/Apps**; MFA; role mapping | Workflows runs; AWS SSO assignments; Splunk events (create/deactivate); Okta policies |
| **Change Management**         | **PR + review** required; CI validates; backend state prevents drift       | PR screenshots; Actions logs; S3/DynamoDB backend entries                             |
| **Computer Operations**       | Monitoring/alerting on identity events; scheduled reports                  | Splunk dashboards/alerts; monthly PDF export & distribution log                       |

### 3.3 SOC 2 (Common Criteria) & NIST CSF (High Level)

* **CC6 (Access Controls)** → Okta policies, MFA, least-privilege via permission sets, Vault JIT creds
* **CC7 (Change & Monitoring)** → CI/CD review & logging; Splunk alerting
* **ID.AM / PR.AC / DE.AE** in **NIST CSF** covered by inventory, access control, and event detection flows

---

## 4) Policies & Standards Implemented

* **Okta Password Policy**: Min length 10; lower/upper/number/symbol; common-password restrictions; history (last 4); max age 90 days; min age 1 day; lockout after 10 failures.
* **Okta MFA**: Okta Verify enforced per sign-on policy; enrollment events tracked in Splunk.
* **Okta Sign-On Policies**: Context-aware; stronger assurance for admin apps; step-up for sensitive targets.
* **AWS Access**: SSO via IAM Identity Center; permission sets (e.g., `OktaReadOnlyAccess`); **no** IAM users for humans; Okta SCIM group synchronization.
* **PAM**: Vault Okta Auth Method for login; **group→policy** mapping; dynamic AWS credentials (short-lived) with **ReadOnlyAccess** for JIT test access.
* **IGA**: Okta **Access Requests** with approvers; **Access Certifications** quarterly for Salesforce, Google Workspace, and AWS permission sets; reviewer actions stored and exportable.
* **Change Control**: GitHub **protected branches**; PR approvals mandatory; CI gates (`fmt/validate/plan`) and controlled `apply`.
* **Logging & Monitoring**: Okta System Log → **Splunk Add-on** (pull); dashboards (admin actions, lifecycle, MFA); two alerts (brute-force, unusual location); monthly scheduled exports.

---

## 5) Provisioning & Federation (End-to-End)

### 5.1 Authoritative Source & JML

* **BambooHR** is the **system of record**. Okta Workflows (or BambooHR/Okta connector) polls for **new hires / changes / terminations**.
* **Joiner**: Create Okta user → Assign baseline groups → App entitlements (e.g., Salesforce) → (Marketing only) invoke Lambda to create S3 folder via Workflows.
* **Mover**: On department change to “Sales”, Workflows adds user to **Salesforce Sales Team**.
* **Leaver**: Deactivate in Okta; downstream access revoked; Splunk shows deactivation events.

### 5.2 Federation Targets

* **AWS**: **SAML** to IAM Identity Center + **SCIM** group sync; **permission sets** enforce least-privilege; test confirms **AccessDenied** on writes for read-only users.
* **Google Workspace**: **Custom SAML** app (prebuilt failed; GCP policy blocked service account key for provisioning). SSO validated; provisioning marked as out-of-scope due to org policy.
* **Salesforce**: SSO & entitlement via Okta groups (where configured).

### 5.3 Active Directory

* **Okta AD Agent** joins lab AD; **Lab OU** in scope for sync; imported users/groups visible in Okta; (if enabled) write-back policies carefully constrained. Evidence: Directory Integrations page; last import logs; agent health.

---

## 6) PAM & Secrets

* **Vault Okta Auth Method**: Users authenticate to Vault with Okta creds; group `lab User` mapped to Vault policy `kv-read-policy`. Evidence: Vault UI (auth methods), `auth/okta/groups/<group>` mapping; Postman `X-Vault-Token` lookup confirms policy.
* **Dynamic AWS IAM Credentials**: Vault AWS secrets engine issues **short-lived** keys (validated by `aws s3 ls` allowed, `aws s3 mb` denied). Evidence: Vault role page; generation event; CloudWatch/Vault logs.
* **Roadmap**: Extend to database secrets; SSH CA; time-bound elevation flows coordinated with Okta Access Requests (assumed in IGA).

---

## 7) Centralized Logging & Monitoring (Splunk)

* **Ingestion**: **Splunk Add-on for Okta Identity Cloud** (pull via API); sourcetype `okta:identity:cloud`, index `main`; historical backfill via **Start Date** and checkpoint reset.
* **Dashboards** (“MellonRyon Dashboard”):

  * **Admin Activity**: lists privileged actions, actor, source IP.
  * **User Lifecycle**: create/deactivate summary.
  * **MFA Enrollment/Activation**: enrollment posture.
* **Alerts**:

  * **Brute-Force** (≥4 failures by same user/IP over last hour).
  * **Unusual Location Logins** (success from countries not on allow-list).
* **Reporting**: **Monthly** PDF export & email distribution; retained alongside PR evidence and S3 state versions.

**Canonical SPL (validated in the lab)**

```spl
/* Admin Activity */
index="main" sourcetype="okta:identity:cloud"
| search actor.type="User" OR actor.type="System"
| rename actor.alternateId as Admin, eventType as Action, client.ipAddress as SourceIP
| table _time, Admin, Action, outcome.result, SourceIP
| sort -_time
```

```spl
/* User Lifecycle */
index="main" sourcetype="okta:identity:cloud"
| search (eventType="user.lifecycle.create" OR eventType="user.lifecycle.deactivate")
| rename actor.alternateId as Initiator, target{}.alternateId as TargetUser, eventType as EventType
| table _time, Initiator, TargetUser, EventType
| sort -_time
```

```spl
/* MFA Enrollment/Activation */
index="main" sourcetype="okta:identity:cloud"
| search eventType="user.mfa.factor.enroll" OR eventType="user.mfa.factor.activate"
| rename actor.alternateId as User, outcome.reason as OutcomeReason, client.userAgent.os as UserOS
| table _time, User, OutcomeReason, UserOS
| sort -_time
```

---

## 8) Infrastructure as Code & Change Control

* **Terraform**: All Okta/AWS resources are declared; **remote backend** in **S3** (versioned) with **DynamoDB locks** ensures single source of truth and prevents concurrent corruption.
* **GitHub Actions**:

  * **Branch-scoped jobs**: `main` → AWS; `okta-configs` → Okta.
  * Gates: `terraform fmt --check`, `terraform validate`, `terraform plan`; `apply` only on approved push to protected branch.
  * **Secrets** injected from GitHub Secrets (e.g., `TF_VAR_OKTA_API_TOKEN`, `AWS_*`).
* **Evidence**: PR approvals, workflow logs, `plan` output artifacts, S3 object versions, DynamoDB lock events during runs.

**Backend example (per project)**

```hcl
terraform {
  backend "s3" {
    bucket         = "iam-terraform-state-bucket"
    key            = "<project>/terraform.tfstate"
    region         = "eu-central-1"
    encrypt        = true
    dynamodb_table = "iam-terraform-state-lock"
  }
}
```

---

## 9) IGA

* **Access Requests**: Users request app access (e.g., Salesforce, AWS permission set) through Okta; approval routing to manager/app owner; auto-provision via SCIM or group push.
* **Access Certifications**: Quarterly reviews for **Salesforce** roles, **Google Workspace** SSO groups, and **AWS** permission sets; reviewer attestations recorded; revocations issued automatically; certification reports exported and archived.
* **Metrics**: % timely reviews, revocation SLAs, exceptions aged >30 days.

---

## 10) Tests Performed & Outcomes (Assurance)

| Control Area                | Test                                                   | Result                                                |
| --------------------------- | ------------------------------------------------------ | ----------------------------------------------------- |
| **MFA enforcement**         | Enroll and login with Okta Verify; verify Splunk event | **Pass** (events visible; policy enforced)            |
| **Least-privilege in AWS**  | Attempt S3 bucket create / EC2 stop as ReadOnly user   | **Denied**, as expected                               |
| **SSO to Google Workspace** | IdP-initiated SSO via custom SAML                      | **Success** (provisioning intentionally out-of-scope) |
| **SCIM → AWS SSO**          | Push `Lab users` group; assign permission set          | **Pass** (group appears; access portal functional)    |
| **Joiner/Mover/Leaver**     | Create/move/deactivate from BambooHR → Okta → Apps     | **Pass** (Workflows logs and Splunk events)           |
| **Vault JIT creds**         | Generate dynamic AWS keys; read allowed, write denied  | **Pass**                                              |
| **CI gating**               | PR raised; fmt/validate/plan block bad code            | **Pass**                                              |
| **Monthly reporting**       | Splunk dashboard export & email delivery               | **Pass**                                              |

---

## 11) Exceptions, Risks & Compensating Controls

* **Google Workspace Provisioning**: Blocked by org policy (`iam.managed.disableServiceAccountKeyCreation`). **Risk**: manual drift for GW users. **Compensating**: SSO only; changes tracked in Okta; review GW membership in quarterly certifications; revisit with keyless or service-account-alt approach.
* **Okta Native Log Streaming**: Push method intermittently deactivated; **Mitigation**: **Splunk Add-on (pull)** proven reliable; monthly export covers audit evidence.
* **AD Scope (Lab)**: Integration limited to Lab OU; **Mitigation**: Documented scope; production playbook would extend OU coverage and password write-back as needed.
* **AWS Workload Logs**: CloudTrail not centralized in this lab. **Mitigation**: Identity events are covered via Okta/Splunk; **Roadmap** adds CloudTrail → Splunk.

---

## 12) Operating Rhythm (Evidence Calendar)

| Frequency     | Activity                                                   | Artefact                                   |
| ------------- | ---------------------------------------------------------- | ------------------------------------------ |
| **Daily**     | Splunk alert review; triage exceptions                     | Alert history, incident notes              |
| **Weekly**    | CI/CD run review; failed plan/apply                        | Actions logs; PR audit                     |
| **Monthly**   | Dashboard **PDF** export & email                           | Splunk report; mail log                    |
| **Quarterly** | **Access Certifications** (Okta IGA) for AWS/GW/Salesforce | Certification reports, remediation tickets |
| **Quarterly** | Policy review (sign-on/password/MFA)                       | Okta screenshots & change log              |
| **Ad hoc**    | Break-glass & PAM tests                                    | Vault logs; temporary access evidence      |

---

## 13) RACI (Light)

* **IAM Admin**: Okta policies, groups, federation, IGA campaigns, Workflows
* **SecOps / SIEM**: Splunk ingestion, dashboards, alerts, monthly exports
* **Cloud/IAM**: AWS SSO, permission sets, SCIM integration
* **DevOps**: Terraform modules, CI/CD, backend state integrity
* **HR**: BambooHR data accuracy, hire/term timeliness
* **Audit/Compliance**: Evidence requests, control testing, exception tracking

---

## 14) Data Retention & Integrity

* **Okta System Log → Splunk**: Retained per index policy (lab default); monthly PDF exports archived for 12–24 months.
* **Terraform State**: S3 with **versioning**; DynamoDB locks; server-side encryption enabled.
* **GitHub**: PR history & workflow logs retained per repo settings; branch protections enforced.

---

## 15) Roadmap (Control Maturity)

* **Add CloudTrail & GuardDuty → Splunk** for fuller infra visibility (SOX/SOC2).
* **Policy-as-Code** (OPA/Sentinel) to gate Terraform plans.
* **Expand Vault**: DB secrets, SSH CA; integrate with Access Requests for time-bound elevation.
* **App Coverage**: Bring Slack/Zendesk; SCIM where possible.
* **DR Playbooks**: Rehydrate Okta/AWS from Terraform; test quarterly.

---

## Appendix A — Reference Queries & Commands

**Splunk (canonical searches)** — see §7.

**Terraform backend (per project)** — see §8.

**Vault Policy (example)**

```hcl
# kv-read-policy (already applied)
path "secret/data/*" {
  capabilities = ["read", "list"]
}
```

**AWS Read-only validation**

```bash
aws s3 ls                         # allowed
aws s3 mb s3://should-fail-123    # AccessDenied (expected)
```

---

## Appendix B — Evidence Checklist (Auditor expected questions)

* Okta **password & sign-on policy** screenshots, effective assignments
* Okta **MFA** enrollment posture & enforcement proof (Splunk events)
* **IGA**: latest campaign exports (attestations & revocations)
* **AWS SSO**: SCIM sync status; assigned permission sets; Access Portal screenshot
* **Vault**: auth method config; group-policy mapping; dynamic creds generation proof
* **CI/CD**: one recent PR with review; `plan` output; `apply` logs; protected branch settings
* **Terraform backend**: S3 bucket properties (versioning), DynamoDB lock entries
* **Splunk**: dashboard PDF (last month); alert definitions; alert trigger samples
* **BambooHR→Okta**: one joiner and one leaver trail (Workflows run history + Splunk events)
* **AD**: Okta Directory Integration status, last import log, scoped OU

---

**Conclusion:** My lab demonstrates **defensible, auditable** identity and access controls with **end-to-end evidence**: policy → provisioning → least-privilege → monitoring → change control. Where constraints exist (e.g., Google Workspace provisioning), they’re explicitly documented with **compensating controls** and a path to remediation.
