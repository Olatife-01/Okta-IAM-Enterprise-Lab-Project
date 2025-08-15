# Okta Enhanced Security & Contextual Access Policies

## Objective

This stage focuses on implementing advanced security and access control mechanisms within Okta that goes beyond basic MFA. The primary goal is to make access **adaptive**—tightening or relaxing requirements based on network, device, and risk; So authentication and session decisions reflect real-world context and reduce risk without crushing usability. This enhances the overall security posture by requiring stronger authentication or modifying session behavior based on factors like network location, device posture, and user behavior risk.

## Technical Thought Process & Evolution of Configuration

Enterprises need authentication that’s **risk-responsive**: the same password + MFA flow shouldn’t apply identically from a managed laptop on a corporate network and from a new IP in a high-risk geography. Okta’s **Network Zones** give us the primitive to classify access from trusted IPs/VPNs versus anywhere else; **Global Session Policy** governs session lifetime and re-auth patterns across the tenant; and **Authentication Policies** push phishing-resistant factors like **Okta Verify FastPass** at the app edge where it matters most. I began by codifying a **Trusted\_Network\_Zone** for predictable traffic and a **Risky\_Geolocation\_Zone** to capture unusual locations. Session policy came next: I shortened idle/absolute lifetimes and required periodic re-auth, with a stricter path when risk signals (new IP/high risk) are present. Finally, at the application layer, I layered a strong app auth policy: FastPass as the primary (possession, phishing-resistant, user-interaction) for trusted cases, and **two factors** for the catch-all untrusted path—every sign-in, no exceptions. Ordering rules from most specific to broad ensured deterministic evaluation. I validated both **positive** (trusted network) and **negative** (untrusted/new IP) paths and confirmed rule hits in **System Log** events (`policy.evaluate`). This staged approach mirrors production: define zones → tune sessions → harden app auth → iterate with telemetry.


## Key Configurations and Concepts

### 1. Network Zones Configuration

Network Zones are fundamental building blocks for contextual access policies, allowing the classification of IP addresses or geographical locations.

* **Trusted_Network_Zone:**
    * **Type:** IP Zone
    * **Purpose:** Represents trusted network locations (e.g., corporate office egress IPs, specific VPN ranges, or My current public IP for testing). Access from this zone is generally considered less risky.
    * **Configuration:** Configured with specific public IP addresses (e.g., my current IP) or IP ranges.
<img width="631" height="569" alt="Screenshot 2025-07-10 203049" src="https://github.com/user-attachments/assets/b14be7d8-17a5-45d4-a0d9-89a127d91bb2" />

* **Risky_Geolocation_Zone:**
    * **Type:** Dynamic Zone
    * **Purpose:** Identifies and classifies access attempts originating from countries or regions deemed high-risk or unusual for the organization.
    * **Configuration:** Configured to include or exclude specific countries (e.g., countries far from my usual operational areas).
<img width="959" height="194" alt="Screenshot 2025-07-10 203510" src="https://github.com/user-attachments/assets/5c94fa3c-0f28-4a34-b83f-ed9efab2d4c5" />

### 2. Global Session Policy (`Enterprise_Session_Policy`) Setup

Global Session Policies control the maximum session lifetime and re-authentication requirements for users across all applications managed by Okta. This policy was applied to the IT group (Bamboo HR).

* **Policy Name:** `Enterprise_Session_Policy`
* **Assigned to Groups:** IT group (Bamboo HR)
* **Policy Order:** Placed **above** the `Default Policy` to ensure precedence for users in the IT group (Bamboo HR).

#### **Rules within `Enterprise_Session_Policy`:**

Rules are evaluated from top to bottom.

* **Rule 1: `Trusted_Network_Access`**
    * **Purpose:** Defines session behavior for users accessing Okta from a known trusted network.
    * **Conditions:**
        * **Users:** `Users assigned to this policy` (`IT group (Bamboo HR)`).
        * **Access from:** `In zone` -> `Trusted_Network_Zone`.
    * **Actions:**
        * **Establish the user session with:** `Any factor used to meet the authentication policy requirement`.
        * **Maximum Okta session lifetime:** `8 hours`.
        * **Re-authentication frequency:** `4 hours`.
        * **Idle session lifetime:** `30 minutes`.
    * **Rule Order:** Placed **above** `Untrusted_Network_Access` within the `Enterprise_Session_Policy`.

* **Rule 2: `Untrusted_Network_Access`**
    * **Purpose:** Defines session behavior for high-risk access attempts originating from potentially untrusted or new locations, enforcing a re-authentication with MFA.
    * **Conditions:**
        * **Users:** `Users assigned to this policy` (`IT group (Bamboo HR)`).
        * **Exclude Users:** `Excluded users` (a specific group you might define for exceptions).
        * **Access from:** `Anywhere`.
        * **IDP is:** `Any`.
        * **Authenticates Via:** `Any`.
        * **Behavior is:** `New IP`.
        * **Risk is:** `High`.
    * **Actions:**
        * **Access is:** `Allowed`.
        * **Establish the user session with:** `Any factor used to meet the Auth policy requirement`.
        * **MFA is:** `Required`.
        * **User will be prompted for MFA:** `After MFA lifetime expires for device cookies`.
        * **MFA Lifetime:** `9 hours`.
        * **Maximum Okta Global Session:** `9 hours`.
        * **Maximum Global Session Idle Time:** `1 hour`.
        * **Okta global session persist across browser sessions:** `Disabled`.
    * **Rule Order:** Placed **below** `Trusted_Network_Access` within the `Enterprise_Session_Policy`.
<img width="952" height="492" alt="Screenshot 2025-07-10 210017" src="https://github.com/user-attachments/assets/0b793bfc-c0e3-4fe4-a4b0-192696f32322" />

### 3. Authentication Policy (`Enterprise_App_Auth_Policy`) Setup

Authentication Policies control *how* users authenticate to specific applications, dictating the required factors based on context. This policy was applied to the `IT group (Bamboo HR)` group and then assigned to a test application (e.g., BambooHR).

* **Policy Name:** `Enterprise_App_Auth_Policy`
* **Assigned to Groups:** `IT group (Bamboo HR)`
* **Application Assignment:** Applied to a chosen test application (e.g., BambooHR, Zendesk).

#### **Rules within `Enterprise_App_Auth_Policy`:**

Rules are evaluated from top to bottom.

* **Rule 1: `App_Auth_Trusted_Network`**
    * **Purpose:** Defines a highly secure, phishing-resistant authentication requirement for trusted scenarios (e.g., managed devices, low risk).
    * **Conditions:**
        * **Group:** IT group (Bamboo HR) .
        * **Risk:** `Low`.
        * **Device:** `Registered, Managed`.
    * **Actions:**
        * **Access:** `Allowed with possession factor`.
        * **Authenticators:** `Okta Verify - FastPass` (configured to satisfy both Knowledge/Biometric AND Additional factor types).
        * **Possession factor constraints:** `Phishing resistant, Require user interaction`.
        * **Authentication methods:** `Allow any method that can be used to meet the requirement`.
        * **Re-authentication frequency:** `When an Okta global session doesn't exist`.
    * **Rule Order:** Placed **above** `App_Auth_Untrusted_Network` within the `Enterprise_App_Auth_Policy`.
<img width="916" height="423" alt="Screenshot 2025-07-10 211045" src="https://github.com/user-attachments/assets/6135f958-4b27-43f5-a476-9470c06518a4" />

* **Rule 2: `App_Auth_Untrusted_Network`**
    * **Purpose:** Acts as a catch-all for untrusted access, enforcing a strict, multi-factor authentication requirement every time.
    * **Conditions:**
        * **IF:** `Any request` (meaning, if no higher-priority rule matches).
    * **Actions:**
        * **Access:** `Allowed with any 2 factor types`.
        * **Authenticators:**
            * Knowledge / Biometric factor types: `Password` **or** `Okta Verify - FastPass`.
            * AND
            * Additional factor types: `Okta Verify - FastPass`.
        * **Possession factor constraints:** `Phishing resistant, Require user interaction`.
        * **Authentication methods:** `Allow any method that can be used to meet the requirement`.
        * **Re-authentication frequency:** `Every time user signs in to resource`.
    * **Rule Order:** Placed **below** `App_Auth_Trusted_Network` within the `Enterprise_App_Auth_Policy`.
<img width="907" height="637" alt="Screenshot 2025-07-10 211117" src="https://github.com/user-attachments/assets/3d30a225-948c-484a-b890-fa06c76e3d31" />

### 4. Testing & Validation

Rigorous testing was conducted to confirm the correct application of these policies.

* **Test User:** Jeremy Smith (a member of the `IT group (Bamboo HR)` group).
* **Test Cases:**
    * **Trusted Network Access:** Jeremy logged in from an IP address within the `Trusted_Network_Zone`.
    * **Untrusted Network Access:** Jeremy logged in from an IP address outside the `Trusted_Network_Zone` (simulating a "New IP" or general untrusted location), after clearing browser cookies.
* **Validation:** Both the Global Session Policy rules and Authentication Policy rules were triggered accordingly for their respective test cases. This was verified by observing the login experience and by inspecting the Okta System Log (`Reports > System Log`) for `policy.evaluate` events, confirming which rules were applied.

## Security Notes & Audit Hooks

* **Principle of Least Privilege:** Narrow group assignments (IT group) and specific network zones reduce unintended exposure.
* **Phishing Resistance:** Prefer **FastPass** with user interaction on trusted paths; require **two factors** for untrusted.
* **Session Hardening:** Shorter idle/absolute lifetimes; no persistent sessions on high-risk paths.
* **Monitoring:** Stream **Okta System Log** to **Splunk**; build panels/alerts for `policy.evaluate`, `authentication.challenge`, and anomalous geo/IP patterns (ties to ISO 27001 A.12.4.1).
* **Change Control:** Track policy/zone changes in Git (export JSON via APIs or admin reports) and reference in your CI/CD audit notes.
* **Evidence:** Keep screenshots and System Log exports per test case for ISO/SOX artifacts.

---

