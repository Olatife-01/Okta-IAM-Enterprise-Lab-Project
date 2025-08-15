# Endpoint Security & Conditional Access — Okta Device Assurance

## I. Objective & Purpose

This lab demonstrates the implementation of **Endpoint Security and Conditional Access** using **Okta Device Assurance Policies** and **Authentication Policies** so that access decisions incorporate device posture (managed/compliant state, OS/version, encryption, screen lock). The objective is to illustrate how device posture and management status can be integrated into access decisions, enhancing the security of Okta-protected resources.

By configuring Device Assurance, I aim to:

- **Enforce Device Compliance:** Define minimum security requirements for devices accessing sensitive applications.
    
- **Implement Conditional Access:** Grant or deny access based on device attributes (e.g., managed, compliant, OS version, disk encryption).
    
- **Enhance Security Posture:** Reduce risk by ensuring access originates from trusted and secure endpoints.
    
- **Simulate Real-World Scenarios:** Understand the policy configuration, even without a full MDM/EDR integration.
    

## II. Technical Thought Process & Evolution of Configuration

Enterprise access should be **context-aware**: identity strength alone is insufficient when device posture is unknown. Device Assurance provides a standards-aligned way to express endpoint requirements (OS baseline, disk encryption, lock screen) and surface those attributes to policy. Authentication Policies then make deterministic allow/deny decisions at the app edge.

Given a free tenant and no full MDM/EDR, the design favored **Okta Verify** as the attribute provider because it is native, reliable, and suitable for establishing a basic posture signal. Initial instructions pointed to legacy Device Trust under Global Session Policy; the current model places **Device Assurance** under **Security > Device Assurance Policies** and binds evaluation within **Security > Authentication Policies**. An unexpected platform prerequisite blocked Windows policy creation until **Security > Device Integrations > Endpoint Security** was enabled (Desktop, Okta as CA with SCEP).

During validation, a denial rule targeting unmanaged devices did not manifest as a hard block. Okta FastPass registration presented the endpoint as “registered” with sufficient assurance to satisfy evaluation in practice. To preserve the intended control for demonstration, the rule was refined to **deny** when: *Device state = Registered* **AND** *Device management = Not managed* **AND** *Device assurance policy = No policy* (Windows). The result documents the policy intent and shows how a production deployment would behave when backed by MDM/EDR signals, while acknowledging FastPass’s strong native trust capabilities.

**Key Design Decisions:**

- **Device Assurance Policies:** Chosen as the mechanism to define device compliance attributes (e.g., minimum OS version, disk encryption, screen lock).
    
- **Authentication Policies:** Used to enforce the Device Assurance Policy by denying access if a device does not meet the defined conditions.
    
- **Okta Verify as Provider:** Relied on Okta Verify as the device attribute provider for basic signals, as it's built into Okta's ecosystem.
    

## III. Prerequisites

Before proceeding, ensure you have the following in place:

- **Okta Admin Access:** Your Okta Developer organization with super administrator access.
    
- **Okta FastPass Enabled:** Confirmed enabled in **Security > Authenticators**. Add okta Verify as authenticator (to include fastPass)
<img width="863" height="907" alt="Screenshot 2025-07-30 191623" src="https://github.com/user-attachments/assets/eecef524-bf60-4b3b-bd82-cf05b3628ec0" />
  
- **Okta Test User:** A test user (e.g., `Joshua Dominguez`) assigned to the Salesforce application.
    
- **Test Device:** A Windows (or macOS) PC for testing, preferably with the Okta Verify browser plugin installed.
    

## IV. Configuration Steps: Okta Device Assurance Policies

This section details the setup of device-based conditional access.

### A. Phase 1: Enable Windows Platform for Device Integrations

This is a prerequisite for creating Windows Device Assurance Policies.

1. **Log in to your Okta Admin Console.**
    
2. Go to **Security** > **Device Integrations**.
    
3. Select **"Endpoint Security"**.
    
4. If prompted, click **"Add device management platform"**.
    
5. **Step 1: Select Platform:** Choose **"Desktop (Windows and macOS only)"**. Click **"Next"**.
<img width="868" height="792" alt="Screenshot 2025-07-30 192755" src="https://github.com/user-attachments/assets/38332558-842b-4f8b-955d-92c66b1dac81" />

6. **Step 2: Configure Management Attestation:**
    
    - **Certificate authority:** Select **"Use Okta as certificate authority"**.
        
    - **SCEP URL challenge type:** Select **"Static SCEP URL"**.
        
    - Click **"Generate"** for the SCEP URL.
        
    - Click **"Save"**.
<img width="875" height="912" alt="Screenshot 2025-07-30 192924" src="https://github.com/user-attachments/assets/c39f0a63-3d0c-4aef-b0a1-4e897d9c924a" />
        
### B. Phase 2: Create a Device Assurance Policy

This policy defines what a "compliant" Windows device looks like.

1. **Log in to your Okta Admin Console.**
    
2. Go to **Security** > **Device Assurance Policies**.
    
3. Click **"Add a policy"**.
<img width="889" height="698" alt="Screenshot 2025-07-30 191746" src="https://github.com/user-attachments/assets/14b5d9ed-9638-4a15-9704-1405c6142975" />
    
4. **Policy name:** `Lab - Compliant Windows Device`.
    
5. **Platform:** Select **"Windows"**.
    
6. **Device attribute provider(s):** Check **"Okta Verify"**. (Uncheck "Chrome Device Trust" if it's selected).
    
7. **Windows Okta Device Attributes:**
    
    - **Minimum Windows version:** Select **"Use a preset version"** and choose a recent version like **"Windows 10 (22H2)"** or **"Windows 11 (22H2)"**.
        
    - **Lock screen:** Check **"Windows Hello must be enabled"**.
        
    - **Disk encryption:** Check **"Device disk must be encrypted"**.
        
    - **Trusted Platform Module:** Leave **UNCHECKED**.
        
8. Click **"Save"**.
<img width="696" height="872" alt="Screenshot 2025-07-30 192125" src="https://github.com/user-attachments/assets/3ef486ea-0757-44c0-bac4-aef4503df6a9" />
  
 > **Note**   - If chrome Trust is allowed:   
<img width="688" height="902" alt="Screenshot 2025-07-30 192216" src="https://github.com/user-attachments/assets/2174ef10-121e-4492-9295-c88e90739af7" />

### C. Phase 3: Create/Modify an Authentication Policy Rule to Use Device Assurance

This rule will enforce the device assurance policy for access to the Salesforce application.

1. **Log in to your Okta Admin Console.**
    
2. Go to **Security** > **Authentication Policies**.
    
3. Click on the **"Default Policy"** (or your "EDR/MDM Policy" if you created it and assigned it to Salesforce).
    
4. Click **"Add Rule"**.
    
5. **Rule name:** `Require Compliant Device for Salesforce Lab`.
    
6. **IF User's user type is:** `Any user type`.
    
7. **AND User's group membership includes:** `Any group`.
    
8. **AND User is:** `Any user`.
    
9. **AND Device state is:** Select **"Registered"**.
    
10. **AND Device management is:** Select **"Not managed"**.
    
11. **AND Device assurance policy is:** Select **"No policy"**. _(This is the critical setting to ensure the rule triggers if the device is "Not managed" regardless of other assurance checks)._
    
12. **AND Device platform is:** Select **"Windows"**.
    
13. **AND User's IP is:** `Any IP`.
    
14. **AND Risk is:** `Any`.
   
15. **THEN Access is:** Select **"Denied"**.
    
16. Click **"Create Rule"**.
    
17. **Adjust Rule Priority:** Drag this new rule **`Require Compliant Device for Salesforce Lab`** to the **TOP** of the rule list within its policy.
    
18. **Assign Policy to App (if using a custom policy):** If you created a new policy (e.g., "EDR/MDM Policy"), ensure it's assigned to your **"Salesforce.com"** application under **Applications > Applications > Salesforce.com > Sign On > Sign On Policy**.
<img width="845" height="533" alt="Screenshot 2025-07-30 195229" src="https://github.com/user-attachments/assets/ab39db06-2878-4fb0-aa3f-0cce8c15d198" />
    

## V. Verification & Simulated Outcome

This section describes the expected behavior of the policy.

1. **Test Scenario:** An Okta test user (e.g., `Joshua Dominguez`), assigned to the Salesforce application, attempts to launch Salesforce from a personal Windows PC.
    
2. **Expected Policy Evaluation:**
    
    - The `Require Compliant Device for Salesforce Lab` rule will be evaluated first due to its priority.
        
    - The conditions "Device state is: Registered" and "Device management is: Not managed" (which is true for a personal PC without a full MDM) will be met.
        
    - The rule's action "THEN Access is: Denied" will trigger.
        
3. **Expected Outcome:** The user is **explicitly denied access** with a message from Okta stating that their device does not meet the security requirements.
    
    - **Note for Lab:** In my environment, due to the presence of Okta Verify and the browser plugin on the test PC, the device is implicitly recognized as "Managed" by Okta FastPass, thus bypassing the denial. However, the policy configuration accurately reflects the intent to deny access from unmanaged/non-compliant devices in a real-world scenario with a properly integrated MDM/EDR solution.
    - **Evidence:** Confirm rule hits in **Reports > System Log** (`policy.evaluate`, device context fields) and capture screenshots of the decision flow.
    

## VI. Troubleshooting & Lessons Learned

This section highlights the challenges encountered and their resolutions.
        
- **Platform Enablement Prerequisite:**
    
    - **Problem:** Could not save Device Assurance Policy due to a prerequisite error: "Please enable the Windows platform in Security > Device Integrations > Endpoint Security > Chrome Device Trust before saving."
        
    - **Root Cause:** A dependency required enabling the Windows platform for device integration, even if "Chrome Device Trust" wasn't explicitly selected as a policy provider.
        
    - **Resolution:** Completed the "Add device management platform" wizard under **Security > Device Integrations > Endpoint Security**, selecting "Desktop (Windows and macOS only)" and "Use Okta as certificate authority."
        
    - **Lesson:** Be aware of implicit prerequisites and dependencies for new features.
        
- **Persistent Access Despite Denial Policy (Simulated Outcome):**
    
    - **Problem:** The test user could still access the Salesforce app, even with the denial rule.
        
    - **Root Cause:** Okta FastPass (via Okta Verify and browser plugin) was implicitly registering the test PC as "Managed/Compliant," overriding the intended denial for an "unmanaged" device.
        
    - **Lesson:** Okta FastPass provides robust device trust signals that can fulfill policy requirements, even without a separate MDM. For precise "deny if unmanaged" lab scenarios, explicit MDM integration or targeting "Not Registered" devices is critical.


## VII. Security Notes & Audit Hooks

* **Zero-Trust alignment:** Combine *who* (identity) with *what* (device posture) for access.
* **Phishing resistance:** Prefer FastPass where allowed; require additional factors for lower-assurance contexts.
* **Telemetry:** Forward **System Log** to Splunk; monitor `policy.evaluate`, device attributes (OS version, encryption), and unusual access by network zone.
* **Audit artifacts:** Preserve policy JSON/exports, screenshots of settings, and System Log extracts per test case to support ISO 27001 A.9/A.12 evidence and SOX change control.

## VIII. Next Steps & Enhancements

With the implementation of Endpoint Security & Conditional Access demonstrated, future enhancements for the Enterprise IAM Lab could include:

- **Full MDM/EDR Integration:** Integrate a trial version of a real MDM (e.g., Microsoft Intune, Jamf Pro) or EDR solution to send actual device posture signals to Okta.
    
- **Granular Remediation:** Configure specific remediation instructions for users who fail device compliance checks.
    
- **Adaptive MFA:** Implement policies that require stronger MFA factors based on device compliance status (e.g., if device is not compliant, require a biometric factor).

