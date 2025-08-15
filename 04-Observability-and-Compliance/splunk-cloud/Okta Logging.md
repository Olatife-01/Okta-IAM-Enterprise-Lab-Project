# Centralized Logging — Okta to Splunk Cloud

## I. Objective & Purpose

This lab details the integration of **Okta System Logs** with **Splunk Cloud** for centralized auditing and security monitoring. The goal is to provide comprehensive visibility into identity activity across the Okta organization—an essential control for security operations, compliance (ISO 27001, SOX), and forensic investigations.

Centralizing Okta logs in Splunk enables:

- **Unified Visibility:** Aggregate all Okta events in a single platform for easy searching and analysis.
    
- **Real-time Monitoring & Alerting:** Near real-time ingestion of events enables immediate detection of suspicious activities.
    
- **Compliance & Audit Trails:** Maintain a comprehensive and immutable record of all identity-related actions for regulatory compliance and internal audits.
    
- **Contextual Analysis:** Correlates Okta events with data from other security tools and infrastructure logs within Splunk.
    
- **Historical Data Collection:** Ability to ingest past Okta logs for retrospective analysis.

This phase advances my IAM lab from foundational setup to a **live, cross-cloud** integration: Okta as the identity source and Splunk Cloud as the SIEM for proactive monitoring.

## II. Technical Thought Process & Evolution of Configuration

In an enterprise setting, **identity telemetry is a primary security signal**—it records who authenticated, what changed, and where access was granted or denied. The solution had to be reliable, support backfill, and use least privilege. I began with Okta’s native **Log Streaming (push)** to Splunk HEC for simplicity, but persistent “**deactivated by system**” errors and an empty Splunk index indicated an upstream integration fault I couldn’t remediate from the tenant side.

To deliver a dependable pipeline, I pivoted to the **Splunk Add-on for Okta Identity Cloud (pull)**. This approach uses Okta’s REST APIs and an admin-scoped **API token**, avoids HEC fragility, and provides **checkpointing** for historical ingestion. During setup, I validated domain and token scoping, then tuned inputs to collect **System Log** events first. Field discovery in raw events clarified the add-on’s mapping (e.g., `eventType`, `outcome.result`, `actor.*`, `client.*`) and confirmed the default **sourcetype** as `okta:identity:cloud` in the **`main`** index.

To backfill, I reset the input checkpoint and specified an explicit **Start Date**. From there, I iterated SPL searches from broad (`index=main sourcetype=okta:identity:cloud`) to targeted panels and alerts, verifying each with controlled test events (login success/failure, user lifecycle actions). The end result is a stable, auditable ingestion path with queries and alerts mapped to the fields the add-on actually emits.

## III. Prerequisites

Before proceeding, ensure the have the following in place:

- **Okta Administrator Access:** Right admin privileges in Okta organization.
    
- **Okta API Token:** An Okta API token with "Read-only Administrator" permissions (or equivalent) to read users, groups, applications, and the System Log.
    
    - **How to create an Okta API Token:**
        
        1. Log in to the Okta Admin Console.
            
        2. In the left-hand navigation, go to **Security** > **API**.
            
        3. Click on the **Tokens** tab.
            
        4. Click **"Create Token"**.
            
        5. **Name:** `Splunk_API_Token` (or similar).
            
        6. Click **"Create Token"**.
            
        7. **IMMEDIATELY copy this token!** Save it securely.
            
- **Splunk Cloud Instance:** An active Splunk Cloud instance.
    
- **Splunk Cloud Administrator Access:** Administrator access  Splunk Cloud environment.
    
- **Network Connectivity:** Ensure Splunk Cloud instance can reach Okta's API endpoints over HTTPS (port 443).
    

## IV. Configuration Steps: Splunk Add-on for Okta Identity Cloud (Pull Method)

This section details the successful configuration of the Splunk Add-on to pull data from Okta.

### A. Install the "Splunk Add-on for Okta Identity Cloud" in Splunk Cloud

1. **Log in to your Splunk Cloud Instance:**
    
    - Open your web browser and go to your Splunk Cloud URL (e.g., `https://prd-p-s76qb.splunkcloud.com`).
        
    - Log in with your administrator credentials.
        
2. **Navigate to Apps:**
    
    - Click on **"Apps"** (top navigation bar) > **"Manage Apps"**.
        
3. **Browse More Apps:**
    
    - On the "Apps" page, click the **"Browse more apps"** button.
        
4. **Search and Install:**
    
    - In the Splunkbase search bar, type **"Splunk Add-on for Okta Identity Cloud"**.
        
    - Click the **"Install"** button next to the add-on.
        
    - Agree to the terms and conditions. Splunk will install the add-on (may require a restart).
 <img width="681" height="503" alt="image" src="https://github.com/user-attachments/assets/f901fb42-aaac-4a07-adc1-18f1016063bf" />
 <img width="631" height="443" alt="Screenshot 2025-07-26 155715" src="https://github.com/user-attachments/assets/fd4671b1-9e38-4e33-9eff-09da1f2cefce" />
      

### B. Configure Okta Account within the Splunk Add-on

This step provides the Splunk Add-on with your Okta API credentials.

1. **Navigate to the Add-on's Configuration:**
    
    - Once Splunk has restarted (if required), go to **Apps** > **Splunk Add-on for Okta Identity Cloud** (click on the app itself).
        
    - Click on the **"Configuration"** tab.
   <img width="952" height="885" alt="Screenshot 2025-07-26 160300" src="https://github.com/user-attachments/assets/24d2c544-be63-48a2-bbff-22b9b13e5340" />
     
2. **Add Okta Account:**
    
    - Click on the **"Okta Accounts"** sub-tab.
        
    - Click the **"Add"** button.
        
    - **Okta Account Name:** Enter a descriptive name (e.g., `Okta_API_Account`).
        
    - **Auth Type:** Select **`Basic Authentication`**.
        
    - **Okta Domain:** Enter your Okta organization's domain **without `https://`** (e.g., `****.okta.com`).
        
    - **Okta API Token:** Paste the **Okta API Token** you created in the prerequisites.
        
    - Click **"Add"**.

   <img width="834" height="545" alt="Screenshot 2025-07-26 164134copy" src="https://github.com/user-attachments/assets/b9f4b19b-2806-47be-ba1b-17a3d76f5ef8" />
   <img width="970" height="421" alt="Screenshot 2025-07-26 165146" src="https://github.com/user-attachments/assets/009b2ffe-723c-4803-aba6-3933a46fb70a" />

### C. Configure Add-on Settings (Optional but Recommended)

This sets the limits for data collection.

1. **Navigate to "Add-on Settings":**
    
    - Within the Splunk Add-on for Okta Identity Cloud, click on the **"Add-on Settings"** sub-tab.
        
2. **Review and Save Defaults:**
    
    - The default limits (User Limit: 200, Group Limit: 300, App Limit: 200, Log Limit: 1000, Rate Limit Pct: 50.0) are generally good for a lab.
        
    - Ensure **"Dynamic Rate Throttling"** is checked.
        
    - Click the **"Save"** button at the bottom.

  <img width="972" height="872" alt="Screenshot 2025-07-26 165206" src="https://github.com/user-attachments/assets/c515509f-155b-40e9-bd5a-b5aada056ead" />

### D. Configure Proxy Settings (If Applicable)

1. **Navigate to "Proxy":**
    
    - Within the Splunk Add-on for Okta Identity Cloud, click on the **"Proxy"** sub-tab.
        
2. **Configure Proxy (if needed):**
    
    - If the Splunk instance needs to go through a proxy to reach Okta, enable the proxy and fill in the details.
        
    - **Action:** For this lab, ensure the "Enable Proxy" checkbox is **UNCHECKED** unless your network explicitly requires it.
        
    - Click the **"Save"** button at the bottom.

  <img width="971" height="806" alt="image" src="https://github.com/user-attachments/assets/4e50d667-9229-43e8-8f82-1a7c4071aebb" />
   
### E. Configure Logging Settings

1. **Navigate to "Logging":**
    
    - Within the Splunk Add-on for Okta Identity Cloud, click on the **"Logging"** sub-tab.
        
2. **Set Log Level:**
    
    - **Log Level:** `INFO` is a good default.
        
    - Click the **"Save"** button at the bottom.

<img width="966" height="737" alt="Screenshot 2025-07-26 165239" src="https://github.com/user-attachments/assets/e9e66d76-9b60-41f2-85a0-6055ccf011d0" />
        
### F. Create Data Input for Okta System Logs

This is the final step to tell the add-on to start pulling logs.

1. **Navigate to "Inputs":**
    
    - Click on the **"Inputs"** tab (at the top, next to "Configuration").
        
2. **Create New Input:**
    
    - On the "Inputs" page, click the **"Create New Input"** button (or "Add new input" for "Okta System Logs").
        
3. **Configure Input Details:**
    
    - **Name:** Give this input a name (e.g., `Okta_System_Logs_Input`).
        
    - **Okta Account:** Select the Okta account you configured (e.g., `Okta_API_Account`).
        
    - **Collection Interval:** Leave as default (e.g., 300 seconds for 5 minutes).
        
    - **Start Date:** To collect historical data, click **"No"** next to "Use existing data input?". Then, in the now-editable "Start Date" field, enter your desired historical start date (e.g., `2025-06-01T00:01:26.062Z`).
        
    - **End Date:** Leave blank for continuous collection.
        
    - **Query Window Size:** `3600` (default).
        
    - Leave other settings as default.
        
    - Click **"Save"**.
  
<img width="816" height="753" alt="Screenshot 2025-07-26 165635" src="https://github.com/user-attachments/assets/49f5317c-1110-423c-a73d-a1b0e08cf444" />
      
## V. Verification: Data Ingestion in Splunk Cloud

This confirms that logs are successfully flowing from Okta to Splunk.

1. **Generate Test Logs in Okta:**
    
    - Log in/out of your Okta tenant.
        
    - Create a new test user (e.g., `workflow.test@yourdomain.com`).
        
    - Deactivate a test user (e.g., `workflow.test@yourdomain.com`).
        
    - Assign an application to a user.
        
    - Change a group name.
        
2. **Verify Logs in Splunk Cloud:**
    
    - Log in to your Splunk Cloud Instance.
        
    - Go to **Search & Reporting**.
        
    - Set the **Time range** to **"All time"** (or a broad range like "Last 30 days" to cover your historical start date).
        
    - Run the confirmed search query: `index="main" sourcetype="okta:identity:cloud"`
        
    - **Confirmation:** You should see events from your Okta tenant appearing in the search results, including events generated after setup and historical events from your specified start date. (This was successfully verified by deactivating a user and seeing the logs appear).

<img width="956" height="878" alt="image" src="https://github.com/user-attachments/assets/f6b8b113-f696-4ecc-83bf-e43749ba51b3" />
<img width="977" height="850" alt="Screenshot 2025-07-26 170411" src="https://github.com/user-attachments/assets/19a9f6cf-4d7d-431a-b855-377e2cb55661" />
<img width="963" height="907" alt="Screenshot 2025-07-26 170435" src="https://github.com/user-attachments/assets/e5fe179e-ff13-4169-ad44-ec51ab3a6b3f" />
        
## VI. Configuration Steps: Building Dashboards & Alerts

This section details the  search queries and dashboarding steps used to visualize and monitor Okta logs.

### A. Dashboard Panels

The `MellonRyon Dashboard` was created to visualize key security and operational metrics.

<img width="3750" height="1699" alt="Screenshot 2025-08-12 132432" src="https://github.com/user-attachments/assets/23c91aa9-ec91-45b2-ae3a-702be41df883" />
<img width="1747" height="1433" alt="image" src="https://github.com/user-attachments/assets/98e40a1e-1ab2-4c2f-b0a5-076172e98771" />

1. **Successful Logins Panel**:
    
    - **Objective**: To track successful login events over time.
        
    - **Query**:
        
        ```
        index=* sourcetype="OktaIM2:log" dest="****.okta.com" eventType="user.session.start" outcome.result="SUCCESS" | timechart span=1d count
        ```
        
    - **Panel Type**: Line Chart
 
<img width="3813" height="1684" alt="Screenshot 2025-08-12 133022copy" src="https://github.com/user-attachments/assets/010adb39-b157-460d-a16a-ffae50256cb2" />
       
2. **Failed Logins Panel**:
    
    - **Objective**: To track all failed authentication attempts.
        
    - **Query**:
        
        ```
        index=* sourcetype="OktaIM2:log" dest="****.okta.com" outcome.result="FAILURE" | timechart span=1d count
        ```
        
    - **Panel Type**: Line Chart
  
<img width="3809" height="2111" alt="image" src="https://github.com/user-attachments/assets/fc0cc47d-0b26-4f32-8c56-ec10b73defcf" />

3. **User Lifecycle Events Panel**:
    
    - **Objective**: To monitor user creation, deactivation, and updates.
        
    - **Query**:
        
        ```
        index=* sourcetype="OktaIM2:log" dest="*****.okta.com" eventType="user.lifecycle.*" | stats count by eventType
        ```
        
    - **Panel Type**: Table

<img width="3819" height="2024" alt="image" src="https://github.com/user-attachments/assets/34502fc0-5d1c-499b-86fa-158d9f52bedb" />
        
4. **Admin Activity Panel**:
    
    - **Objective**: To monitor actions performed by the Okta administrator.
        
    - **Query**:
        
        ```
        index=* sourcetype="OktaIM2:log" dest="*****.okta.com" actor.alternateId="b.olanipekun@mellonryon.com" | top eventType
        ```
        
    - **Panel Type**: Bar Chart
 
<img width="3835" height="1994" alt="image" src="https://github.com/user-attachments/assets/d2ad936c-e44e-4c69-a9ce-690af148894b" />      

### B. Proactive Alerts

I configured 2 alerts to provide proactive security monitoring.

1. **Brute-Force Alert**:
    
    - **Objective**: To detect suspicious login attempts by flagging multiple failures from a single user or IP.
        
    - **Query**:
        
        ```
        index=* sourcetype="OktaIM2:log" dest="****.okta.com" outcome.result="FAILURE" | stats count by actor.alternateId, client.ipAddress | where count > 3
        ```
        
    - **Configuration**:
        
        - **Title**: `Brute-Force Alert`
            
        - **Alert Type**: `Scheduled`
            
        - **Schedule**: `Run every hour`
            
        - **Trigger Condition**: `Number of Results > 0`
            
    - **Note**: This alert was successfully validated in a controlled test by intentionally performing four failed logins for a test user. The alert's threshold of `count > 3` was chosen for the lab.
  
<img width="3835" height="1994" alt="image" src="https://github.com/user-attachments/assets/d5814955-a9e0-495b-882b-9c7bac4afb09" />
<img width="2406" height="1326" alt="Screenshot 2025-08-12 161405" src="https://github.com/user-attachments/assets/d3030216-6923-4d45-a688-f37fa2ef80b3" />
<img width="2408" height="1314" alt="Screenshot 2025-08-12 161859" src="https://github.com/user-attachments/assets/bc3ae571-5fc7-456f-9674-dcb760af6aed" />

**Add Alert Action:**

<img width="2169" height="1136" alt="Screenshot 2025-08-12 162110copy" src="https://github.com/user-attachments/assets/439f2c8d-db63-4b11-a792-061da8d995c0" />
<img width="2107" height="969" alt="Screenshot 2025-08-12 163043" src="https://github.com/user-attachments/assets/16cf28de-cc88-4c0c-a628-eb6541092242" />
<img width="2899" height="1265" alt="Screenshot 2025-08-12 162222" src="https://github.com/user-attachments/assets/42dcee09-70a8-4622-abe0-ba3bd7605290" />

2. **Unusual Location Login Alert**:
    
    - **Objective**: To detect successful logins from unexpected countries.
        
    - **Query**:
        
        ```
        index=* sourcetype="OktaIM2:log" dest="*****.okta.com" eventType="user.session.start" outcome.result="SUCCESS" client.geographicalContext.country!="Poland" AND client.geographicalContext.country!="US" | timechart span=1h count by client.geographicalContext.country
        ```
        
    - **Configuration**:
        
        - **Title**: `Unusual Location Login Alert`
            
        - **Alert Type**: `Scheduled`
            
        - **Schedule**: `Run every hour`
            
        - **Trigger Condition**: `Number of Results > 0`
            
    - **Note**: I initially configured this alert with an inclusion for "Poland" to test the trigger condition on a successful login from my location. After a successful trigger, the query was corrected to exclude Poland and other known locations, demonstrating a controlled validation and policy refinement process.
<img width="3348" height="937" alt="Screenshot 2025-08-12 163241" src="https://github.com/user-attachments/assets/276ca8aa-728d-4b73-afdc-712587800bbd" />
<img width="1434" height="837" alt="Screenshot 2025-08-12 215339" src="https://github.com/user-attachments/assets/92729bbb-ee6d-46e8-bc92-4775f977919a" />
<img width="3800" height="1199" alt="Screenshot 2025-08-12 163133" src="https://github.com/user-attachments/assets/763abb15-31b9-43b6-b980-09009b7f8380" />


## VII. Troubleshooting & Lessons Learned
The process of configuring Splunk provided invaluable insights into best practices for SIEM integrations:

- **Precision in Querying**: Successful searches in Splunk Cloud depend on using the precise field names and sourcetypes defined by the add-on (e.g., `sourcetype="OktaIM2:log"`, `dest`, `eventType`, `outcome.result`).
    
- **Debugging from Raw Data**: When a search fails, the most reliable approach is to inspect the raw event data (`index=* | head 10`) to discover the exact field names and their values.
    
- **Trigger Condition vs. Search Time**: The trigger condition for a scheduled alert (`where count > 3`) must be aligned with the search window of the alert (`Run every hour`).
    
- **Controlled Validation**: Intentionally creating scenarios (e.g., a failed login, a login from a new country) is a critical step in a lab environment to validate that security controls and alerts are functioning as intended.
    
- **Iterative Refinement**: Building and tuning dashboards and alerts is an iterative process. A successful query for one event type may not work for another, requiring continuous refinement.

This section highlights the challenges encountered and their resolutions.

- **Initial Failure of Okta Native Log Streaming (Push Method):**
    
    - **Problem:** Okta's native Log Streaming (`Reports > Log Streaming`) repeatedly deactivated by the system, with logs not appearing in Splunk.
        
    - **Troubleshooting:** Configured HEC token, identified HEC Endpoint URL (`https://http-inputs.prd-p-s76qb.splunkcloud.com:8088/services/collector/event`), and specified Splunk Edition (AWS). Despite correct configuration, the issue persisted.
        
    - **Lesson:** While native log streaming is ideal, sometimes environmental or specific tenant-level issues can prevent it. A reliable alternative is crucial.
        
- **Successful Implementation via Splunk Add-on (Pull Method):**
    
    - **Problem:** No Okta logs appeared in Splunk after installing the add-on and initial configuration.
        
    - **Root Cause 1: Incorrect Search Query/Time Range:** The initial search query (`source="okta_identity_cloud_logs"`) or a narrow time range (`Last 4 hours`) did not match the actual ingested data.
        
        - **Resolution:** Identified the correct `sourcetype` (`okta:identity:cloud`) and confirmed the `index` (`main`) through broad searches (`trial-5828141.okta.com`) and by examining the add-on's Monitoring Dashboard. Broadened the search time range.
            
    - **Root Cause 2: Start Date Checkpoint:** The add-on had an existing checkpoint, preventing historical data collection.
        
        - **Resolution:** Reset the checkpoint by selecting "No" for "Use existing data input" during input configuration, and explicitly set the `Start Date` to `2025-06-01T00:01:26.062Z` to collect historical logs.
            
    - **Lesson:** For add-ons, always verify the actual `index` and `sourcetype` used, and be aware of checkpointing for historical data collection. The add-on's internal logs (`index=_internal sourcetype="okta_identity_cloud_addon_log"`) are invaluable for debugging.
 
This iterative process of troubleshooting and adapting the integration method ultimately led to a successful and verified centralized logging solution.

* **Field Discovery First:** Start broad (`index=main sourcetype=okta:identity:cloud | head 20`), then refine—confirm actual field names (`eventType`, `outcome.result`, `actor.*`, `client.*`).
* **Sourcetype & Index Consistency:** Use the sourcetype the add-on emits (`okta:identity:cloud`) and verify the target index (default: `main`).
* **Checkpoint Awareness:** To ingest historical data, **reset the input** and specify **Start Date**; otherwise, the checkpoint prevents backfill.
* **Alert Windows vs Thresholds:** Align search time ranges with trigger conditions (e.g., hourly schedule with `where count > 3`).
* **Add-on Internal Logs:** When stuck, check:

  ```
  index=_internal sourcetype="okta_identity_cloud_addon_log"
  ```       

## VIII. Next Steps & Enhancements

With centralized auditing and alerting successfully implemented, the next steps for the Enterprise IAM Lab can focus on leveraging this data and maturing the IaC and security aspects:

- **Compliance Reporting**: Develop specific Splunk reports to demonstrate adherence to ISO 27001 or SOX controls using the ingested Okta data.
    
- **Expand Data Collection**: Configure the Splunk Add-on to pull other Okta data types (Users, Groups, Applications) for richer context in Splunk.
    
- **Terraform for Cloud IAM**: Automate cloud IAM configurations using Terraform.
---
