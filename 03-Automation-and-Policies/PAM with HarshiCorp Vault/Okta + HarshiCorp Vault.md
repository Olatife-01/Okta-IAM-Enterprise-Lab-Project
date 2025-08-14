# Privileged Access Management (PAM) — HashiCorp Vault with Okta (Okta Auth Method)

> **Scope:**. I integrated **HashiCorp Vault** with **Okta** using Vault’s **Okta Auth Method** (direct Okta Authentication API), after an initial OIDC attempt failed to surface in the Vault UI. The goal is to centralize privileged authentication and lay the groundwork for JIT and dynamic secrets. 

## I. Introduction & Purpose

This document details the integration of **HashiCorp Vault** with **Okta** to establish a robust Privileged Access Management (PAM) solution within our Enterprise IAM Lab. This specific integration ultimately leveraged Vault's **Okta Auth Method**, which directly uses Okta's Authentication API. The primary goal is to centralize privileged identity authentication and secrets management, using Okta as the authoritative Identity Provider (IdP) for all administrative and automated access to critical infrastructure and sensitive data.

By integrating Vault with Okta via the direct Okta Auth Method, I achieve:
* **Centralized Authentication:** Users authenticate once with their Okta username and password directly through Vault.
* **Enhanced Security:** Integrates with Okta's strong authentication features, including Okta Verify Push, if configured.
* **Simplified Credential Management:** Eliminates managing separate credentials for Vault.
* **Foundation for Advanced PAM:** Sets the stage for implementing Just-in-Time (JIT) access, privileged session management, and dynamic secret generation.

## II. Technical Thought Process & Evolution of Configuration

Our initial intent was to integrate HashiCorp Vault with Okta using **OpenID Connect (OIDC)**, a modern and flexible standard for identity federation. We attempted to enable the OIDC auth method via the Vault CLI.

However, during the validation phase, a significant unexpected issue emerged:
* **Problem Faced:** Although `Okta-oidc/` was successfully enabled and visible when verified via `vault auth list` in the CLI, the **"Okta-oidc" option was conspicuously absent from the Vault UI's login page dropdown**. This prevented UI-based authentication via OIDC.
* **Initial Troubleshooting Attempt:** We pursued common browser-related workarounds, including hard refreshing the browser (`Ctrl + F5`) and clearing browser cache and cookies for the Vault domain. Despite these efforts, the OIDC option did not appear in the UI.

Given the persistence of the UI display issue with OIDC and the immediate goal of establishing a functional PAM integration, a strategic pivot was made.
* **Workaround/Decision:** We opted to configure Vault's native **"Okta" authentication method** (often referred to as the "Okta blade" or direct API integration), which was readily available as an option in the Vault UI under "Infra". This method directly communicates with Okta's Authentication API, bypassing the OIDC flow entirely.

This adaptive approach allowed us to move forward quickly and successfully establish the authentication bridge between Okta and Vault, serving as a practical demonstration of adaptability in a lab environment.

The authentication flow using this chosen "Okta Auth Method" is as follows:
1.  A user attempts to authenticate to Vault (via UI or CLI) using their Okta username and password.
2.  Vault sends these credentials directly to Okta's Authentication API.
3.  Okta authenticates the user (and may prompt for MFA, like Okta Verify Push, if configured).
4.  If successful, Okta responds to Vault with authentication status and user/group information.
5.  Vault uses this information to map the user to pre-defined Vault policies, granting the appropriate level of access to secrets and capabilities.

## III. Prerequisites

Before proceeding, ensure you have the following in place:

* **Okta Developer Account:** Your Okta organization is active and you have administrator access.
* **Test User(s) and Group(s) in Okta:** A test user, specifically `joshua.dominguez126@mellonryon.com`, who is a member of an Okta group named `lab User`.
* **Okta API Token:** This token grants Vault the necessary permissions to query Okta's user and group information.
    * **How to create an Okta API Token:**
        1.  Log in to your Okta Admin Console.
        2.  In the left-hand navigation, go to **"Security"** > **"API"**.
        3.  Click on the **"Tokens"** tab.
        4.  Click **"Create Token"**.
        5.  Give it a **"Name"** (e.g., `Vault-Integration-Token`).
        6.  Click **"Create Token"**.
        7.  **IMPORTANT:** Copy the `Token` value immediately. It will only be shown once. **Save this securely**, as we will need it for the Vault configuration. Treat it like a sensitive password.
* **HashiCorp Vault Cluster:** A running Vault cluster was created. Ensure it is initialized and unsealed.
* **Vault CLI:** The `vault` command-line interface installed and configured to point to your Vault instance.
* **Postman:** Installed and configured for API testing.
* **Network Connectivity:** Ensure your Vault instance can communicate with Okta's API endpoints (outbound HTTPS/443 to your Okta Org URL).

## IV. Configuration Steps

I configured Vault to use the Okta Auth Method, linking it to my Okta organization.

### A. HashiCorp Vault Configuration: Enable and Configure Okta Authentication Method

The Okta authentication method was enabled and configured directly through the Vault UI.

1.  **Access your Vault Instance (UI):**
    * Log in to your Vault UI (e.g., `https://.z1.hashicorp.cloud:*`).
    * Log in with a root token or an administrator token.
<img width="811" height="896" alt="Screenshot 2025-07-12 120625" src="https://github.com/user-attachments/assets/cd2b20dd-dde2-40e3-91b7-d42c43c88ecb" />

2.  **Navigate to Authentication Methods:**
    * In the left-hand navigation, click on **"Access"**.
    * Then click on **"Auth Methods"**.

3.  **Enable the "Okta" Auth Method:**
    * Click on **"Enable new method"**.
    * From the list, select the **"Okta"** method under "Infra".
    * Click **"Next"**.
<img width="1010" height="691" alt="Screenshot 2025-07-12 122502" src="https://github.com/user-attachments/assets/58141de8-b2ca-43a3-b8fb-9392a6d2b098" />

4.  **Configure the Okta Auth Method Details:**
    * **Organization Name:** Set to your Okta domain.
<img width="812" height="152" alt="image" src="https://github.com/user-attachments/assets/d740b95d-f437-4078-bb60-7501bd612f9b" />

    * **API Token:** Paste the **Okta API Token Value** you generated and securely saved in Section III.
<img width="782" height="161" alt="Screenshot 2025-07-12 160754" src="https://github.com/user-attachments/assets/94f977ad-58c3-405b-84a7-e1cf003742d5" />

    * **Base URL (Optional):** This can usually be left as the default (`okta.com`) as it was not specified to be changed.
    * *Note:* The `Bypass Okta MFA` option was not explicitly mentioned as configured, implying Okta's native MFA flow would be used.

5.  **Save the Configuration:**
    * Click the **"Save"** button to apply the configuration.
    * *Confirmation:* The "Okta" method now appears in your list of enabled auth methods, indicating successful configuration.

### B. Vault Secret Engine Configuration

A Key-Value (KV) secrets engine was enabled and a secret was created.

1.  **Enable New Secret Engine:**
    * A new secret engine was enabled with the path `KV`. This is typically done through the Vault UI or CLI.
<img width="809" height="622" alt="Screenshot 2025-07-12 121615" src="https://github.com/user-attachments/assets/9a989223-d204-4252-9ec7-98f4878a9334" />

2.  **Create Secret:**
    * A new secret was created with the path `secret/app/db-credentials`.
<img width="797" height="436" alt="Screenshot 2025-07-12 122035" src="https://github.com/user-attachments/assets/d2aad8aa-37ba-4cfe-806b-29c5a5685fe0" />

### C. Vault Policy Creation

A specific Vault policy was created to define access to secrets.

1.  **Access your Vault Instance (CMD/PowerShell):**
    * Open your Command Prompt or PowerShell or via UI.
    * Ensure you are logged in to Vault with a token that has root  capabilities.
<img width="1608" height="759" alt="image" src="https://github.com/user-attachments/assets/cabb4a91-152a-4dd7-a355-6554685c0e9d" />

2.  **Create `kv-read-policy`:**
    * A policy named `kv-read-policy` was created. This policy grants read and list capabilities to secrets under the `secret/data/*` path.
    ```cmd
    vault policy write kv-read-policy - <<EOF
    path "secret/data/*" {
      capabilities = ["read", "list"]
    }
    EOF
    ```
   <img width="779" height="477" alt="Screenshot 2025-07-12 162714" src="https://github.com/user-attachments/assets/d81ed42e-9b63-48ae-bf67-961e6f745b15" />

### D. HashiCorp Vault: Map Okta Groups to Vault Policies

An Okta group was created and mapped to the Vault policy.

1.  **Create and Map `lab User` Okta Group:**
    * An Okta group named `lab User` was created.
    * This group was then mapped to the `kv-read-policy` within Vault. This ensures that any user who successfully authenticates via Okta and is a member of the Okta group `lab User` receives the `kv-read-policy` Vault policy.
    * *Visual Reference:* See `Pasted image 20250712163302.png` in `PAM with HashiCorp Vault.md`.
    ```cmd
    vault write auth/okta/groups/lab User policies="kv-read-policy"
    ```
<img width="806" height="450" alt="Screenshot 2025-07-12 163259" src="https://github.com/user-attachments/assets/28c48bc0-cf45-4119-bcf1-08e87a14a90a" />

## V. Testing and Validation

Authentication and policy enforcement were successfully tested, including verification via Postman.

1.  **Access Vault UI via Okta Auth Method:**
    * The test user `****@mell**.com`, a member of the `lab User` Okta group, was used to log in to the Vault UI.
    * On the Vault sign-in page, the "Okta" method was selected.
<img width="349" height="452" alt="Screenshot 2025-07-12 160852" src="https://github.com/user-attachments/assets/67c2e82e-bb9b-41b4-99c3-12ec2f27e96e" />


    * The user logged in successfully with their Okta credentials.
<img width="1074" height="523" alt="image" src="https://github.com/user-attachments/assets/0a360d39-03f0-4741-861d-65e3d7933a3d" />

2.  **Confirm User Permission with Postman:**
    * After logging in successfully, the user's token was obtained from their profile icon in the Vault UI.
<img width="227" height="372" alt="image" src="https://github.com/user-attachments/assets/684bbb66-cd69-408f-8ecf-120073d02255" />

    * **Postman Configuration:**
        * A GET request was created in Postman.
<img width="914" height="496" alt="image" src="https://github.com/user-attachments/assets/b3936699-f011-4582-ae25-2f2995ee4a24" />

        * The request header `X-Vault-Token` was set, with the obtained user token as its value.
        * The GET request was sent to the URL `https://***lookup`.
    * **Result:** The GET request returned a `200 OK` status with a JSON body. The body explicitly showed that the token had the policies `kv-read-policy` and `default`, and indicated the username `jos*****.com` and its mapping path `auth/okta/login/****.com`. This confirmed the successful authentication and correct policy assignment.
      
<img width="912" height="876" alt="Screenshot 2025-07-12 165640copy" src="https://github.com/user-attachments/assets/8050740d-b8e0-4a34-bcda-d47103041285" />


## VI. Troubleshooting Common Issues

This section reflects the types of issues I encountered with this setup, including the specific OIDC problem faced, and general troubleshooting for the successful Okta Auth Method.

* **Problem: "Okta-oidc" Auth Method Not Showing in Vault UI (Initial Attempt):**
    * **Context:** This issue occurred during My initial OIDC setup attempt, despite `vault auth list` confirming its enablement via CLI.
    * **Impact:** Prevented UI-based login using the OIDC method.
    * **Troubleshooting & Workaround Applied:** We attempted hard refreshing the browser and clearing cache/cookies, but these did not resolve the UI display issue. As a workaround, we then opted to configure the direct "Okta" authentication method, which was visible and functional.
    * **Suggested Remediation:** If a configured auth method doesn't appear in the UI, try a hard refresh (`Ctrl + F5`), clear browser cache/cookies, and ensure Vault service is running without errors.

* **"Permission denied" during login (UI or CLI) with Okta Auth Method:**
    * **Cause:** Incorrect Okta username or password, or an issue with the Okta API token used in Vault configuration.
    * **Solution:** Double-check Okta credentials and verify the `API Token` is correct, active, and has sufficient permissions in Okta (Read-only Admin is a good start for lab).

* **"Error authenticating: No policies were assigned by the 'okta' plugin" or similar:**
    * **Cause:** The Okta group membership of the authenticating user does not match any configured group mappings in Vault (`auth/okta/groups/<group_name>`). This is crucial for authorization.
    * **Solution:** Ensure the Okta group name configured in Vault (e.g., `lab User`) exactly matches the group name in Okta (case-sensitive). Verify the test user is a member of that Okta group.

* **MFA issues (e.g., push not received, TOTP not accepted) with Okta Auth Method:**
    * **Cause:** Okta MFA configuration, or `bypass_okta_mfa` setting in Vault's Okta auth method config.
    * **Solution:** Ensure Okta Verify or other MFA methods are properly enrolled and active for the test user in Okta. If `Bypass Okta MFA` was checked, be aware Vault won't prompt for Okta's MFA.

* **Vault `syslog` or server logs show errors:**
    * **Cause:** More fundamental issues with the Okta auth method configuration, network, or Vault service.
    * **Solution:** Check the Vault server's output or its configured log files for more detailed error messages.

## VII. Next Steps & Enhancements

With Okta authentication successfully integrated with HashiCorp Vault using the direct Okta Auth Method, you have a strong foundation for advanced PAM. Future enhancements could include:

* **Implementing Dynamic Secrets:** Configure Vault to generate temporary, on-demand credentials for databases, cloud APIs, or SSH, eliminating static secrets.
* **Just-in-Time (JIT) Access:** Define mechanisms to grant privileged access only for a limited time when needed, then automatically revoke it.
* **Secrets Engine Configuration:** Configure specific secret engines in Vault (e.g., AWS, Azure, GCP, Kubernetes, database secrets engines) to manage credentials for various platforms.
* **Vault Agent:** Deploy Vault Agents for applications to securely retrieve secrets without direct application interaction with Vault.
* **Broader Policy Model:** Map multiple Okta groups to tiered Vault policies (read-only, writer, admin).
--- 
