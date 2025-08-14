# 01 — Okta Foundations

*Developer account setup, branding, user import, groups & automated assignments*

> **Scope:** This is my lab (not production). I set up a free Okta Developer org as the identity hub, customized branding and emails, created test users, imported a bulk CSV (\~160 users), built groups and automated group rules. These steps lay the groundwork for app integrations, AWS federation, policies, and observability I’ll cover later.

---

## 1) Okta Developer Account Creation

### Purpose

Establish a free **Okta Developer Organization** (Org) to serve as the central **Identity Provider (IdP)** for my lab. This provides the platform for users, apps, and security policies.

### Steps Performed
1.  Navigated to `developer.okta.com`.
2.  Clicked on the "Sign Up" button to initiate the registration process.
3.  Provided personal details (First Name, Last Name, Email, Country) and agreed to the terms.
4.  Verified the account via the link sent to the registered email address.
5.  Set a secure password and a security question for the Okta administrator account.
6.  Successfully logged into the Okta Admin Console.


### Key information I recorded

* **Okta Org URL:** `https://dev-xxxxxxx.okta.com` *(placeholder—redact before publishing)*
* **Admin Email:** `<your_admin_email@domain>` *(redact)*

---

## 2) Okta Tenant Customization: Branding & User Experience

### Purpose

Present a consistent, professional user experience on the **sign-in page**, **end-user portal**, and **emails**. Clear branding improves user trust and reduces phishing risk.

### Technical thought process

A branded and professional login experience builds **user trust**, which is a key control for preventing phishing attacks. It also demonstrates a mature IAM deployment and a deeper understanding of the platform beyond its core technical functions.

### Steps Performed

1. **Customized the Theme**:
    
    - Navigated to **"Customization" > "Branding" > "Theme"**.
        
    - Uploaded a company logo and favicon.

        <img width="861" height="785" alt="Screenshot 2025-08-09 203347" src="https://github.com/user-attachments/assets/eb1ea427-d30d-4b2a-beee-b5c7d88219b8" />

    - Customized the color palette to match a corporate brand guide.
        
2. **Customized Emails**:
    
    - Navigated to **"Customization" > "Branding" > "Emails"**.
        
    - Customized a default email template (e.g., "Welcome Email") to include the company's logo. This provides a consistent and professional look for all user-facing communications.

<img width="537" height="732" alt="Screenshot 2025-08-09 205038" src="https://github.com/user-attachments/assets/6f58301e-092c-4481-8d3a-3c46441e713b" />

**User Sing-in Portal **

* Verified the **sign-in** portal reflects the theme.

<img width="951" height="877" alt="Screenshot 2025-08-09 204828" src="https://github.com/user-attachments/assets/28e4519e-46ed-4548-86d5-86efd6b7a81e" />

### Expected outcome

The customized theme and branding were successfully applied to the Okta sign-in page, the end-user dashboard, and all user-facing emails. The final outcome is a professional, branded, and user-friendly experience that aligns with the project's overall goal of building an enterprise-grade IAM solution.
---

## 3) Manual Test User Creation

### Purpose

To create a basic test user account directly within the Okta Universal Directory. This user will be used to test initial application integrations and authentication flows.

### Steps I performed

1.  From the Okta Admin Console, navigated to **"Directory" > "People"**.
2.  Clicked the green **"Add Person"** button.
3.  Filled in the following details:
    * First Name: `Test`
    * Last Name: `User`
    * Primary email: `test.user@yourdomain.com` (using a placeholder for lab purposes)
    * Username: `test.user`
    * Password: Set a static password (e.g., `Password123!`) and confirmed it.
    * Unchecked "User must change password on first login" for simpler lab testing.
    * Unchecked "Send user an activation email."
4.  Clicked **"Save"**.

### Expected Outcome
A new user, `Test User` with username `test.user`, was successfully created and activated in the Okta Universal Directory. This user is now ready to be assigned to applications.
**People (sample view)**
!\[People list]\(sandbox:/mnt/data/Screenshot 2025-07-12 124942.png)

> **Redact:** names/emails.

---

## 4) Bulk User Import (CSV)

### Purpose

To efficiently populate the Okta Universal Directory with a large number of user identities from a Human Resources (HR) data source (simulated via CSV-Chat GPT), avoiding manual creation. This step is critical for scalability and preparing for automated provisioning workflows.

### Technical Thought Process
* **CSV Import:** Utilized Okta's built-in CSV import functionality for initial bulk user onboarding. While SCIM from BambooHR is the long-term goal, CSV import is a practical first step for lab environments or one-time data migrations.
* **Data Preparation:** Ensured the CSV file (*****`filename.csv`*****) contained necessary user attributes (e.g., first name, last name, email, username, and critically, a `usertype` attribute for group assignments).

### Steps Performed
1.  Prepared the csv file with 160 user entries, including a `usertype` column for each user (e.g., 'Employee', 'Service Principal', 'Guest').
2.  From the Okta Admin Console, navigated to **"Directory" > "People"**.
3.  Clicked the **"More Actions"** dropdown button and selected **"Import from CSV"**.
4.  Uploaded the `okta_final_bulk_users.csv` file.
5.  Mapped the CSV columns to corresponding Okta user profile attributes (e.g., `first name` to Okta `firstName`, `last name` to Okta `lastName`, `usertype` to Okta `usertype` custom attribute if created, or a relevant standard attribute).
6.  Initiated the import process and confirmed the creation of **160** new user accounts in the Okta Universal Directory.
7.  Resolved any potential import errors or conflicts, if they arose (none observed for this import).

### Expected Outcome
160 new user profiles were successfully created and populated in Okta, making them available for group assignments and application access.

---

## 5) Okta Group Creation

### Purpose

To establish logical groupings of users within Okta based on their roles and access requirements. Groups simplify access management by allowing permissions to be assigned to a group rather than individual users, enhancing scalability and manageability.

### Technical Thought Process
* **Role-Based Access Control (RBAC) Foundation:** Creating groups like 'Employee', 'Service Principal', and 'Guest' lays the groundwork for an RBAC model, where access policies are tied to group membership.
* **Future Automation:** These groups will be targets for both manual assignments and automated assignments via Okta Group Rules and later, potentially, SCIM provisioning from BambooHR.

### Steps Performed
1.  From the Okta Admin Console, navigated to **"Directory" > "Groups"**.
2.  Clicked the green **"Add Group"** button for each group.
3.  Created the following three groups with a descriptive name and description:
    * **Group Name:** `Employee Group`
        * Description: `Contains all standard employees.`
    * **Group Name:** `Service Principal Group`
        * Description: `Contains non-human accounts and service identities.`
    * **Group Name:** `Guest Group`
        * Description: `Contains external users or temporary guests.`
4.  Clicked **"Add Group"** for each.

### Expected Outcome
Three new, empty Okta groups were created, ready to have users assigned to them.
---

## 6) Group Rules for Automated Membership

### Purpose

To automate the assignment of users to specific Okta groups based on their attributes. This ensures consistent, dynamic, and scalable group membership management, reducing manual effort and potential errors.

### Technical Thought Process
* **Attribute-Based Grouping:** Leveraging the `usertype` attribute (imported with the bulk users) allows for dynamic group membership. When a user's `usertype` changes, their group membership automatically adjusts.
* **Efficiency and Compliance:** Automating group assignment improves operational efficiency and helps maintain compliance by ensuring users are only in the groups appropriate for their current role or status.
* **Rule Order/Exclusivity:** Considered if any users might fit multiple rules and ensured rules are distinct or ordered appropriately if overlaps were possible (in this case, `usertype` is assumed to be mutually exclusive).

### Steps Performed
1.  From the Okta Admin Console, navigated to **"Directory" > "Groups"**.
2.  Clicked on the **"Rules"** tab.
3.  Clicked the green **"Add Rule"** button for each rule.
4.  Configured the following group rules:

    * **Rule 1: Employee Group Assignment**
        * **Rule Name:** `Assign Employees to Employee Group`
        * **If user attribute `usertype` equals `Employee`** (or relevant attribute and value from your CSV)
        * **Assign to Groups:** `Employee Group`
        * Clicked **"Create Rule"**.

    * **Rule 2: Service Principal Group Assignment**
        * **Rule Name:** `Assign Service Principals to Service Principal Group`
        * **If user attribute `usertype` equals `ServicePrincipal`** (or relevant attribute and value from your CSV)
        * **Assign to Groups:** `Service Principal Group`
        * Clicked **"Create Rule"**.

    * **Rule 3: Guest Group Assignment**
        * **Rule Name:** `Assign Guests to Guest Group`
        * **If user attribute `usertype` equals `Guest`** (or relevant attribute and value from your CSV)
        * **Assign to Groups:** `Guest Group`
        * Clicked **"Create Rule"**.
5.  After creating each rule, clicked the **"Activate"** button for each rule to make it effective. (Alternatively, you can activate all rules at once if prompted after creation).
6.  Verified that users were automatically assigned to their respective groups by checking the "People" tab within each group or by viewing individual user profiles.

### Expected Outcome
Users imported from the CSV were automatically assigned to the `Employee Group`, `Service Principal Group`, or `Guest Group` based on their `usertype` attribute, demonstrating successful automation of group membership.
---

