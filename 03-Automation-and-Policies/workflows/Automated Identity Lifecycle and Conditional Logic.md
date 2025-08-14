# Okta Workflows — Automated Identity Lifecycle & Conditional Logic

> **Scope:** I built no-code/low-code **Okta Workflows** to automate Joiner/Mover/Leaver patterns, enforce conditional group logic, and improve auditability through notifications.

---
## I. Objective & Purpose

This lab demonstrates the use of **Okta Workflows** to build practical, no-code/low-code automations for key Identity and Access Management (IAM) scenarios. The primary objective is to showcase an understanding of automated identity lifecycle management (Joiner-Mover-Leaver) and the application of conditional logic to enforce governance at scale.

By creating these flows, I aim to:

- **Automate Manual Tasks:** Replace repetitive administrative actions with reliable, event-driven flows.
    
- **Enforce Governance:** Use conditional logic to ensure users are assigned to the correct groups based on their profile attributes.
    
- **Improve Auditability:** Provide a real-time audit trail for key lifecycle events through automated notifications.
    
- **Master Core Workflows Concepts:** Demonstrate proficiency with flow triggers, connectors, data mapping, and branching.
    

## II. Technical Thought Process & Evolution of Configuration

Implementing Workflows successfully required a deeper understanding of how the platform handles data and actions.

**Key Design Decisions:**

- **Joiner Flow:** An email notification was chosen as a simple, verifiable "Joiner" scenario.
    
- **Mover Flow:** Conditional group assignment was chosen as a "Mover" scenario to demonstrate branching logic.
    
- **Leaver Flow:** An email notification was chosen as a simple, verifiable "Leaver" scenario.
    

**Challenges Encountered & Resolutions:**
        
1. **Concatenating Text & Dynamic Pills:**
    
    - **Problem:** Dragging a dynamic attribute pill (e.g., `Display Name`) into a text field (e.g., email subject) would replace the entire static text.
        
    - **Root Cause:** The `Concatenate` card's input fields were designed to hold a single string of text, and a pill was treated as that string, replacing any existing text.
        
    - **Resolution:** Rebuilt the `Concatenate` cards to have a separate input field for **every single piece of static text and every dynamic pill**, and discovered that using **Shift + Enter** inside an input field for new lines was the correct method to format the email body professionally.
        
    - **Lesson:** Precise handling of data types and input fields is crucial. Use separate inputs for each piece of a concatenated string if necessary.
        
2. **Missing Functions:**
    
    - **Problem:** Key function cards like "Concatenate" and "Compose" were not immediately found, or the "Log" card was absent.
        
    - **Resolution:** Re-attempted searches with correct spelling (`Concatenate`) and adapted the flows to use available cards.
        
    - **Lesson:** Confirm card availability and exact naming before building.
        
        
3. **Data Type Mismatch & Incorrect Logic:**
    
    - **Problem:** In the advanced flow, the "Okta - Add User to Group" card was unable to accept a list of objects from the "Okta - Search Groups" card.
        
    - **Root Cause:** The `Add User to Group` card requires a single `Group ID` (a string), but I was incorrectly passing an entire group object. Additionally, the conditional logic was flawed.
        
    - **Resolution:** The flow was corrected to use an intermediary **"List - At"** card to get a single group object from the search results and then to explicitly use an **"Object - Get"** card to extract just the `ID` from that object. The `If/Else` condition was also corrected to check the `Count` of the search results, not the ID. The `Create Group` and `Add User to Group` cards were placed inside the "Else" branch to handle the "group not found" scenario.
        
    - **Lesson:** Data types must match between cards. Explicitly extract primitive values from objects or lists before passing them to other cards.
        

## III. Prerequisites

Before proceeding, ensure the following :

- **Okta Developer Account:** An active Okta organization with super administrator access.
    
- **Okta Workflows Console:** Access to the Okta Workflows Console.
    
- **Okta Test User(s) and Group(s):** An Okta test user (e.g., `Workflow Testuser`) and a test group (e.g., `Salesforce Sales Team`).
    
- **Okta Email Connection:** The built-in email connector is configured to use an administrator's email/password.
    

## IV. Configuration Steps: Okta Workflows

This section details the successful implementation of three key workflow scenarios and a final advanced flow.

### A. Workflow 1: Automated User Onboarding Email (Joiner)

**Objective:** When a new user is created in Okta, automatically send an email to `***@gmail.com` with the new user's details.

1. **Create a New Flow:**
    
    - **Flow Name:** `Automated User Onboarding Email`
        
    - **Event Card:** **"Okta - User Created"** (connected to `My Okta Org Connection`).
        <img width="807" height="614" alt="Screenshot 2025-07-31 193639" src="https://github.com/user-attachments/assets/2589f6fa-57fa-46d4-8f55-e591494e0206" />

2. **Add and Configure Read User and Email Cards:**
    
    - To the right of the event card, add an **"Okta - Read User"** card to get the user's full profile (connected to the `ID` from "Okta User Created").
        <img width="850" height="440" alt="Screenshot 2025-07-31 201102" src="https://github.com/user-attachments/assets/ea86d9b4-f28f-4e4e-8237-5a1b260196e8" />

    - Add a **"Concatenate"** card for the **Subject:**
        <img width="1761" height="481" alt="Screenshot 2025-07-31 201542" src="https://github.com/user-attachments/assets/91466cbc-17e5-4438-84ba-dd8c9d29c0c7" />

        - **Text 1:** `New Okta user created:`
            
        - **Text 2:** Drag `Display name` from "Okta - Read User".
            <img width="1237" height="899" alt="Screenshot 2025-07-31 203153" src="https://github.com/user-attachments/assets/c10e9765-c988-4178-83ad-bda468e89668" />

    - Add a **"Concatenate"** card for the **Body:**
        
        - Use multiple inputs for each line of static text and each attribute pill, using **Shift + Enter** to create new lines where needed.
          <img width="598" height="732" alt="Screenshot 2025-07-31 212026" src="https://github.com/user-attachments/assets/954c3c60-0dd9-4503-a6ba-82681d476089" />
          <img width="1237" height="899" alt="Screenshot 2025-07-31 203153" src="https://github.com/user-attachments/assets/9b006d90-93cb-4f64-917e-404326406664" />
            
    - Add a **"Send Email"** card:
        <img width="680" height="415" alt="Screenshot 2025-07-31 194156" src="https://github.com/user-attachments/assets/fc9b3639-aaf2-4df4-afd4-5a9f8d0215b8" />
        <img width="660" height="447" alt="Screenshot 2025-07-31 194234" src="https://github.com/user-attachments/assets/8dd6f731-75ee-41cf-b8be-758c4ae937f5" />
        <img width="636" height="614" alt="Screenshot 2025-07-31 194604" src="https://github.com/user-attachments/assets/cf97db5e-1315-40fe-afcd-26e493171c78" />
        <img width="507" height="584" alt="image" src="https://github.com/user-attachments/assets/116d9ad5-332a-4c93-a791-101e7aee31ed" />
        <img width="487" height="491" alt="image" src="https://github.com/user-attachments/assets/53aae411-fd35-4007-8632-d568d208da53" />

        - **To:** `h@gmail.com`
            
        - **From:** `mellonryon.com`
            
        - **Subject:** Drag the `output` from the Subject Concatenate card.
            
        - **Body:** Drag the `output` from the Body Concatenate card.
            
        - **Connection:** `Okta Email Connection`.
            <img width="1593" height="908" alt="Screenshot 2025-07-31 204106copy" src="https://github.com/user-attachments/assets/c6e2813e-9acd-487e-bad6-1d104ab35baf" />

3. **Save and Activate:**
    
    - Save the flow and turn it **ON**.
        
4. **Verification:** Created a new user in Okta and confirmed an email was sent successfully with correctly formatted details.
    <img width="697" height="680" alt="Screenshot 2025-07-31 204606" src="https://github.com/user-attachments/assets/7ab20014-0603-4f44-add9-5f8fb672d41e" />
    <img width="421" height="515" alt="image" src="https://github.com/user-attachments/assets/e3deecdf-07fc-41be-b9d5-eef5a30f03d4" />

**Flow Architecture**
<img width="592" height="147" alt="Screenshot 2025-07-31 213116" src="https://github.com/user-attachments/assets/d2afe6fd-1b54-4fc5-9b24-f14207b4dec0" />

### B. Workflow 2: Conditional Group Assignment (Mover)

**Objective:** When a user's profile is updated, automatically add them to the `Salesforce Sales Team` group if their `Department` is changed to "Sales".

1. **Create a New Flow:**
    
    - **Flow Name:** `Conditional Group Assignment`
        
    - **Event Card:** **"Okta - User Okta Profile Updated"** (connected to `My Okta Org Connection`).
        
2. **Add Logic and Actions:**
    
    - Add an **"Okta - Read User"** card to get the user's full profile (connected to the `ID` from "User Okta Profile Updated").
        
    - Add an **"If/Else"** card.
        <img width="1129" height="878" alt="Screenshot 2025-07-31 220418" src="https://github.com/user-attachments/assets/79b76123-b43c-486a-82d8-94b8d22c78b9" />

    - **Configure Condition:** `IF {{Okta Read User.Profile Properties.Department}} equals "Sales"`
        
    - **Inside the "If" branch:** Add an **"Okta - Add User to Group"** card.
        
        - **User ID:** Drag the `ID` from "Okta - Read User".
            
        - **Group ID:** Manually paste the Group ID of `Salesforce Sales Team` (found from the Okta Admin Console URL for the group).
            <img width="1915" height="802" alt="Screenshot 2025-07-31 222253" src="https://github.com/user-attachments/assets/95161f28-33aa-44fd-8620-2b4ef58c6b02" />

3. **Save and Activate:**
    
    - Save the flow and turn it **ON**.
        
4. **Verification:** Changed a test user's `Department` to "Sales" in Okta and confirmed they were automatically added to the `Salesforce Sales Team` group.
    <img width="1036" height="633" alt="Screenshot 2025-07-31 222405" src="https://github.com/user-attachments/assets/cbbe83bf-ffd9-4a75-aa5e-17bc80f5a4b0" />


### C. Workflow 3: Automated User Deprovisioning Notification (Leaver)

**Objective:** When a user is deactivated in Okta, automatically send an email notification to the IAM team.

1. **Create a New Flow:**
    
    - **Flow Name:** `Automated User Deprovisioning Notification`
        
    - **Event Card:** **"Okta - User Deactivated"** (connected to `My Okta Org Connection`).
        
2. **Add and Configure Email Cards:**
    
    - Add an **"Okta - Read User"** card (connected to the `ID` from "User Deactivated").
        
    - Add a **"Concatenate"** card for the **Subject:** `Okta User Deprovisioned: {{Okta Read User.Display Name}}`
        
    - Add a **"Concatenate"** card for the **Body:** Build a formatted message using static text and attributes (Name, Email, ID, etc.) from the "Okta - Read User" card, using **Shift + Enter** for new lines.
        
    - Add a **"Send Email"** card:
        
        - **To:** Administrator email.
            
        - **Subject:** Drag the subject from the Concatenate card.
            
        - **Body:** Drag the body from the Concatenate card.
            
        - **Connection:** `Okta Email Connection`.
            
3. **Save and Activate:**
    
    - Save the flow and turn it **ON**.
        <img width="1522" height="889" alt="image" src="https://github.com/user-attachments/assets/b7c0d16a-7d49-4ecc-ad46-a9d6b7157dfc" />

4. **Verification:** Deactivated a test user in Okta and confirmed an email notification was sent with the correct details.
    <img width="683" height="507" alt="image" src="https://github.com/user-attachments/assets/f17b2d1f-a2c8-4c79-9caf-24b2996c0be6" />

<img width="554" height="223" alt="Screenshot 2025-08-01 190036" src="https://github.com/user-attachments/assets/3206d58f-ac62-4e78-b0db-3dfc651a4c1a" />


### D. Workflow 4: Dynamic User Provisioning (Advanced Low-Code Flow)

**Objective:** This low-code flow dynamically creates a new user, checks if a group exists, creates the group if needed, and then adds the user.

1. **Create a New Flow:**
    
    - **Flow Name:** `Dynamic User Provisioning`
        
    - **Event Card:** **"Flow Control - Delegated Flow"** (with inputs for `firstName`, `lastName`, `email`, `groupName`).
        <img width="975" height="416" alt="Screenshot 2025-08-01 192008" src="https://github.com/user-attachments/assets/7b3cf064-29e3-4cce-b930-0614b870501a" />
         
2. **Add User Creation and Group Logic:**
    
    - Add an **"Okta - Create User"** card to the right.
        
        - **Configure:** Map `firstName`, `lastName`, `email` from the Delegated Flow. Set `Username` and `Primary email` as `email`.
          <img width="585" height="740" alt="Screenshot 2025-08-01 192911" src="https://github.com/user-attachments/assets/a3db032f-a75a-4535-9c16-18d1c2dc353e" />
  
    - Add an **"Okta - Search Groups"** card.
        <img width="297" height="368" alt="Screenshot 2025-08-01 193000" src="https://github.com/user-attachments/assets/4ffecc37-f87e-4fbc-a178-15cbfa12a8fa" />

        - **Configure:** Search for the `groupName` from the Delegated Flow.
          <img width="296" height="790" alt="Screenshot 2025-08-01 194140" src="https://github.com/user-attachments/assets/75f199f3-ca6a-40b3-82ea-6263f6d0455a" />
  
    - Add an **"If/Else"** card.
        
        - **Configure Condition:** `IF {{List At.item.id}} is not null`.
            
3. **Corrected Actions in "If" and "Else" Branches:**
   
    - **Inside the "If" branch (Group Exists):** Add an **"Okta - Add User to Group"** card.
        
        - **Configure:** User ID: `ID` from `Create User`. Group ID: `ID` .
      <img width="495" height="524" alt="Screenshot 2025-08-01 221019" src="https://github.com/user-attachments/assets/0846bbae-6a4c-4651-a011-b4150fe876b4" />

    - **Inside the "Else" branch (Group Does Not Exist):**
        
        - Add an **"Okta - Create Group"** card.
            
        - **Configure:** Name: `GroupName` from `Delegated Flow`.
            
        - Add an **"Okta - Add User to Group"** card.
            
        - **Configure:** User ID: `ID` from `Create User`. Group ID: `ID` from `Create Group`.
          <img width="620" height="497" alt="Screenshot 2025-08-01 221039" src="https://github.com/user-attachments/assets/bde2b7a8-3bd5-4b5f-9544-e9245319b03c" />

          <img width="1629" height="898" alt="Screenshot 2025-08-01 215932" src="https://github.com/user-attachments/assets/e5d0b4de-eb8f-4fde-8b66-b8daee92ab4d" />

4. **Save and Activate:**
    
    - Save the flow and turn it **ON**.
        
5. **Verification:** Ran the delegated flow with a new user and a non-existent group name. Confirmed the user was created, the group was created, and the user was added to the group.
    <img width="1624" height="649" alt="Screenshot 2025-08-01 203443" src="https://github.com/user-attachments/assets/11971857-83f4-4a0b-b481-9d87ccf0d87d" />
    <img width="546" height="595" alt="Screenshot 2025-08-01 203533" src="https://github.com/user-attachments/assets/aab2e415-4171-4a9a-ae58-209498ebaf57" />
    <img width="704" height="424" alt="Screenshot 2025-08-01 204807" src="https://github.com/user-attachments/assets/2cdf1e11-d928-41f1-a921-683648f71de8" />
    <img width="1687" height="912" alt="Screenshot 2025-08-01 205606" src="https://github.com/user-attachments/assets/188e29b0-56e2-4cbd-b994-7691e5eddea7" />
    <img width="977" height="517" alt="Screenshot 2025-08-01 220257" src="https://github.com/user-attachments/assets/6f208e5a-a83f-4087-97e2-d80b87bd9fef" />


<img width="794" height="384" alt="Screenshot 2025-08-01 220001" src="https://github.com/user-attachments/assets/6a98c3fc-a80e-4305-b206-29cf6253bcab" />


## V. Advanced Low-Code Flow Analysis

The advanced flow demonstrates a powerful "check and create" pattern, which is crucial for building resilient automations. By creating this flow, we showcase an understanding of:

- **Resilient Logic:** The `If/Else` block prevents flow failure if the group already exists.
    
- **Dynamic Resource Creation:** The flow can create groups on the fly based on a user's needs.
    
- **Efficient Process:** This low-code flow eliminates multiple manual steps for an admin, enforcing security and consistency at scale.
    

## VI. Lessons Learned

- **Concatenating Text:** Using the **Shift + Enter** key inside an input field for line breaks is the correct method for formatting professional emails.
    
- **Data Mapping:** Explicitly extract primitive values (e.g., `ID`, `Name`) from objects or lists before passing them to other cards to avoid data type mismatch errors.
    
- **Permissions:** Administrative actions within flows (e.g., creating groups, reading user details) require a Workflows connection with sufficient permissions. The specific `okta.groups.manage` scope was required and granted for the `Okta Workflows Connection` app.

## VII. What’s Next (separate notes)

* **Workflows → AWS Lambda + S3** for folder creation (attribute-driven) and **Daily Deprovision Audit** via scheduled flow and email.
* **Terraform (IaC)** for Okta/AWS with **S3 + DynamoDB** backend and **Git CI/CD**.
