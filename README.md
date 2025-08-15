# Okta-IAM-Enterprise-Lab-Project

## Project Overview

This repository is a portfolio of a hands-on lab project focused on designing, building, and documenting a modern, zero-trust-aligned Identity and Access Management (IAM) architecture. The project demonstrates practical experience with a variety of cloud and on-premises technologies, including **Okta** as the central identity provider, automation via **Terraform** and **Okta Workflows**, and observability with **Splunk Cloud**.

## Project Goal

I designed, built, and documented a robust enterprise IAM lab using **Okta** as the central Identity Provider. The aim is to demonstrate practical IAM integration, security guardrails, and automation in a realistic but non-production environment.

## Flow

* Users authenticate with **Okta** and access AWS/SaaS via **SSO**.
* Where supported, accounts are created/updated via **SCIM**.
* Policies enforce **MFA**, **adaptive risk**, **network zones**, and **device assurance**.
* Infrastructure/identity changes are automated or reproducible (**Workflows**, **Terraform**).
* **Okta System Logs** are designed to flow to **Splunk Cloud** for dashboards/alerts.
* Evidence (reports/logs/Terraform history) can be bundled for audit.
<img width="734" height="1381" alt="image" src="https://github.com/user-attachments/assets/dc318921-db87-49b3-903c-82f0ccbf560e" />

## Components

### Identity Sources

* **BambooHR (SCIM)** — HR-as-master design
* **Active Directory** — Okta AD Agent, bi-directional directory sync

### Identity Hub (Okta)

* **Okta** — Universal Directory, Groups/Rules, Policies (MFA, Adaptive, Zones), Device Assurance, End-User Self-Service, App Integrations.
* \**Okta Identity Governance / Okta Privileged Access*

<img width="822" height="587" alt="image" src="https://github.com/user-attachments/assets/a595ab51-ee94-417a-bf61-465180fe20e1" />
<img width="672" height="648" alt="image" src="https://github.com/user-attachments/assets/ac54f3d7-ce64-47e3-a832-546333c0c314" />

### Downstream Applications

* **Salesforce** — SAML SSO + SCIM
* **Google Workspace** — SSO only; provisioning blocked by org policy
* **Zendesk** — SAML SSO *(implemented)*
* **Slack** — SSO (SCIM optional; not enabled in this lab)
<img width="648" height="708" alt="image" src="https://github.com/user-attachments/assets/e1c826b1-925c-4633-ba20-4a49d242b699" />

### Cloud Access

* **AWS IAM Identity Center** — SSO + SCIM, permission sets, group assignments

### Automation

* **Okta Workflows** — JML patterns; Lambda-triggered S3 folder creation; daily de-provision audit email
* **Terraform (IaC)** — Okta & AWS resources; **S3 + DynamoDB** backend; Git CI/CD
<img width="840" height="663" alt="image" src="https://github.com/user-attachments/assets/c6a80a30-572a-40a2-9dbf-cacc32156269" />

### Observability / SIEM

* **Splunk Cloud** — Ingestion of Okta System Logs, dashboards, and email alerts 
<img width="876" height="550" alt="image" src="https://github.com/user-attachments/assets/6f75821c-968d-4395-8ea8-d42879eb99c5" />

### Security Tooling

* **Okta Verify** — MFA factor
* **EDR/MDM** — not integrated; posture expressed via **Okta Device Assurance**
* **Password Manager**
<img width="741" height="468" alt="image" src="https://github.com/user-attachments/assets/14f6f227-35ae-45cc-9076-6ddda291df97" />

## Why I built it this way (Zero-Trust alignment)

* **Least privilege:** group-based assignments, permission sets, and (optional) JIT patterns.
<img width="733" height="649" alt="image" src="https://github.com/user-attachments/assets/b304391a-0f9d-46c7-a320-890b2a2d11bb" />

* **Contextual access:** Adaptive MFA, Network Zones, and Device Assurance for high-tier apps.
* **Auditability:** Okta logs + Splunk dashboards/alerts + Terraform state/commit history.

## Repository Structure

* **01-Okta-Foundations** — UD, groups, policies, MFA, device assurance, self-service, branding
* **02-Application-Integrations** — Salesforce, Google Workspace (SSO), Zendesk, Slack, AWS IAM Identity Center
* **03-Automation-and-Policies** — Okta Workflows, Terraform (S3 + DynamoDB; Git CI/CD), policy tiering
* **04-Observability-and-Compliance** — Splunk Cloud (design + to-capture), evidence and reporting

### Reading order (recommended)

1. 01 Foundations
2. 02 App Integrations
3. 03 Automation & Policies
4. 04 Observability & Compliance

## Phases of Development

1. Planning & Design
2. Okta Core Setup
3. App Integrations (Salesforce, Zendesk, Google SSO, AWS IAM Identity Center)
4. Security & Guardrails (MFA, Adaptive, Zones, Device Assurance; App Tiering)
5. Automation (Workflows + Terraform)
6. Observability & Evidence (Splunk design)
7. Lessons Learned & Next Steps

## Documentation Purpose

* Step-by-step configurations and policies
* Technical settings and rationale (what I chose and why)
* Troubleshooting steps and constraints
* Screenshots placed **inline** inside each section for seamless reading

This serves as a portfolio piece to show practical IAM skills—configuration, integration, and automation.

---
