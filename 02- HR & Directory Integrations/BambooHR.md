# BambooHR (One-Way SCIM Provisioning & SAML SSO) Integration

## Purpose

Establish a comprehensive identity integration with BambooHR serving two primary functions:

1. **SCIM Provisioning (BambooHR → Okta)**: Automate user lifecycle from BambooHR (authoritative HR system) into Okta’s Universal Directory. New hires are created in Okta, attributes updated, and users deactivated on termination—improving data accuracy and reducing manual effort. *(Okta’s BambooHR app uses the BambooHR API for inbound profile sourcing—functionally SCIM-like.)*

2. **SAML SSO (Okta → BambooHR)**: Enable Single Sign-On from Okta for designated users (e.g., HR admins and BambooHR-sourced employees), improving user experience and security.

## Technical Thought Process & Evolution of Configuration
BambooHR is the system of record for workforce data; in an enterprise, reliable Joiner-Mover-Leaver depends on HR mastering identities, not an IT admin clicking in a console. That’s why I positioned BambooHR as **Profile Master** and used Okta to **consume** authoritative profiles via the BambooHR API (SCIM-style), while using **SAML** for access—one app instance handling inbound profile sourcing and outbound SSO. I anchored identity matching on email, set “use existing Okta user” to avoid duplication, and mapped a minimal, durable attribute set (first/last name, work email, employee number) to keep updates deterministic. To prevent drift, I explicitly **disabled “To App” provisioning** so Okta never pushes into HR, and I restricted SSO assignment to users that already exist in BambooHR (plus HR admins). I validated the JML lifecycle by creating, updating, and deactivating a test employee in BambooHR and observing those changes propagate into Okta on import. Early errors (“matching user not found”) exposed directionality mistakes and led to the inbound-only correction. I staged rollout through a lab group, enforced MFA in Okta, and wired Splunk searches to evidence provisioning and SSO events for audit trails. The result is idempotent and replayable across tenants: HR owns the truth, Okta brokers access, SAML delivers the session, and logs prove the controls. This pattern integrates cleanly with the broader lab (Vault, AWS, CI/CD) and sets the foundation for Workflows-driven onboarding and downstream app provisioning.
* ** Separation of Duties & One-Way Mastering: ** BambooHR is the authoritative source for people data; Okta consumes it and drives downstream access. To preserve separation of duties and clear data lineage, we intentionally disable “To App” (Okta → BambooHR) provisioning. This prevents the IAM platform from modifying HR records, enforces least-privilege on API scopes back into HR, and ensures auditability (HR owns facts; IAM translates those facts into entitlements).
* **SCIM (System for Cross-domain Identity Management):** SCIM is the standard protocol utilized for automating the inbound (To Okta) user provisioning and deprovisioning lifecycle. Okta acts as a SCIM client, periodically polling BambooHR's API for changes.
* **SAML 2.0 (Security Assertion Markup Language):** SAML 2.0 facilitates the outbound (From Okta) Single Sign-On process. Okta acts as the Identity Provider (IdP), sending cryptographically signed assertions to BambooHR (the Service Provider - SP) to authenticate users without requiring them to re-enter credentials.
* **Dual Integration:** The same Okta application instance for BambooHR serves both the inbound SCIM provisioning and the outbound SAML SSO, demonstrating a complete identity management lifecycle for the application's users.
* **Profile Sourcing Priority:** Okta's Profile Sourcing feature ensures that BambooHR maintains authoritative control over user profiles, making them read-only in Okta to prevent conflicts and maintain data integrity.

## Configuration Steps Performed

### A. BambooHR Free Trial Setup:
1.  Navigated to `www.bamboohr.com/free-trial/` and signed up for a free trial.
2.  Activated the account via email and completed initial company setup.
3.  Logged into the new BambooHR instance.
<img width="1023" height="797" alt="Screenshot 2025-07-09 184435" src="https://github.com/user-attachments/assets/32a4e6c2-a930-403d-af31-eddc26a7b2f4" />

### B. Prepare BambooHR for Integration (API Key & SAML SP Details):
1.  **Generate API Key (for SCIM):**
    * In BambooHR, clicked on the **user profile icon/menu** (top/bottom right).
    * Selected **"API Keys"** (or "My Device & API Keys").
<img width="1069" height="820" alt="Screenshot 2025-07-09 184515" src="https://github.com/user-attachments/assets/2eb38b31-eef3-4b4a-9dee-dc12aad3fb5b" />

    * Clicked **"+ Add New Key"**, provided a description (`Okta SCIM Integration`).
<img width="1049" height="765" alt="Screenshot 2025-07-09 184755" src="https://github.com/user-attachments/assets/684961af-7978-4e13-aaff-454f12c1a46d" />

    * Generated and **securely copied this API Key**.
2.  **Note BambooHR Subdomain:** Noted the BambooHR Subdomain from the instance URL (e.g., `yoursubdomain.bamboohr.com`).
3.  **Get SAML Service Provider (SP) Details (for SSO):**
    * In BambooHR, navigated to **Settings (gear icon) > Apps > SAML Single Sign-On**.
    * Identified and noted BambooHR's SP details needed for Okta:
        * **ACS URL (Assertion Consumer Service URL) / Single Sign-On URL**
        * **Entity ID / Audience URI**
    * Kept this BambooHR SSO page open.

### C. Add and Configure BambooHR Application in Okta (SAML & SCIM):
1.  Logged into the Okta Admin Console.
2.  Navigated to **"Applications" > "Applications"**.
3.  Clicked **"Browse App Catalog"**, searched for `BambooHR`, and selected it.
4.  Clicked **"Add integration."**
5.  **General Settings (Step 1 of 3):**
    * **Application label:** `BambooHR (HR Source & Admin SSO)`
    * Clicked **"Next."**
6.  **Configure Sign-On Options (Step 2 of 3):**
    * **Sign on methods:** Selected **"SAML 2.0"**.
    * Clicked **"Done."**

### D. Configure SAML SSO from Okta to BambooHR:
1.  In Okta, on the **"Sign On"** tab for the `BambooHR (HR Source & Admin SSO)` application.
2.  Clicked **"Edit"** in the "SAML 2.0" section.
3.  **SAML 2.0 Configuration:**
    * **Single sign on URL (ACS URL):** Pasted the **ACS URL** obtained from BambooHR (step B.3).
    * **Audience URI (SP Entity ID):** Pasted the **Entity ID** obtained from BambooHR (step B.3).
    * **Name ID format:** Selected **"EmailAddress"**.
    * **Application username:** Selected **"Okta username"**.
    * **Attribute Statements:** Added:
        * **Name:** `Email`
        * **Name format:** `Unspecified`
        * **Value:** `user.email`
    * Clicked **"Save."**
<img width="715" height="716" alt="Screenshot 2025-07-09 185801" src="https://github.com/user-attachments/assets/3f95b31f-f2ee-4426-a212-cd6ee5cefa9f" />

4.  **Get Okta's SAML Identity Provider (IdP) Details:**
    * Still on the "Sign On" tab, clicked **"View SAML setup instructions."**
    * Copied **Identity Provider Single Sign-On URL**, **Identity Provider Issuer**, and **downloaded the X.509 Certificate**.
5.  **Complete SAML Configuration in BambooHR:**
    * Switched back to the BambooHR SSO configuration page (from step B.3).
    * Pasted **Okta's SSO Login URL** into BambooHR's "SSO Login URL" field.
    * Pasted **Okta's IdP Entity ID** into BambooHR's "IdP Entity ID" or "Issuer" field.
    * Uploaded the **X.509 Certificate** downloaded from Okta.
    * Ensured "Enable SSO" or similar was checked in BambooHR and **saved changes.**
<img width="697" height="729" alt="Screenshot 2025-07-09 191001" src="https://github.com/user-attachments/assets/f45433b1-2c7c-441c-a5fa-646e5383f946" />

### E. Configure "To Okta" SCIM Provisioning:
1.  On the **"Provisioning"** tab for the BambooHR application in Okta, clicked **"Integration"** on the left.
2.  Clicked **"Configure API Integration."**
<img width="841" height="372" alt="Screenshot 2025-07-09 191405" src="https://github.com/user-attachments/assets/6160603d-e3e9-4f2c-b17a-927fe5ad8c57" />

3.  Checked **"Enable API Integration."**
4.  **API Token:** Pasted the BambooHR API Key (from step B.1).
5.  **Subdomain:** Pasted the BambooHR subdomain (from step B.2).
6.  Clicked **"Test API Credentials"** (verified success), then **"Save."**
<img width="914" height="628" alt="Screenshot 2025-07-09 191540" src="https://github.com/user-attachments/assets/f0a2dbfd-1966-4ba9-9eb0-b81eba28a03c" />

7.  On the **"Provisioning"** tab, clicked **"To Okta"** on the left.
8.  Clicked **"Edit"**.
9.  **Provisioning Features:**
    * **[x] Create Users**
    * **[x] Activate Users**
    * **[x] Update User Attributes**
    * **[x] Deactivate Users**
10. **Matching People:**
    * **Match users by:** `Email`
    * **If a match is found:** `Use existing Okta user`
11. **Profile & Attribute Mapping:**
    * Click **"Go to Profile Editor."**
    * Mapped essential attributes: `firstName` -> `firstName`, `lastName` -> `lastName`, `workEmail` -> `email`, `employeeNumber` -> `employeeNumber` (or `externalId`). Ensured "Apply on create and update."
    * Clicked **"Save Mappings."**
12. **Profile & Lifecycle Sourcing:**
    * **[x] Allow BambooHR to source Okta users** (This makes BambooHR the Profile Master).
13. **User Deactivation/Reactivation:**
    * **When a user is deactivated in the app:** Selected **"Deactivate"**.
    * **When a user is reactivated in the app:** Selected **"Reactivate deactivated Okta users"**.
14. Clicked **"Save"** on the "To Okta" page.
<img width="825" height="823" alt="Screenshot 2025-07-09 192706" src="https://github.com/user-attachments/assets/29a30520-85f2-4a35-9345-5fb676dfc685" />

### F. Configure "To App" Provisioning (from Okta to BambooHR - Disabled):
**Objective:** enforce least-privilege, preserve HR→IAM data lineage, and produce auditable evidence.

* **SSO-only for BambooHR admins:** Require SAML SSO via Okta (with MFA) for all BambooHR admin roles. Maintain exactly **one** break-glass local admin, vaulted, rotated, and tested quarterly.
* **Limit app assignment:** Assign the BambooHR SAML app **only** to users sourced from BambooHR (profile master) and explicitly approved BambooHR admins. Drive access via Okta groups filtered to BambooHR-sourced identities; avoid ad-hoc individual assignments.
* **One-way mastering (SoD):** Keep **“To Okta” enabled** and **“To App” disabled**. HR owns people data; IAM translates attributes into entitlements. This prevents write-back to HR and cleanly separates duties.
* **Minimal attribute mapping:** Send only attributes BambooHR/SSO strictly requires (email, name). Avoid unnecessary PII in SAML assertions.
* **API key hygiene:** Store the BambooHR API key in a secret store (e.g., GitHub Actions Secrets / Vault), never in code; rotate on a defined schedule and on admin turnover.
* **Monitoring & alerts (Okta → Splunk):**

  * Ingestion health: alert on SCIM import failures and large deltas.
  * Access hygiene: alert on BambooHR app assignments outside the BambooHR-sourced group.
  * Auth signals: alert on repeated SSO failures and non-standard MFA outcomes for BambooHR admins.

1.  On the **"Provisioning"** tab, clicked **"To App"** on the left.
2.  Confirmed that options for pushing user creation/updates to BambooHR (like "Create Users" or "Update User Attributes") were **NOT enabled/checked**. If "Update User Attributes" was visible, it was explicitly **left disabled** to prevent conflicts with BambooHR being the Profile Master and avoid unwanted profile updates.
3.  This confirmed that Okta would not attempt to push general user profiles to BambooHR, preventing "Matching user not found" errors for Okta-mastered users not originating from BambooHR.

### G. Assign Users/Groups & Test

1.  **Assign the Application for SAML SSO:**
    * In Okta, for the `BambooHR (HR Source & Admin SSO)` app, clicked the **"Assignments"** tab.
    * Clicked **"Assign" > "Assign to People"** (or Groups).
    * **Crucially, assigned users who exist in *both* Okta and BambooHR.** This includes:
        * Your **administrator account** (if it exists in BambooHR for admin SSO).
        * The **test user (e.g., "Jeremy Smith") that was successfully imported from BambooHR to Okta** (ensuring they exist in both systems for SSO testing).
    * Clicked **"Save and Go Back"** then **"Done"**.
<img width="974" height="560" alt="Screenshot 2025-07-09 200350" src="https://github.com/user-attachments/assets/371ac4a3-270c-413f-9138-6b1dc9b7eec0" />

2.  **Test User Ingestion (SCIM Provisioning) from BambooHR (BambooHR to Okta):**
    * **Created a new employee in BambooHR** (e.g., `Jeremy Smith`) to ensure they were unique.
    * In Okta, for the BambooHR app, navigated to **"Provisioning" > "Import"** and clicked **"Import Now."**
    * Selected **"Confirm Assignments"** and chose to **"Create New User"** for `Jeremy Smith`.
    * **Verification:** Confirmed `Jeremy Smith` was successfully created as an active user in Okta's Universal Directory (`Directory > People`) with correct attributes.
    * **Attribute Update & Deactivation Test:** Modified `Jeremy Smith`'s job title in BambooHR, ran import, and verified the update in Okta. Deactivated `Jeremy Smith` in BambooHR, ran import, and verified deactivation in Okta.
<img width="896" height="752" alt="Screenshot 2025-07-09 194720" src="https://github.com/user-attachments/assets/a6e9deb4-6683-4536-8edf-6bca711c7122" />
<img width="844" height="852" alt="Screenshot 2025-07-09 194813" src="https://github.com/user-attachments/assets/e46eb8c4-4ced-47f6-9f74-956fecd53a26" />
<img width="962" height="810" alt="Screenshot 2025-07-09 195624" src="https://github.com/user-attachments/assets/ec7d3256-d9c4-42d1-9359-c5404c303088" />

3.  **Test SAML SSO (Okta to BambooHR for Admins/Sourced Users):**
    * Activated `Jeremy Smith`'s account in Okta and enrolled Okta Verify.
    * Opened a new Incognito/Private browser window.
    * Logged in to the Okta End-User Dashboard as `Jeremy Smith`.
    * Clicked on the **"BambooHR (HR Source & Admin SSO)"** application tile.
    * **Verification:** Confirmed seamless and successful login into BambooHR.
<img width="1080" height="377" alt="Screenshot 2025-07-09 203825" src="https://github.com/user-attachments/assets/2137a758-473c-4271-9872-9be3da893de9" />
<img width="997" height="209" alt="Screenshot 2025-07-09 203935" src="https://github.com/user-attachments/assets/dec68f2e-5aad-4ff4-9c07-b9d804ebd41f" />
<img width="1078" height="462" alt="Screenshot 2025-07-09 203856" src="https://github.com/user-attachments/assets/e2a37fc1-5cff-48f3-ac65-d40a7ed85b9a" />

## Challenges Faced & Lessons Learned

### 1: Locating BambooHR API Key
* **Issue:** The API Key (required for SCIM provisioning) was not found under the expected "Settings > API Keys" or "Settings > API Management" sections as per some common documentation.
* **Resolution:** The API Key generation option was located under the **user's profile icon/menu** (e.g., in the top/bottom right corner) labeled as "My API Keys" or similar, in the current BambooHR UI for trial accounts.
* **Lesson:** User interface paths can change or differ based on account types (trial vs. paid, recent updates). Always check common alternative locations like user profile menus for API credentials.

### 2: Locating BambooHR SAML SSO Settings
* **Issue:** The Single Sign-On (SSO) configuration in BambooHR was not found under "Settings > Integrations > Single Sign-On."
* **Resolution:** The SAML SSO setup in the current BambooHR UI is found under **Settings (gear icon) > Apps > SAML Single Sign-On**.
* **Lesson:** Similar to API keys, specific integration settings in SaaS applications can be moved. "Apps" or "Integrations" sections under main settings are common places to find such configurations.

### 3: "Automatic Provisioning to App Failed: Matching User Not Found" Errors
* **Issue:** Encountered errors (e.g., for "Joshua Dominguez") when attempting to assign Okta-mastered users (who did not originate from BambooHR) to the BambooHR application in Okta. The error indicated Okta was trying to provision/match the user *to* BambooHR, but BambooHR wasn't the intended target for user creation from Okta, and the user didn't exist there. Okta's "To App" provisioning options were not fully visible/configurable to disable "Create Users."
* **Compromise/Fix:**
    * Under **"Provisioning" > "To App"** for the BambooHR application in Okta, confirmed that **"Update User Attributes" (and implicitly "Create Users" if visible)** was **NOT enabled**. This reinforces BambooHR as the Profile Master and prevents Okta from attempting to push user creations/updates *to* BambooHR.
<img width="736" height="840" alt="Screenshot 2025-07-09 193702" src="https://github.com/user-attachments/assets/c840a5e0-63c8-4504-90bd-dc8f34522f22" />

    * **Crucial Lesson:** For an HR system acting as a "source of truth," you typically **do not enable "To App" provisioning (from Okta to HR)** for general users. Assigning users to the Okta application for SSO should primarily be done for users who **already exist and are managed within the HR system** (e.g., employees imported from BambooHR, or HR Admins whose accounts manually exist in BambooHR).
    * **Lesson:** Understanding the **directionality of provisioning ("To Okta" vs. "To App")** and the concept of a **"Profile Master"** is fundamental. Errors often arise from attempting to push identities against the defined mastering flow.
    * **Governance rationale:** Beyond resolving the error, keeping BambooHR → Okta one-way aligns with SoD: HR maintains identity attributes, while IAM governs access. Disabling “To App” eliminates the risk of Okta overwriting HR data and provides clean accountability for auditors.

---
