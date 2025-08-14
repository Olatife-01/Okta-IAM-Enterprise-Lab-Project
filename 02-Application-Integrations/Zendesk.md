# Zendesk (SAML SSO) Integration — Okta as IdP
## Purpose
To establish Single Sign-On (SSO) between Okta (as the Identity Provider) and Zendesk Support (as a Service Provider) using the SAML 2.0 protocol. This allows users to seamlessly access Zendesk from their Okta dashboard without needing separate Zendesk credentials, centralizing authentication and improving user experience.

## Technical Thought Process
* **SAML (Security Assertion Markup Language):** Chosen for its widely adopted standard for exchanging authentication and authorization data between an IdP (Okta) and an SP (Zendesk). It's robust for web-based SSO for applications that support it.
* **IdP-Initiated Flow:** For this lab, I am primarily testing an IdP-initiated flow where users start from their Okta dashboard and click the Zendesk application tile. Okta then sends a SAML assertion to Zendesk.
* **Trust Establishment:** The core of SAML integration is establishing trust by exchanging specific URLs (like the SSO URL and Entity ID) and a digital certificate for signing and validating assertions.
* **User Existence:** For SAML SSO to work, the user's primary email address (or username, depending on configuration) must typically exist in both Okta and the target application (Zendesk) and match. Automatic provisioning (SCIM) will be a later step to automate this user creation.
* **Targeted Assignment:** The use of the `Lab Users` group ensures that only specific, designated users can access Zendesk via this SSO integration, which is crucial for controlled testing and phased rollouts in real-world scenarios.

## Configuration Steps Performed

### A. Zendesk Support Trial Setup:
1.  Navigated to `zendesk.com/register/` and signed up for a free "Support Suite" trial.
2.  Created a unique Zendesk subdomain (e.g., `ryonhelp.zendesk.com`).
3.  Set an administrator password for the Zendesk instance.
4.  Logged into the new Zendesk Support environment.

### B. Configure Zendesk for SAML (Service Provider Side):
1.  In Zendesk, navigated to **Admin Center (gear icon) > Security and Authentications > SSO**.
2.  Clicked **"Add SSO configuration"** and selected **"SAML"**.
3.  **Copied Zendesk's Service Provider (SP) details for Okta configuration:**
    * **Assertion Consumer Service (ACS) URL / Post-back URL:** `https://ryonhelp.zendesk.com/access/saml` (Used this in Okta setup as "Single sign on URL" or "Assertion Consumer Service URL")
    * **Audience URI / SP Entity ID:** `ryonhelp.zendesk.com` (Used this in Okta setup as "Audience URI (SP Entity ID)")
4.  Kept the Zendesk SAML configuration page open to paste Okta's details later.
<img width="1101" height="911" alt="Screenshot 2025-07-08 200212" src="https://github.com/user-attachments/assets/05e0d177-b620-44e4-9408-1e28af26331d" />

### C. Add and Configure Zendesk Application in Okta (Identity Provider Side):
1.  Logged into the Okta Admin Console.
2.  Navigated to **"Applications" > "Applications"**.
3.  Clicked **"Browse App Catalog"**, searched for `Zendesk`, and selected "Zendesk."
4.  Clicked **"Add integration."**
5.  **General Settings:**
    * Application label: `Zendesk (Lab)`
    * **Subdomain:** Entered `ryonhelp` (The actual Zendesk subdomain).
<img width="1100" height="721" alt="Screenshot 2025-07-08 200832" src="https://github.com/user-attachments/assets/b4e908ee-de1f-4632-80e4-64105ab70703" />

    * Clicked **"Next"**.
6.  **Sign-On Options:**
    * Selected **"SAML 2.0"**.
    * Clicked **"Done"**.
<img width="1099" height="880" alt="Screenshot 2025-07-08 203352copy" src="https://github.com/user-attachments/assets/5fc7bd33-7de1-4fcf-8d2a-8fe561506d7e" />

7.  Accessed **"View Setup Instructions"** from the "Sign On" tab for the Zendesk (Lab) application in Okta.
8.  **Copied Okta's Identity Provider (IdP) details for Zendesk configuration:**
    * **Identity Provider Single Sign-On URL:** (e.g., `https://dev-xxxxxxx.okta.com/app/zendesk/xxxxxxxx/sso/saml`)
    * **Identity Provider Issuer (Entity ID):** (e.g., `http://www.okta.com/saml/sso/xxxxxxxx`)
    * Certificate fingerprint
### D. Complete SAML Configuration in Zendesk:
1.  Switched back to the open Zendesk SAML configuration page.
2.  Pasted the **Identity Provider Single Sign-On URL** from Okta into Zendesk's "SSO URL" field.
3.  Uploaded the downloaded **X.509 Certificate** file from Okta into Zendesk's "Certificate" section.
4.  Checked **"Enable SAML SSO"**.
5.  Clicked **"Save"**.
<img width="1088" height="903" alt="Screenshot 2025-07-08 202044" src="https://github.com/user-attachments/assets/ac2aceb1-aa79-4322-9ea4-7a6a6e5aeb53" />

### E. Assign "Lab Users" Group to Zendesk in Okta:
1.  Navigated back to the Zendesk (Lab) application in Okta.
2.  Clicked on the **"Assignments"** tab.
3.  Clicked **"Assign" > "Assign to Groups"**.
4.  Selected the **`Lab Users`** group.
5.  Clicked **"Assign"** then **"Save and Go Back"** and **"Done"**.

## Testing and Validation

1.  **Zendesk User Preparation:** Manually created a user in Zendesk (Admin Center > Manage > People > Add user) with the same primary email address as `test.user` from the `Lab Users` group in Okta (e.g., joshua.dominguez126@mellonryon.com). This ensures a matching user exists in both directories for the initial SSO test.
2.  **IdP-Initiated SSO Test:**
    * Opened a new Incognito browser window.
    * Navigated to the Okta End-User Dashboard .
    * Logged in as Joshua (member of `Lab Users` group) with Okta Verify MFA.
<img width="715" height="484" alt="Screenshot 2025-07-08 203104" src="https://github.com/user-attachments/assets/a9eb0e3c-6420-49fc-9c78-b0ab4c46431d" />

    * Clicked on the **"Zendesk (Lab)"** application tile.
    * **Result:** Successfully redirected and logged into Zendesk Support as joshua.****.com without re-entering credentials. This confirms successful SAML SSO configuration.
      
<img width="715" height="601" alt="Screenshot 2025-07-08 203140" src="https://github.com/user-attachments/assets/9640f43c-7c67-4908-8510-7acf276f5ff1" />
<img width="1011" height="297" alt="Screenshot 2025-07-08 203518" src="https://github.com/user-attachments/assets/4e587da2-528b-465a-8435-7b4da769d16d" />

## Challenges & Solutions (Optional - for your real experience)
* The Zendesk SAML flow looked a bit different from what i did in the past, it is more simplified now, just had to follow the Okta SAML configuration doc.
---
