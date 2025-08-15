# Demonstrating Compliance Logging with Okta & Splunk

## I. ISO 27001: The Framework and Our Objective

**ISO/IEC 27001** provides the framework for an Information Security Management System (ISMS). The objective of this final lab phase is to show how our technical stack—**Okta** (workforce identity) and **Splunk Cloud** (centralized logging/SIEM)—produces **direct, auditable evidence** against specific ISO controls. Rather than staying conceptual, I built artifacts an auditor can actually review.

> Note: Control references below use ISO/IEC 27001:2013 Annex A numbering (e.g., A.9, A.12).

## II. The Thought Process: Linking IAM to Compliance

I mapped ISO controls that are closest to workforce IAM and security monitoring, then used Okta to **enforce policy** and Splunk to **evidence outcomes**:

1. **Identify Key Controls**: I needed to find ISO 27001 controls that are directly related to Identity and Access Management (IAM). I focused on controls related to access policy, user management, and event logging.
    
2. **Use Our Tools**: I then determined how our Okta and Splunk instances could satisfy these controls. For access policy, the Okta Admin Console was the perfect tool. For event logging and reporting, Splunk was the clear choice.
    
3. **Build the Evidence**: I created a single, centralized dashboard in Splunk that would contain all the necessary reports. This dashboard transforms raw log data into an auditable document, making it easy for an auditor to review our compliance posture.
    

## III. Policy Enforcement in Okta (ISO Control A.9.4.1)

To satisfy **ISO Control A.9.4.1 (Access Control Policy)**, which requires an organization to implement a formal policy to manage access to information and systems, I configured a stringent password policy. This policy ensures all users adhere to a minimum standard for credential security.

I configured the Password Policy as follows:

- **Password Complexity**:
    
    - Minimum length: 10 characters
        
    - Required characters: Lowercase, uppercase, number, and a symbol.
        
    - Other checks: Restrict common passwords and do not allow the username, first name, or last name.
<img width="797" height="911" alt="Screenshot 2025-08-13 131148" src="https://github.com/user-attachments/assets/58f658cb-78be-4f6f-8ddf-709b596e03e8" />
     
- **Password Aging**:
    
    - Password expires after: 90 days
        
    - Minimum password age: 1 day
        
    - Enforce password history for the last 4 passwords
        
- **Account Lockout**: Lock out users after 10 unsuccessful attempts.
<img width="783" height="474" alt="Screenshot 2025-08-13 131208" src="https://github.com/user-attachments/assets/4265bdc0-5d8f-4fa7-bce3-00d9573c83db" />
    

## IV. The Splunk Compliance Evidence Dashboard (ISO Control A.12.4.1)

To satisfy **ISO Control A.12.4.1 (Event Logging)**, which mandates the logging and monitoring of administrative actions and security events, I created a dedicated Splunk dashboard. This dashboard is a single pane of glass that provides a clear, auditable trail of all security-relevant activity.

The dashboard consists of three key reports, each built from the `sourcetype="OktaIM2:log"` data:

### **1. Admin Activity Log**

- **Purpose**: This report provides a complete, chronological log of all privileged actions. It is crucial for incident response and oversight of administrative changes.
    
- **Splunk Query (SPL)**:
    
    ```
    index=* sourcetype="OktaIM2:log" outcome.result=FAILURE
    | rename actor.alternateId as Admin, eventType as Action, client.ipAddress as SourceIP
    | table _time, Admin, Action, SourceIP
    | sort -_time
    ```
<img width="938" height="890" alt="image" src="https://github.com/user-attachments/assets/dc8380fa-13a6-4439-b7dc-a2725a88dbd2" />
<img width="548" height="368" alt="Screenshot 2025-08-13 134353" src="https://github.com/user-attachments/assets/7d905c20-5c2e-462c-8b0c-36fbeb9c2ec2" />
    
### **2. User Lifecycle Changes**

- **Purpose**: This report tracks all user creation and deactivation events, proving that I have a defined and auditable process for user registration and de-registration.
    
- **Splunk Query (SPL)**:
    
    ```
    index=* sourcetype="OktaIM2:log"
    | search (eventType="user.lifecycle.create" OR eventType="user.lifecycle.deactivate")
    | rename actor.alternateId as Initiator, target{}.alternateId as TargetUser, eventType as EventType
    | table _time, Initiator, TargetUser, EventType
    | sort -_time
    ```
    

### **3. Multi-Factor Authentication (MFA) Enrollment**

- **Purpose**: This report monitors the enrollment of MFA, providing evidence that the access control policies are being enforced and that users are successfully completing their security setups.
    
- **Splunk Query (SPL)**:
    
    ```
    index=* sourcetype="OktaIM2:log"
    | search eventType="user.mfa.factor.enroll" OR eventType="user.mfa.factor.activate"
    | rename actor.alternateId as User, outcome.reason as OutcomeReason, client.userAgent.os as UserOS
    | table _time, User, OutcomeReason, UserOS
    | sort -_time
    ```
<img width="1909" height="979" alt="Screenshot 2025-08-13 134623" src="https://github.com/user-attachments/assets/2cb66b1c-4040-499c-998b-8dd040d06f07" />
    
## V. Automating Compliance Reporting 📧

To complete the reporting process, I set up a scheduled export for the dashboard. This automates the evidence-gathering process, ensuring a consistent and auditable record is generated and delivered to stakeholders.

- **Schedule**: The dashboard is configured to run and generate a PDF export on a monthly basis.
    
- **Recipients**: The report is delivered via email to a designated recipient.
    
- **Benefit**: This automation transforms a manual process into a repeatable, efficient, and reliable part of My compliance program.
<img width="918" height="497" alt="image" src="https://github.com/user-attachments/assets/4c558e0c-3606-4a9f-ac88-c7e9107c3fea" />
<img width="802" height="762" alt="image" src="https://github.com/user-attachments/assets/893c68e9-8114-4395-912c-177b67ac86bf" />
<img width="786" height="752" alt="Screenshot 2025-08-13 135126" src="https://github.com/user-attachments/assets/f5edb4f0-cf36-4b2d-a5a4-f0d0df5aeafb" />
<img width="685" height="659" alt="Screenshot 2025-08-13 135324" src="https://github.com/user-attachments/assets/86265905-5d8c-4cde-a096-091a94f815ed" />

