# Google Workspace (SAML SSO) Integration (Custom Application)

## Purpose
To establish Single Sign-On (SSO) between Okta (as the Identity Provider) and Google Workspace (as a Service Provider) using a **custom SAML 2.0 application** in Okta. This enables users to access Google services seamlessly via their Okta login, enhancing security and user convenience. This custom approach was taken due to issues encountered with the pre-built Google Workspace application connector in Okta's App Catalog and further challenges with Google Cloud Platform policies.

## Technical Thought Process
* **SAML Trust Relationship:** This integration relies on SAML 2.0 to establish a trusted connection. Okta sends a signed assertion to Google Workspace, which validates it and logs the user in.
* **Custom SAML Application Justification:** The decision to use a custom SAML application was primarily driven by difficulties encountered in getting the pre-built Google Workspace application from the Okta App Catalog to function correctly. This provided a workaround to achieve SSO, but also highlighted further complexities related to automated provisioning.
* **Manual SAML Configuration:** Unlike pre-built apps where many parameters are automatically populated, a custom SAML app requires manually gathering and inputting Service Provider (Google Workspace) details (like ACS URL and Entity ID) into Okta, and then taking Okta's IdP details and inputting them into Google.
* **User Matching:** For successful SSO, the user's primary email address must typically exist in both Okta and the target application (Google Workspace) and match.
* **Targeted Assignment:** The `Lab Users` group is specifically assigned this application to manage and test access for a controlled set of users, aligning with lab best practices.

## Challenges Faced

### Issue 1: Pre-built Google Workspace App Connector Failure
During initial attempts to integrate Google Workspace using the pre-built application from the Okta App Catalog, persistent issues were encountered that prevented successful SSO. The exact root cause (e.g., domain verification issues, specific Okta tenant behavior) was not immediately apparent, leading to a decision to pivot.

### Issue 2: Google Cloud Platform (GCP) Policy Blocking Key Creation
When attempting to configure user provisioning for Google Workspace, a Google Cloud Platform organization policy, `iam.managed.disableServiceAccountKeyCreation`, blocked the creation of the necessary P12 service account key. This policy is a security control often enforced by organizations to prevent the use of long-lived service account keys, which are typically required by Okta's pre-built Google Workspace provisioning connector.

### Resolution (Workaround for SSO)
To proceed with the lab objectives and demonstrate SAML SSO, a **Custom SAML Application** was configured in Okta. This allowed for manual input of SAML parameters, bypassing the potentially problematic pre-configured aspects of the built-in connector. This successfully validated the core SSO functionality. The GCP policy issue specifically impacts provisioning, which is not supported by this custom SAML app.

## Configuration Steps Performed

### A. Google Workspace Admin Console Access:
1.  Ensured administrator access to a Google Workspace domain.
2.  Logged into the Google Admin Console (`admin.google.com`).

### B. Configure Google Workspace for SAML (Service Provider Side):
1.  In Google Admin Console, navigated to **"Security" > "Authentication" > "SSO with third-party IdP"**.
2.  Checked **"Set up SSO with a third-party identity provider."**
<img width="1899" height="946" alt="Screenshot 2025-07-08 204839" src="https://github.com/user-attachments/assets/6ad32c37-5bfa-4e7f-8172-52016d9a731a" />

3.  **Identified and noted Google Workspace's Service Provider (SP) details for Okta configuration:**
    * **ACS URL / Redirect URL:** `https://www.google.com/a/yourdomain.com/acs` (Replace `yourdomain.com` with your actual Google Workspace domain)
    * **Entity ID (Audience URI):** `google.com/a/yourdomain.com` (Replace `yourdomain.com` with the actual Google Workspace domain)
    * *These specific URLs were crucial for manually configuring the custom SAML app in Okta.*
4.  Kept the Google Admin Console SSO configuration page open to paste Okta's details later.

### C. Add and Configure Google Workspace as a Custom SAML Application in Okta (Identity Provider Side):
1.  Logged into the Okta Admin Console.
2.  Navigated to **"Applications" > "Applications"**.
3.  Clicked **"Create App Integration"**.
4.  Selected **"SAML 2.0"** as the Sign-on method.
5.  Clicked **"Next."**
6.  **General Settings:**
    * **App name:** `Google Workspace (Lab - Custom SAML)`
    * **App logo:** (Optional, uploaded a Google Workspace logo for recognition).
<img width="1059" height="941" alt="Screenshot 2025-07-08 205409" src="https://github.com/user-attachments/assets/aa7a0693-f71e-4699-b9b8-5465ae77dd74" />

    * Clicked **"Next."**
7.  **Configure SAML (Crucial Step for Custom App):**
    * **Single sign on URL (ACS URL):** Entered Google's **ACS URL** obtained from step B.3 (e.g., `https://www.google.com/a/yourdomain.com/acs`).
    * **Audience URI (SP Entity ID):** Entered Google's **Entity ID** obtained from step B.3 (e.g., `google.com/a/yourdomain.com`).
<img width="1915" height="536" alt="image" src="https://github.com/user-attachments/assets/651e23bd-4b48-45b7-846d-9acbab24163e" />

    * **Default Relay State:** Left blank.
    * **Name ID format:** Selected **"EmailAddress"**. (Google typically expects the user's email as the Name ID).
    * **Application username:** Selected **"Okta username"**.
    * **Attribute Statements (Optional but Recommended):** (Added if needed by Google, e.g., for mapping other user attributes beyond Name ID. For basic SSO, often not strictly required initially beyond Name ID).
        * `Name: email`, `Name format: Unspecified`, `Value: user.email`
    * Clicked **"Next."**
8.  **Feedback (for Okta):**
    * Selected "I'm an Okta customer adding an internal app."
    * Selected "This is an internal app that i have created."
    * Clicked **"Finish."**
9.  **Get Okta's SAML Metadata for Google Workspace (from the Custom App):**
    *  Now on the "Sign On" tab of the new custom "Google Workspace (Lab - Custom SAML)" application.
    * Under the "SAML 2.0" section, click **"View SAML setup instructions"** (or similar, it might be called "How to Configure SAML 2.0 for this Application").
    * **Copied Okta's Identity Provider (IdP) details for Google Workspace configuration:**
        * **Identity Provider Single Sign-On URL:** (e.g., `https://dev-xxxxxxx.okta.com/app/sso/exkxxxxxxxx/sso/saml`)
        * **Identity Provider Issuer:** (e.g., `http://www.okta.com/exkxxxxxxxx`)
        * **X.509 Certificate:** Click the **"Download certificate"** link.

### D. Complete SAML Configuration in Google Workspace:
1.  Switched back to the open Google Admin Console SSO configuration page.
2.  Pasted the **Identity Provider Single Sign-On URL** from Okta into Google's "Sign-in page URL" field.
3.  Pasted the **Identity Provider Issuer** from Okta into Google's "Entity ID" field (sometimes called "IdP Issuer ID").
4.  Uploaded the downloaded **X.509 Certificate** file from Okta into Google's "Verification certificate" section.
<img width="1915" height="903" alt="Screenshot 2025-07-08 211757" src="https://github.com/user-attachments/assets/a9624413-8fb5-4e35-b1a6-5141bd79e5b9" />

5.  Clicked **"SAVE"**.

### E. Assign "Lab Users" Group to Google Workspace in Okta:
1.  Navigated back to the custom "Google Workspace (Lab - Custom SAML)" application in Okta.
2.  Clicked on the **"Assignments"** tab.
3.  Clicked **"Assign" > "Assign to Groups"**.
4.  Selected the **`Lab Users`** group.
5.  Confirmed the primary email for the assigned user(s) matches their email in Google Workspace.
6.  Clicked **"Save and Go Back"** then **"Done"**.

## Testing and Validation

1.  **Google Workspace User Preparation:** Ensured that at least one user from the `Lab Users` group in Okta also exists in the Google Workspace domain with the exact same primary email address (e.g., `test.user@yourdomain.com`).
2.  **IdP-Initiated SSO Test:**
    * Opened a new Incognito/Private browser window.
    * Navigated to the Okta End-User Dashboard (`your-okta-org-url.okta.com/enduser/dashboard`).
    * Logged in as `test.user` (member of `Lab Users` group) with Okta Verify MFA.
<img width="1101" height="655" alt="Screenshot 2025-07-08 211815" src="https://github.com/user-attachments/assets/7409f274-bb7a-4478-845b-176982bdefa2" />

    * Clicked on the **"Google Workspace (Lab - Custom SAML)"** application tile.
    * **Result:** Successfully redirected and logged into Google Workspace (e.g., Gmail, Drive) as `test.user@yourdomain.com` without re-entering credentials. This confirms successful custom SAML SSO configuration.
<img width="445" height="489" alt="Screenshot 2025-07-08 215254" src="https://github.com/user-attachments/assets/e94a3fa2-8e36-47c3-8183-96a50db080cb" />

<img width="1109" height="906" alt="Screenshot 2025-07-08 215403" src="https://github.com/user-attachments/assets/e8d52f37-64f0-404f-868e-cf2e7eb11fb4" />


---

**Current Limitation:** 
The current custom SAML integration provides Single Sign-On only. It does **not** automatically provision (create, update, or deactivate) users in Google Workspace from Okta's Universal Directory. This functionality is typically part of the pre-built "Google Workspace" application connector in Okta's App Catalog, which leverages Google's Admin SDK APIs (SCIM-like behavior).
* **Challenges Encountered:** Attempts to configure provisioning using the pre-built connector were blocked by a Google Cloud Platform organization policy (`iam.managed.disableServiceAccountKeyCreation`) preventing service account key creation.
* 
**Possible future actions (when environment allows):**
* Automated provisioning is a critical component of a robust IAM architecture. This will be revisited at a later stage, potentially by:
    * Further troubleshooting the pre-built Okta Google Workspace application if possible in a different environment.
    * Exploring alternative strategies for user lifecycle management with Google Workspace, or focusing provisioning efforts on other applications not impacted by this specific GCP policy.

---
