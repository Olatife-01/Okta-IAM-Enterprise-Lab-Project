# Zendesk (SAML SSO) — Okta as IdP

## Purpose

Enable **Single Sign-On (SSO)** to **Zendesk** using **Okta** as the **SAML 2.0 Identity Provider**. This lets my Okta users access Zendesk with their Okta credentials, applying Okta MFA/policies and improving user experience.

---

---

## Troubleshooting & Lessons Learned

* **Subdomain mismatch:** ACS/Audience must use your exact **Zendesk subdomain**.
* **Clock skew / cert issues:** If you see “invalid signature” or “audience” errors, re-download the **Okta cert** and verify time sync.
* **User not found:** Ensure the **email** (NameID) in Okta **exists** in Zendesk.
* **Lockout risk:** Don’t “require SSO for all” until you’ve confirmed at least one **bypass admin** and validated both directions.
* **SLO not required:** Single Logout is optional; test carefully if you enable it.




# Zendesk (SAML SSO) Integration

## Purpose
To establish Single Sign-On (SSO) between Okta (as the Identity Provider) and Zendesk Support (as a Service Provider) using the SAML 2.0 protocol. This allows users to seamlessly access Zendesk from their Okta dashboard without needing separate Zendesk credentials, centralizing authentication and improving user experience.

## Technical Thought Process
* **SAML (Security Assertion Markup Language):** Chosen for its widely adopted standard for exchanging authentication and authorization data between an IdP (Okta) and an SP (Zendesk). It's robust for web-based SSO for applications that support it.
* **IdP-Initiated Flow:** For this lab, we're primarily testing an IdP-initiated flow where users start from their Okta dashboard and click the Zendesk application tile. Okta then sends a SAML assertion to Zendesk.
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

### C. Add and Configure Zendesk Application in Okta (Identity Provider Side):
1.  Logged into the Okta Admin Console.
2.  Navigated to **"Applications" > "Applications"**.
3.  Clicked **"Browse App Catalog"**, searched for `Zendesk`, and selected "Zendesk."
4.  Clicked **"Add integration."**
5.  **General Settings:**
    * Application label: `Zendesk (Lab)`
    * **Subdomain:** Entered `ryonhelp` (your actual Zendesk subdomain).
    * Clicked **"Next"**.
6.  **Sign-On Options:**
    * Selected **"SAML 2.0"**.
    * Clicked **"Done"**.
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
    * Clicked on the **"Zendesk (Lab)"** application tile.
    * **Result:** Successfully redirected and logged into Zendesk Support as joshua.dominguez126@mellonryon.com without re-entering credentials. This confirms successful SAML SSO configuration.

## Challenges & Solutions (Optional - for your real experience)
* The Zendesk SAML flow looked a bit different from what i did in the past, it is more simplified now, just had to follow the Okta SAML configuration doc.
---
