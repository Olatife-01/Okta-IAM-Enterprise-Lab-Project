# AWS IAM Identity Center — SAML SSO + SCIM (Okta → AWS)

> **Scope:** I federated Okta to **AWS IAM Identity Center** (formerly AWS SSO) for **SAML SSO** and enabled **SCIM** so users/groups and assignments can be managed centrally in Okta. Access in AWS is enforced via **Permission Sets** mapped to **Okta Push Groups**. Terraform-based role/account provisioning is documented separately.

## I. Objective & Purpose

This lab demonstrates the implementation of **federated access (Single Sign-On - SSO)** from **Okta** to the **AWS Management Console** using **AWS IAM Identity Center** (formerly AWS Single Sign-On). The primary objective is to enable Okta-managed users to securely sign in to AWS accounts and assume specific AWS IAM roles, centralizing identity management and enhancing security posture.

By establishing this federation, we achieve:

- **Centralized Authentication:** Users authenticate once with their Okta credentials (leveraging Okta's MFA and policies) to access AWS.
    
- **Simplified Access:** Eliminates the need for separate AWS IAM user credentials for each individual, reducing credential sprawl.
    
- **Role-Based Access Control:** Users assume specific, pre-defined AWS IAM roles upon federation, enforcing least privilege.
    
- **Automated User & Group Synchronization:** Okta automatically provisions users and groups to AWS IAM Identity Center via SCIM, streamlining lifecycle management.
    
- **Enhanced Auditability:** All authentication and access attempts are logged in Okta's System Log (and streamed to Splunk).
    

## II. Technical Thought Process & Evolution of Configuration

Implementing Okta federation with AWS involved navigating the evolving AWS SSO landscape and ensuring precise configuration between the two platforms.

**Key Design Decisions:**

- **AWS IAM Identity Center:** The decision was made to use AWS IAM Identity Center as the central point for AWS SSO. This service simplifies multi-account access, integrates with external IdPs like Okta, and is the recommended AWS approach for workforce SSO.
    
- **SAML 2.0:** SAML (Security Assertion Markup Language) was chosen as the protocol for federation, as it is the industry standard for enterprise SSO between an Identity Provider (Okta) and a Service Provider (AWS).
    
- **SCIM Provisioning:** To enable group-based assignments and automated user lifecycle management within AWS IAM Identity Center, SCIM (System for Cross-domain Identity Management) provisioning was implemented from Okta to AWS.
    

**Challenges Encountered & Resolutions:**

1. **AWS SSO Service Identification:**
    
    - **Problem:** Initial confusion arose between the legacy AWS IAM Identity Provider (SAML federation directly to IAM) and the newer AWS IAM Identity Center service.
        
    - **Resolution:** Confirmed that **AWS IAM Identity Center** is the correct and recommended service for centralized workforce SSO, despite its prior naming.
        
2. **IdP SAML Metadata Handling:**
    
    - **Problem:** AWS IAM Identity Center's setup process initially seemed to only allow uploading an XML certificate, not a metadata URL, leading to an "IdP could not be added" error when a `.cert` file was uploaded instead of the full XML metadata.
        
    - **Resolution:** The Okta documentation clarified that AWS IAM Identity Center requires the **full IdP SAML metadata XML file** (e.g., `metadata.xml`) to be downloaded from Okta and then **uploaded directly** to AWS, rather than providing a URL or just a certificate.
        
3. **Lack of User/Group Synchronization (Post-SAML Setup):**
    
    - **Problem:** After successfully configuring SAML, users and groups from Okta were not visible in AWS IAM Identity Center for assignment.
        
    - **Root Cause:** SAML only handles authentication. **SCIM provisioning** is required to synchronize user and group identities from Okta into AWS IAM Identity Center.
        
    - **Resolution:** Enabled and configured SCIM provisioning in the Okta "AWS IAM Identity Center" application, obtained the SCIM endpoint URL and Access Token from AWS IAM Identity Center settings, and configured these in Okta.
        
4. **Group Provisioning Mechanism:**
    
    - **Problem:** After enabling SCIM, group provisioning was still not immediately apparent via the general "To App" provisioning settings in Okta.
        
    - **Root Cause:** The AWS IAM Identity Center app in Okta uses a dedicated **"Push Groups" tab** for managing group synchronization, separate from general user provisioning settings.
        
    - **Resolution:** Explicitly used the "Push Groups" tab to select and push the `Lab User` group to AWS IAM Identity Center.
        

## III. Prerequisites

Before proceeding, ensure you have the following in place:

- **AWS Account:** An active AWS account with root user or IAM administrator access.
    
- **Okta Developer Account:** An active Okta Developer organization with super administrator access.
    
- **Okta Test User(s) and Group(s):** At least one Okta test user (e.g., `Joshua Dominguez`) who is a member of a test group (e.g., `Lab users`).
    
- **Terraform CLI:** Installed and configured (for managing AWS IAM Roles, as detailed in the separate Terraform lab documentation).
    

## IV. Configuration Steps: Okta + AWS IAM Identity Center Federation

This section details the step-by-step process for setting up SAML federation and SCIM provisioning.

### A. Phase 1: Get Okta SAML Metadata (In Okta Admin Console)

1. **Log in to your Okta Admin Console.**
    
2. **Add the AWS IAM Identity Center Application:**
    
    - Navigate to **"Applications"** > **"Applications"**.
        
    - Click **"Browse App Catalog"**.
        
    - Search for **"AWS IAM Identity Center"** and select it.
        
    - Click **"Add integration"**.
        
    - **Application label:** (e.g., "AWS IAM Identity Center"). Click **"Done"**.
        <img width="904" height="856" alt="Screenshot 2025-07-29 191750" src="https://github.com/user-attachments/assets/650f1a11-48a9-4bc2-a733-7b01b73e0528" />

3. **Get Okta's IdP SAML Metadata XML File:**
    
    - On the AWS IAM Identity Center application page in Okta, click the **"Sign On"** tab.
        
    - Under **"SAML Signing Certificates"**, select **"View IdP Metadata"** from the **Actions** drop-down menu.
        
    - **Save the contents of the XML page as `metadata.xml`** to your local system. This file contains Okta's SAML metadata.
        

### B. Phase 2: Configure AWS IAM Identity Center (In AWS Management Console)

This step establishes trust in AWS and obtains necessary URLs for Okta.

1. **Log in to the AWS Management Console.**
    
2. **Navigate to IAM Identity Center:**
    
    - In the search bar, type `IAM Identity Center` and select it.
        
3. **Enable IAM Identity Center (if not already enabled):**
    
    - If prompted, click **"Enable"** in the upper right.
        <img width="966" height="848" alt="Screenshot 2025-07-29 193613" src="https://github.com/user-attachments/assets/e3270b0c-5494-466d-b825-9553373b9beb" />

4. **Change Identity Source to External Identity Provider:**
    
    - In the left-hand navigation, click **"Settings"**.
        
    - Under "Identity source", click **"Change identity source"** from the **Actions** drop-down menu.
        
    - Select **"External identity provider"**. Click **"Next"**.
        <img width="973" height="796" alt="Screenshot 2025-07-29 194128" src="https://github.com/user-attachments/assets/ed2978ab-4c94-4a54-8bdd-1fe262698eb5" />

5. **Configure External Identity Provider (Upload Okta's Metadata):**
    
    - **IdP SAML metadata:** Click **"Choose file"** and **upload the `metadata.xml` file** you saved from Okta in Phase 1.
        
    - **Copy the following URLs** displayed on this page and **save them securely**:
        
        - **AWS access portal sign-in URL** (e.g., `https://d-c3677b1c00.awsapps.com/start`)
            
        - **IAM Identity Center ACS URL** (e.g., `https://eu-north-1.signin.aws.amazon.com/platform/saml/d-c3677b1c00`)
            
        - **IAM Identity Center issuer URL** (e.g., `https://identitycenter.amazonaws.com/ssoins-6508b501b3e38cd0`)
            <img width="704" height="594" alt="Screenshot 2025-07-29 194433" src="https://github.com/user-attachments/assets/caa7bcdc-ae29-4430-a332-afcf0fada0d2" />

    - Click **"Next"**.
        
6. **Review and Confirm:**
    
    - Type **`ACCEPT`** (all caps) into the confirmation box.
        
    - Click **"Change identity source"**.
        
    - _Confirmation:_ A success banner will confirm the identity source change.
        

### C. Phase 3: Configure Okta AWS IAM Identity Center App (In Okta Admin Console)

This step completes the SAML configuration in Okta using URLs from AWS.

1. **Go back to your Okta Admin Console** (your AWS IAM Identity Center application page).
    
2. Click on the **"Sign On"** tab.
    
3. Click **"Edit"**.
    
4. Enter your **AWS IAM Identity Center SSO ACS URL** and **AWS IAM Identity Center SSO issuer URL** (the values you copied from AWS in Phase 2) into the corresponding fields.
    <img width="581" height="454" alt="Screenshot 2025-07-29 195625" src="https://github.com/user-attachments/assets/fa4605cd-c672-43fe-9eaa-a98f3d766859" />

5. **Application username format:** Select an appropriate option (e.g., "Okta username" or "Email"). This value must be unique for users in AWS IAM Identity Center.
    
6. Click **"Save"**.
   <img width="960" height="853" alt="Screenshot 2025-07-29 200323" src="https://github.com/user-attachments/assets/2754d21a-0588-4f96-a064-5668923c6c26" />

### D. Phase 4: Define Permission Sets in AWS IAM Identity Center (In AWS Management Console)

Permission sets define the access users will have in your AWS accounts.

1. **Log in to your AWS Management Console.**
    
2. **Navigate to IAM Identity Center.**
    
3. In the left-hand navigation, click **"Permission sets"**.
    
4. Click **"Create permission set"**.
    
5. **Permission set type:** Select **"Custom permission set"**. Click **"Next"**.
    <img width="982" height="663" alt="Screenshot 2025-07-29 200836" src="https://github.com/user-attachments/assets/cfa4f0e8-e0ad-4d6d-b3d0-24165a4c6524" />

6. **Specify permission set details:**
    
    - **Permission set name:** `OktaReadOnlyAccess`.
        
    - **Description:** `Provides read-only access for Okta federated users.`
        
    - Leave other settings as default. Click **"Next"**.
        <img width="959" height="853" alt="Screenshot 2025-07-29 201139" src="https://github.com/user-attachments/assets/70530408-4eaa-4aff-a3b6-32723b355acb" />
        <img width="958" height="843" alt="Screenshot 2025-07-29 201750" src="https://github.com/user-attachments/assets/29de25f2-2c54-4db4-9c26-5fa412b7420c" />
        <img width="962" height="808" alt="Screenshot 2025-07-29 202041" src="https://github.com/user-attachments/assets/97286946-acff-4f33-b670-cbb72a26d74a" />
        <img width="977" height="689" alt="Screenshot 2025-07-29 202237" src="https://github.com/user-attachments/assets/b7b97a9b-15a9-4a8f-a0c4-42043f9d75f7" />
        
7. **Attach AWS managed policies:**
    
    - Expand **"AWS managed policies"**.
        
    - In the search bar, type `ReadOnlyAccess`.
        
    - Check the checkbox next to **"ReadOnlyAccess"** (the generic one). If not found, check **"AmazonEC2ReadOnlyAccess"** as an alternative.
        
    - Click **"Next"**.
        <img width="966" height="853" alt="Screenshot 2025-07-29 202433" src="https://github.com/user-attachments/assets/b7d9e9a6-61fc-410b-962f-0be00cc17911" />

8. **Review and Create:**
    
    - Review the details. Click **"Create permission set"**.
        <img width="977" height="689" alt="Screenshot 2025-07-29 202237" src="https://github.com/user-attachments/assets/6830bbc6-92ca-4f53-84af-cf9e868c4b99" />


### E. Phase 5: Configure SCIM Provisioning (Okta to AWS IAM Identity Center)

This crucial step synchronizes users and groups from Okta to AWS IAM Identity Center.

1. **Get SCIM Endpoint and Token from AWS:**
    
    - **Log in to your AWS Management Console.**
        
    - Navigate to **IAM Identity Center**.
        
    - In the left-hand navigation, click **"Settings"**.
        
    - Under "Automatic provisioning", click **"Enable"**.
        
    - AWS will display the **SCIM endpoint URL** and an **Access token**. **IMMEDIATELY copy both of these values and save them securely.**
        <img width="701" height="685" alt="Screenshot 2025-07-29 203017" src="https://github.com/user-attachments/assets/24b4d7a7-0103-41c0-8aac-ec28ae3b227b" />

2. **Configure Provisioning in Okta:**
    
    - **Log in to your Okta Admin Console.**
        
    - Go to your **"AWS IAM Identity Center"** application.
        
    - Click on the **"Provisioning"** tab.
        
    - Click **"Configure API Integration"**.
        
    - Check **"Enable API Integration"**.
        
    - **SCIM connector base URL:** Paste the **SCIM endpoint URL** from AWS.
        
    - **Authentication Mode:** Select **"OAuth 2.0"**.
        
    - **OAuth Bearer Token:** Paste the **Access token** from AWS.
        
    - Click **"Test API Credentials"**. (Should succeed).
        
    - Click **"Save"**.
        <img width="762" height="791" alt="Screenshot 2025-07-29 203421" src="https://github.com/user-attachments/assets/7cc3590b-fded-41bc-abc2-33456c005455" />

3. **Configure Provisioning Features ("To App") in Okta:**
    
    - On the **"Provisioning"** tab, on the left, click **"To App"**.
        
    - Click **"Edit"**.
        
    - Check: **"Create Users"**, **"Update User Attributes"**, **"Deactivate Users"**.
        
    - Click **"Save"**.
      <img width="769" height="775" alt="Screenshot 2025-07-29 203610" src="https://github.com/user-attachments/assets/4abc396b-9f22-491c-9dcc-dd44562347ec" />
  
4. **Push Groups from Okta (Dedicated Tab):**
    
    - On the AWS IAM Identity Center app in Okta, click the **"Push Groups"** tab.
        
    - Click **"+ Push Groups"** > **"Find groups by name"**.
        
    - Search for and select your **`Lab users`** group.
        
    - Under "Match result & push action", select **"Create Group"**.
        
    - Click **"Save"**.
        <img width="800" height="686" alt="Screenshot 2025-07-29 204511" src="https://github.com/user-attachments/assets/84903077-4910-4ae4-b9a3-e5623cbcc79e" />
        <img width="784" height="799" alt="Screenshot 2025-07-29 204601" src="https://github.com/user-attachments/assets/93c813ef-a518-4e66-806f-40bf9a210923" />
        <img width="830" height="498" alt="Screenshot 2025-07-29 204920" src="https://github.com/user-attachments/assets/f59dbb1d-eff2-4e1a-947e-99847dfd0d5c" />

    - **Wait a few minutes** for the group to synchronize. Verify its "Push Status" becomes "Active".
        

### F. Phase 6: Assign Users/Groups to AWS Accounts (in IAM Identity Center)

This step links the synchronized Okta group to your AWS account and the permission set.

1. **Log in to your AWS Management Console.**
    
2. **Navigate to IAM Identity Center.**
    
3. In the left-hand navigation, click **"AWS accounts"**.
    
4. Select the **checkbox** next to your **AWS account**.
    
5. Click **"Assign users or groups"**.
    <img width="964" height="848" alt="Screenshot 2025-07-29 204000" src="https://github.com/user-attachments/assets/42345d8a-00bf-4915-b3d8-d8db552b02e9" />

6. **Select users and groups:**
    
    - **Identity source:** Ensure "External identity provider" is selected.
        
    - **Users or groups:** Click the **"Groups"** tab.
        
    - Select the **checkbox** next to your **`Lab users`** group (it should now be visible).
        <img width="669" height="589" alt="Screenshot 2025-07-29 204952" src="https://github.com/user-attachments/assets/4394f2dd-31a8-480b-b355-399d033e7d42" />

    - Click **"Next"**.
        <img width="794" height="840" alt="Screenshot 2025-07-29 203825" src="https://github.com/user-attachments/assets/ffcd73a2-c819-40e2-8020-e4822c17d262" />

7. **Select permission sets:**
    
    - Select the **checkbox** next to the **`OktaReadOnlyAccess`** permission set.
        
    - Click **"Next"**.
       <img width="674" height="767" alt="Screenshot 2025-07-29 205442" src="https://github.com/user-attachments/assets/8662a49d-69c2-433f-b5c9-e55da6bc6c0f" />
       <img width="656" height="669" alt="Screenshot 2025-07-29 205349" src="https://github.com/user-attachments/assets/99bc5cb5-1b22-4f1d-8465-2f3751cfff72" />

8. **Review and Submit:**
    
    - Review the summary. Click **"Submit"**.
     <img width="652" height="429" alt="Screenshot 2025-07-29 205508" src="https://github.com/user-attachments/assets/04770f1b-cd65-4050-9df9-7e5e6a359849" />
   

### G. Phase 7: Test Federated Access to AWS Console

This is the final verification.

1. **Open a new incognito/private browser window.**
    
2. Go to your **Okta End-User Dashboard** (e.g., `https://trial-5828141.okta.com/`).
    
3. Log in with an **Okta test user** who is a member of your `Lab users` group.
    
4. You should see the **"AWS IAM Identity Center"** application icon. Click it.
    <img width="909" height="777" alt="Screenshot 2025-07-29 205631" src="https://github.com/user-attachments/assets/aacc6c0b-3639-4a91-8e54-b52951a5742e" />

5. You should be redirected to the **AWS Access Portal**.
    
6. Click on the **"AWS Account"** you were assigned to.
    
7. Click on the **"Management console"** link next to the `OktaReadOnlyAccess` permission set.
    
8. You should be redirected to the **AWS Management Console**, logged in as the federated user, with the `OktaReadOnlyAccess` role assumed.
    <img width="912" height="522" alt="Screenshot 2025-07-29 205806" src="https://github.com/user-attachments/assets/65321457-58ee-4de5-bf05-1edafb7d2e7d" />

9. **Verify Permissions:** Navigate to **S3** and **EC2** (Instances).
    
    - You should be able to **see** your `mellonryon-fed-access-test-bucket-boluw-29jul-v2` S3 bucket.
        
    - You should be able to **see** your `MellonryonServer` EC2 instance.
        
    - Try to upload a file to S3, delete the bucket, or stop/terminate the EC2 instance. You should receive an **"Access Denied"** error, confirming that the `ReadOnlyAccess` policy is correctly enforced.
       
## V. Troubleshooting & Lessons Learned

- **AWS SSO Service Identification:** Initial confusion between legacy AWS IAM Identity Provider and the correct **AWS IAM Identity Center** service.
    
- **IdP SAML Metadata Handling:** AWS IAM Identity Center requires **uploading the `metadata.xml` file** directly, not a URL or just a certificate.
    
- **Lack of User/Group Synchronization:** SAML only handles authentication. **SCIM provisioning** is required to synchronize user and group identities from Okta into AWS IAM Identity Center.
    
- **Group Provisioning Mechanism:** AWS IAM Identity Center app in Okta uses a dedicated **"Push Groups" tab** for group synchronization, separate from general user provisioning settings.
    
- **AWS IAM Permission Set Selection:** The generic `ReadOnlyAccess` policy needed to be explicitly located and selected within the "AWS managed policies" section during permission set creation.

- **Duplicate identities:** Manually created users in AWS can collide with SCIM. Delete duplicates and let SCIM recreate them.

- **Token rotation:** If provisioning silently stops, **regenerate SCIM token** in AWS and update Okta.

---

## Notes & Related Work

* **Terraform (separate doc):** I manage Okta/AWS objects as code (remote state in **S3 + DynamoDB**), including permission-set/account assignments where practical.
* **SIEM:** Okta System Log → **Splunk Cloud** (covered in Observability).
* **Policies:** MFA, Adaptive, Zones, Device Assurance applied at Okta side (covered in Foundations/Policies).



