# Salesforce — SAML SSO + SCIM Provisioning (Okta → Salesforce)

## I. Introduction & Purpose

This document details the configuration and demonstration of **SCIM (System for Cross-domain Identity Management) provisioning from Okta to Salesforce**. The primary goal is to automate the user lifecycle management (Joiner-Mover-Leaver) for Salesforce users, with Okta acting as the authoritative Identity Provider (IdP). This integration enhances security, improves operational efficiency, and ensures data consistency across both platforms.

By implementing SCIM provisioning, we achieve:

- **Automated User Creation:** New users in Okta are automatically provisioned to Salesforce.
    
- **Attribute Synchronization:** Changes to user profiles in Okta are automatically updated in Salesforce.
    
- **Automated Deprovisioning:** Users deactivated or unassigned in Okta are automatically deprovisioned (made inactive) in Salesforce, reducing orphaned accounts and security risks.
    
- **Centralized User Management:** Simplifies administration by managing users primarily from Okta.

## III. Prerequisites

Before proceeding, ensure you have the following in place:

- **Okta Developer Account:** Your Okta organization is active and you have administrator access.
    
- **Salesforce Developer Edition Account:** Your free Salesforce Developer Edition is active, and you can log in as an administrator. Your "My Domain" should be configured and active (e.g., `yourlabname.my.salesforce.com`).
    
- **Salesforce Administrator User:** A dedicated Salesforce user (e.g., `Joshua Dominguez`) with a custom profile (`Okta SCIM Admin Profile`) that has **`API Enabled`** and **`Manage Users`** permissions enabled.
    
- **Okta Test User(s) and Group(s):** At least one Okta test user (e.g., `Frank Gonzalez`) and a group (e.g., `Lab users`) assigned to them. These users should _not_ already exist in Salesforce for a clean provisioning test.
    
- **Network Connectivity:** Ensure your Okta instance can communicate with Salesforce.
    

## IV. Configuration Steps

We will configure Salesforce first, then Okta, and finally assign users.

### A. Salesforce Preparation: My Domain, Custom Profile, and Connected App

This section prepares your Salesforce instance for Okta to connect and provision users.

1. **Enable My Domain:**
    
    - Log in to your Salesforce Developer Edition.
        
    - Go to **Setup** (gear icon) > **"Setup"**.
        
    - In "Quick Find", type `My Domain` and click **"My Domain"**.
        
    - Choose and register a unique domain name (e.g., `yourlabname`).
  
<img width="949" height="906" alt="Screenshot 2025-07-16 225247" src="https://github.com/user-attachments/assets/27584585-7a4f-47a8-a788-281b7b3b1207" />
        
<img width="781" height="767" alt="Screenshot 2025-07-16 225424" src="https://github.com/user-attachments/assets/2be8272f-7bed-43c6-a8e8-9f283939de58" />
        

  - Once ready, click **"Deploy to Users"**.
        
    - _Note: Your Salesforce URL will change to `https://yourlabname.my.salesforce.com`._
        
2. **Create or Edit a Custom User Profile for SCIM Admin:**
    
    - This profile ensures the Salesforce user Okta authenticates with has the necessary permissions.
        
    - Log in to your Salesforce Developer Edition.
        
    - Go to **Setup** > **"Setup"**.
        
    - In "Quick Find", type `Profiles` and click **"Profiles"**.

        <img width="950" height="771" alt="Screenshot 2025-07-19 121326" src="https://github.com/user-attachments/assets/b72a12d9-736e-4a2d-b13d-14d294624c67" />

    - Find **"System Administrator"** and click **"Clone"** next to it.
    <img width="923" height="883" alt="Screenshot 2025-07-19 121342" src="https://github.com/user-attachments/assets/1b83362a-db5f-4880-9669-3c08f18a3799" />

    - **Profile Name:** Enter `Okta SCIM Admin Profile`. Click **"Save"**.
        
    - On the new profile's detail page, click **"Edit"**.
        
    - Scroll down to **"Administrative Permissions"**.
        
    - Ensure **`API Enabled`** and **`Manage Users`** are **checked**.
        
    - Click **"Save"**.
        
    - _(Confirmation: It was verified that the default System Administrator profile already has these permissions, so creating a new profile and assigning it is best practice but not strictly required if using the main System Admin user directly for the lab.)_
        
3. **Assign the Custom Profile to a Dedicated Admin User:**
    
    - Log in to your Salesforce Developer Edition.
        
    - Go to **Setup** > **"Setup"**.
        
    - In "Quick Find", type `Users` and click **"Users"**.
        
    - Find or create a dedicated Salesforce administrator user.
<img width="656" height="701" alt="Screenshot 2025-07-19 122840 copy" src="https://github.com/user-attachments/assets/9cbe8456-1d2a-4ba5-9955-8dfdb98248b0" />
        
    - Click **"Edit"** next to the user's name.
        
    - Locate the **"Profile"** field (which is a **link** displaying the current profile, e.g., "System Administrator").
        
    - Click on the **"Profile" link**. This will take you to the profile's definition page.
        
4. **Create a Salesforce Connected App (Crucial for Okta SCIM Connection):**
    
    - This is the application in Salesforce that Okta will use to authenticate and provision.
        
    - Log in to your Salesforce Developer Edition.
        
    - Go to **Setup** > **"Setup"**.
        
    - In "Quick Find", type `App Manager` and click **"App Manager"**.
        <img width="935" height="898" alt="Screenshot 2025-07-16 230505" src="https://github.com/user-attachments/assets/ed1c0014-9c1a-42db-8b62-a575dc0e4a81" />

    - On the "App Manager" page, click the **"New Connected App"** button.
        
    - **Basic Information:**
        
        - **Connected App Name:** `Okta SCIM Provisioning2` .
            <img width="687" height="710" alt="Screenshot 2025-07-19 165457" src="https://github.com/user-attachments/assets/be8bb806-be57-43d6-ac61-c95befac2231" />

        - **API Name:** `Okta_SCIM_Provisioning_2` (auto-populates).
            
        - **Contact Email:** Your email address.
            
    - **API (Enable OAuth Settings):**
        
        - Check **"Enable OAuth Settings"**.
            
        - **Callback URL:** Enter the **exact literal URL** provided by Okta: `https://system-admin.okta.com/admin/app/generic/oauth20redirect`
            
        - **Selected OAuth Scopes:** Move these two to "Selected OAuth Scopes":
            
            - `Manage user data via APIs (api)`
                
            - `Perform requests at any time (refresh_token, offline_access)`
             <img width="664" height="263" alt="Screenshot 2025-07-19 165959" src="https://github.com/user-attachments/assets/415f0560-3d4c-4f58-b09e-54ffdc3799c7" />


        - **Flow Enablement:**
            
            - Check **"Enable Authorization Code and Credentials Flow"**.
                
            - Leave all other flow checkboxes **UNCHECKED**.
                
        - **Security:**
            
            - Check **"Require secret for Web Server Flow"**.
                
            - Check **"Require secret for Refresh Token Flow"**.
                
            - **UNCHECK** **"Require Proof Key for Code Exchange (PKCE) Extension for Supported Authorization Flows"** (as per Okta doc).
             <img width="309" height="135" alt="Screenshot 2025-07-19 170042" src="https://github.com/user-attachments/assets/3a21c819-9c45-4f06-8721-9bab815f22f6" />
   
            - Leave other security checkboxes **UNCHECKED**.
                
    - **Save the Connected App:** Click **"Save"**.
        
    - **Note Down Consumer Key and Consumer Secret:** On the "Connected App Detail" page, find "API (Enable OAuth Settings)". Note the **"Consumer Key"** and **"Consumer Secret"** (click "Click to reveal" for the secret). **Save these securely!**
        
5. **Configure OAuth Policies for the Connected App:**
    
    - On the "Connected App Detail" page (after saving), click **"Manage"**.
        
    - Under **"OAuth Policies"**:
        
        - **Permitted Users:** Change to **"All users may self-authorize"**.
            
        - **Refresh Token Policy:** Set to **"Refresh token is valid until revoked"**.
            
    - Click **"Save"**.
        
    - **Allow 5-10 minutes** for Salesforce changes to take effect.
        <img width="666" height="146" alt="Screenshot 2025-07-19 170231" src="https://github.com/user-attachments/assets/ab88d4a1-aa86-4985-a0c8-21402fa93d16" />


### B. Okta Configuration: Add Salesforce App and Configure Provisioning

This section configures the Salesforce application in Okta and establishes the SCIM connection.

1. **Add the Salesforce.com Application to Okta:**
    
    - Log in to your Okta Admin Console.
        
    - Go to **Applications** > **Applications**.
        
    - Click **"Browse App Catalog"**.
        
    - Search for **"Salesforce.com"** and click **"Add Integration"**.
        
    - **General Settings:**
        
        - **Application label:** "Salesforce.com" (or "Salesforce Lab SCIM").
            
        - **Instance Type:** Select **"Production"** (as your Developer Edition behaves like Production for API access).
<img width="589" height="593" alt="Screenshot 2025-07-19 123809" src="https://github.com/user-attachments/assets/091f6839-20a8-4149-9f2b-22b475fa7ee0" />

            
        - **Custom Domain:** Enter your Salesforce "My Domain" name (e.g., `yourlabname` or `mellonryon`).
            
        - Click **"Done"**.
            
2. **Configure SAML SSO (Prerequisite for Provisioning):**
    
    - On the Salesforce application page in Okta, click the **"Sign On"** tab.
        
    - Under "Settings", click **"Edit"**.
        
    - Ensure **"SAML 2.0"** is selected as "Sign on method".
        
    - Click **"View SAML Setup Instructions"** (or similar) to get Okta's SAML metadata (Identity Provider Single Sign-On URL, Identity Provider Issuer, X.509 Certificate).
        
    - **In Salesforce:** Go to **Setup** > **Single Sign-On Settings**. Click **"New"**.
        
        - Fill in details using Okta's SAML metadata.
            <img width="921" height="817" alt="image" src="https://github.com/user-attachments/assets/8dd39665-72c4-47a2-8c90-1697ca7897ac" />

        - Save.
            
        - Note Salesforce's Entity ID, ACS URL, and Salesforce Login URL.
            
    - **Back in Okta:** On the "Sign On" tab, fill in Salesforce's Entity ID and ACS URL.
        
    - **Test SSO:** Assign an Okta user to Salesforce, create a matching user in Salesforce, and test logging in from the Okta dashboard. (This was confirmed successful).
        
3. **Configure Provisioning Tab (Okta to Salesforce SCIM Connection):**
    
    - On the Salesforce application page in Okta, click the **"Provisioning"** tab.
        
    - Click **"Configure API Integration"**.
        
    - Check **"Enable API Integration"**.
        
    - **Authentication Mode:** Select **"OAuth 2.0"**.
        
    - **Salesforce Environment Type:** Confirm **"Developer Edition"** (if available, otherwise "Production").
        
    - **Salesforce Instance URL:** Your Salesforce "My Domain" URL (e.g., `https://yourlabname.my.salesforce.com`).
        
    - **Authorization Server:** Leave as "Default".
        
    - **OAuth Consumer Key:** Paste the **Consumer Key** from your Salesforce Connected App.
        
    - **OAuth Consumer Secret:** Paste the **Consumer Secret** from your Salesforce Connected App.
        
    - **Click "Authenticate with Salesforce.com" (Crucial Step):** This initiates the OAuth flow. Log in to Salesforce as your dedicated admin user (`Joshua Dominguez`) and grant access.
        
    - **Click "Test API Credentials":** This should now be successful.
        
    - Click **"Save"**.
       <img width="623" height="544" alt="Screenshot 2025-07-19 170304" src="https://github.com/user-attachments/assets/2cd42ad1-9a3d-4a60-952f-c3e6fc63b0b1" />


4. **Configure Provisioning Features ("To App"):**
    
    - On the "Provisioning" tab, on the left, click **"To App"**.
        
    - Click **"Edit"**.
        
    - Check **"Create Users"**, **"Update User Attributes"**, **"Deactivate Users"**.
        
    - Leave "Sync Password" **UNCHECKED**.
        
    - Click **"Save"**.

        <img width="625" height="801" alt="Screenshot 2025-07-19 170537" src="https://github.com/user-attachments/assets/23d1ab74-7585-46b4-b625-43c29a910342" />

5. **Map User Attributes ("To App"):**
    
    - On the "Provisioning" tab, under "To App", scroll to **"Attribute Mappings"**.
        
    - Click **"Edit"**.
        
    - Map common attributes (e.g., `firstName` -> `firstName`, `lastName` -> `lastName`, `email` -> `email`, `mobilePhone` -> `phone`, `department` -> `department`, `title` -> `title`, `managerId` -> `managerId`).
        
    - Click **"Save"**.

<img width="933" height="887" alt="Screenshot 2025-07-19 172412" src="https://github.com/user-attachments/assets/fb7b6b51-c3eb-47d9-a948-18350a2e08c9" />

<img width="895" height="897" alt="image" src="https://github.com/user-attachments/assets/7edc7048-0418-4b12-9e3d-526a13d625bf" />

### C. Assign Users/Groups for Provisioning in Okta

This step tells Okta who to provision to Salesforce.

1. **Go to the "Assignments" Tab:**
    
    - On the Salesforce application page in Okta, click the **"Assignments"** tab.
        
2. **Assign Groups:**
    
    - Click **"Assign"** > **"Assign to Groups"**.
        
    - Select your **`Lab users`** group and click **"Assign"**.
        
    - In the pop-up, for "Profile", select **"Standard User"**. Leave "Role" and "Permission Sets" unmapped/unchecked.
        
    - Click **"Save and Go Back"**.
        
    - Click **"Done"**.
        

## V. Testing and Validation: End-to-End User Lifecycle (Joiner-Mover-Leaver)

This demonstrates the full automated user lifecycle management.

1. **Joiner Scenario (User Creation):**
    
    - **In Bamboo HR:** Create a **new test user** (e.g., `Frank Gonzalez`). Confirm provisioning into Okta with all correct Attribute.
        <img width="803" height="655" alt="Screenshot 2025-07-19 175855" src="https://github.com/user-attachments/assets/054e8de3-1061-46ab-b716-d48f2bf5cb3e" />

    - Assign this new user to the **`Lab users`** group in Okta.
        
    - **In Salesforce:** Log in as admin. Go to **Setup** > **Users** > **Users**.
        
    - **Verify:** The new user should be created and **Active** in Salesforce, with correctly mapped attributes and the "Standard User" profile.
        <img width="688" height="562" alt="Screenshot 2025-07-19 173908" src="https://github.com/user-attachments/assets/819bc67f-fb67-47de-a61c-c0aaf7984b71" />

<img width="695" height="705" alt="Screenshot 2025-07-19 174104" src="https://github.com/user-attachments/assets/72c49430-304e-4c73-baa7-a672bf090425" />

2. **Mover Scenario (Attribute Update):**
    
    - **In Okta:** Go to the profile of your test user (e.g., `Frank Gonzalez`).
        
    - Go to the **"Profile"** tab and click **"Edit"**.
        
    - Change an attribute (e.g., **"Title"** to `Senior Network Administrator`).
        
    - Click **"Save"**. confirm App assignment removed in okta
        <img width="634" height="859" alt="Screenshot 2025-07-19 180058" src="https://github.com/user-attachments/assets/de5f6e46-5491-4ea6-a8d6-c0bc725db48c" />

    - **In Salesforce:** Go to the test user's profile. Refresh the page.
        
    - **Verify:** The "Title" (or updated attribute) should now reflect the change from Okta.
        
3. **Leaver Scenario (User Deprovisioning):**
    
    - **In Okta:** Go to **Directory** > **Groups**. Find the **`Lab users`** group.
        
    - Go to the **"People"** tab within the group.
        
    - Find your test user (e.g., `Frank Gonzalez`) and click the **"X"** icon next to their name to remove them from the group. Confirm removal.
        
    - **In Salesforce:** Go to **Setup** > **Users** > **Users**. Find your test user.
        
    - **Verify:** The user should now be **Inactive** (Active checkbox unchecked) in Salesforce, confirming successful deprovisioning.
        <img width="689" height="573" alt="Screenshot 2025-07-19 180602" src="https://github.com/user-attachments/assets/58c1154d-f7f1-4387-ba41-6420b7ce5f68" />

    - Even though user is visible under all users, he is not visible under active users:
*Salesforce doesn't typically "delete" users immediately when deprovisioned via SCIM; instead, it marks them as inactive. This preserves historical data and audit trails.*
 <img width="691" height="460" alt="Screenshot 2025-07-19 180704" src="https://github.com/user-attachments/assets/0532f5b7-960d-43a6-8da6-c1a8466b9570" />

## VI. Testing SSO
 - Login to assigned user dashboard
<img width="955" height="681" alt="Screenshot 2025-07-19 130145" src="https://github.com/user-attachments/assets/c6f78be1-768e-47fd-9a93-57f1db0b3dca" />
        
- You need okta browser plugin to launch IDP initiated flow:
        <img width="736" height="333" alt="Screenshot 2025-07-19 120745" src="https://github.com/user-attachments/assets/7d8a58b6-9de7-46b1-b9c7-6d02b65d7de5" />

<img width="932" height="897" alt="Screenshot 2025-07-19 120629" src="https://github.com/user-attachments/assets/1c3874d3-f128-4a18-b367-7dcff4b1f00d" />

- Sigin in to salesforce
<img width="958" height="862" alt="Screenshot 2025-07-19 121020" src="https://github.com/user-attachments/assets/963205c0-147b-4188-97e6-1f93dc38ef43" />

<img width="923" height="574" alt="Screenshot 2025-07-19 130206" src="https://github.com/user-attachments/assets/4188c753-7463-41b6-95c4-2edbaeab7b91" />


## VII. Troubleshooting & Lessons Learned

This section highlights the key challenges encountered and their resolutions, providing valuable insights for future integrations.

- **Salesforce My Domain Login Issue:**
    
    - **Problem:** Unable to log in via custom domain after activation.
        
    - **Resolution:** Cleared browser cache/cookies, used incognito mode.
        
    - **Lesson:** Browser caching can interfere with domain changes.
        
- **Persistent "Could not verify Salesforce administrator credentials" Error during Provisioning Setup:**
    
    - **Problem:** Okta consistently failed to authenticate with Salesforce for provisioning, despite correct Consumer Key/Secret.
            
    - **Root Cause : Exact Callback URL Mismatch:** The Callback URL configured in Salesforce was not the precise literal URL expected by Okta's Salesforce app template.
        
        - **Problematic URL:** `https://trial-5828141.okta.com/oauth2/v1/authorize/callback` (my previous suggestion).
            
        - **Correct Literal URL:** `https://system-admin.okta.com/admin/app/generic/oauth20redirect` (from Okta documentation).
            
        - **Resolution:** Updated the Connected App's Callback URL in Salesforce to the exact `https://system-admin.okta.com/admin/app/generic/oauth20redirect`'
            
    - **Lesson:** OAuth integrations are highly sensitive to exact URL matches, precise scope definitions, and specific security settings. Always adhere rigorously to vendor documentation.
        
- **Group Assignment vs. Individual Unassignment:**
    
    - **Problem:** Unable to unassign an application from an individual user if they received it via group assignment.
        
    - **Resolution:** To deprovision a user assigned via a group, remove the user from the group in Okta.
        
    - **Lesson:** Group-based assignments simplify management but require group-level actions for deprovisioning.
