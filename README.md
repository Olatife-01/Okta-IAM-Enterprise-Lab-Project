Here’s your text, cleaned up and formatted as Markdown for your **root `README.md`**:

---

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

## Components

### Identity Sources

* **BambooHR (SCIM)** — HR-as-master design
* **Active Directory** — Okta AD Agent, bi-directional directory sync

### Identity Hub (Okta)

* **Okta** — Universal Directory, Groups/Rules, Policies (MFA, Adaptive, Zones), Device Assurance, End-User Self-Service, App Integrations.
* \**Okta Identity Governance / Okta Privileged Access*

### Downstream Applications

* **Salesforce** — SAML SSO + SCIM
* **Google Workspace** — SSO only; provisioning blocked by org policy
* **Zendesk** — SAML SSO *(implemented)*
* **Slack** — SSO (SCIM optional; not enabled in this lab)

### Cloud Access

* **AWS IAM Identity Center** — SSO + SCIM, permission sets, group assignments

### Automation

* **Okta Workflows** — JML patterns; Lambda-triggered S3 folder creation; daily de-provision audit email
* **Terraform (IaC)** — Okta & AWS resources; **S3 + DynamoDB** backend; Git CI/CD

### Observability / SIEM

* **Splunk Cloud** — Ingestion of Okta System Logs, dashboards, and email alerts 

### Security Tooling

* **Okta Verify** — MFA factor
* **EDR/MDM** — not integrated; posture expressed via **Okta Device Assurance**
* **Password Manager**

## Why I built it this way (Zero-Trust alignment)

* **Least privilege:** group-based assignments, permission sets, and (optional) JIT patterns.
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
