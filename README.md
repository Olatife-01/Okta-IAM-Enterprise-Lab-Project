# Okta-IAM-Enterprise-Lab-Project-
Enterprise Identity and Access Management (IAM) Lab Projects
Project Overview
This repository serves as a portfolio of a hands-on lab project focused on designing, building, and documenting a modern, zero-trust-aligned Identity and Access Management (IAM) architecture. The project demonstrates practical experience with a variety of cloud and on-premises technologies, including Okta as the central identity provider, automation via Terraform and Okta Workflows, and observability with Splunk Cloud.

The goal of this lab was to demonstrate/create a functional and secure identity platform that enforces strong authentication policies, automates user lifecycle management, and provides a clear audit trail for compliance.

## Repository structure
- [01-Okta-Foundations](./01-Okta-Foundations) — UD, groups, policies, MFA, device assurance, self-service, branding
- [02-Application-Integrations](./02-Application-Integrations) — Salesforce, Google Workspace (SSO), Zendesk, Slack, AWS IAM Identity Center
- [03-Automation-and-Policies](./03-Automation-and-Policies) — Okta Workflows, Terraform (S3 + DynamoDB; Git CI/CD), security policies & app tiering
- [04-Observability-and-Compliance](./04-Observability-and-Compliance) — Splunk Cloud (design + to-capture), evidence and reporting


High-Level Architecture Diagram
This diagram visualizes the final architecture of the lab environment, including all key integrations and data flows.

<br>

<p align="center">
<img src="https://mermaid.ink/img/pako:eNqNlctuozAQhV9lzJg1L6S0GzZg3V8Q3VpE_Cg8iC4Vv1QJt1yO3k9Y4m7Vqlb0YGaGGT_v3DkYQyN4Yw4pQhNIsfE81D4Qc3sC2N4B0s2Y-88-uS-OQ87f-JzT-1N02iW-0v0i6-nF_7d0-8f64M_eX1J2jUuV07b1O-b0_j_G8v9dYvj-C11wH8lT0p50eL8-j4_gXmE-9QcWn0d52tPz8N9W-6Wq53w_T_4h2yQ8p08d0rD-w_sP4M4uJ8_h7p3vT-vA_-71_W938d9-2r7d1t0e3l9-0zD_uO7B-oO09Xl--b83m-o7j03X21T8M_qgY_0P7D-jS-L60aGk3fF94Xh3T5Hn4_gA9V1n19Fm3d6B8bU83S3eO-L2d-j9-YF4f9lX521f7l043y5_b3dO6bT091c53d_h-b65X13OQ5iG8wz4fX0-V_c_72R3gJ10-h_a_wT3x9e_O7f3LhD4l_o-4_d1g1n8oB3mQ9q-T9-XQp2u9-X_hJ-5H534d0bYVvD0L_b11oVvD1n3z9p7zS-X4d_156w_35z6uJ8W93b7w_6765P9P9O96-Q_P2h9z3-Y0399j7R_t_hPj3l-c71r610R6r-30Wp6P63013d3B9Hk4_f1kE_e_gP1tA_i6oN8g" alt="Mermaid chart showing the IAM lab architecture diagram">
</p>
