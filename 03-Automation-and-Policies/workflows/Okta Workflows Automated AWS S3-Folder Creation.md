# Okta Workflows — Automated AWS S3 Folder Creation

> **Scope:** I built a practical, cross-cloud automation where an Okta user profile change (Mover scenario) triggers an **AWS Lambda** function to create a **personal folder** in a target **S3 bucket**. I used attribute-based logic (Department = “Marketing”) so the action only runs for the right users.

---
## I. Objective & Purpose

This lab demonstrates the implementation of a practical, live workflow to showcase cross-cloud automation. The primary objective was to build a flow that automatically provisions a personal folder in an AWS S3 bucket based on a user's attributes in Okta.

By creating this flow, we successfully demonstrated:

- **Automated Resource Provisioning**: A new user in Okta with a specific attribute automatically triggers the creation of a dedicated folder in AWS S3.
    
- **Cross-Cloud Integration**: How Okta Workflows can act as a central orchestration engine to securely connect and manage resources across different cloud providers (Okta and AWS).
    
- **Role-Based Access Control (RBAC)**: The flow uses conditional logic to trigger actions only for users with a specific role, enforcing a core RBAC principle.
    

## II. Technical Thought Process & Evolution of Configuration

The design of this workflow centered on creating a secure and reliable serverless integration pattern between Okta and AWS. The final, successful implementation was a result of a meticulous process of configuring each component to ensure it met the exact requirements of the target system.

**Key Design Decisions:**

- **Trigger (Mover Scenario)**: The **`Okta - User Profile Updated`** event card was selected as the trigger. This event-driven approach allows the flow to automatically run whenever a user's profile is modified, enabling a "Mover" scenario where a user's access or resources change with their role.
    
- **Conditional Logic**: An **`If/Else`** card was used to check if the user's `Department` attribute equals `"Marketing"`. This condition acts as a policy, ensuring the flow's actions are only executed for the relevant users and enforcing a basic RBAC model.
    
- **Secure Serverless Integration**: A serverless pattern was chosen to integrate with AWS. This involves an **AWS Lambda function** that contains the logic to create the S3 folder, which is then securely invoked by Okta Workflows. This pattern is highly secure as it avoids hardcoding AWS credentials in the workflow itself.
    
- **Correct Payload Formatting**: The `payload` sent to the AWS Lambda function was meticulously formatted as a JSON object, which the Lambda function was specifically coded to parse. This ensured that the data was correctly received and processed.
    
- **Dynamic Data Mapping**: A `Compose` card was used to dynamically construct the S3 folder name (e.g., `marketing-Joshua Dominguez`) using data pills from the `Read User` card. This ensured that a unique and consistent folder name was created for each user, avoiding a static folder name.
    

## III. Prerequisites

Before building the flow, the following foundational components were successfully configured:

- **Okta Workflows Console**: You have access with administrator permissions.
    
- **AWS Lambda Function**: A Python function named `create-s3-folder-function` was deployed.
    
- **Okta AWS Lambda Connection**: A working connection named `AWS_Lambda_Connection` was configured with the appropriate AWS IAM user credentials.
    
- **AWS S3 Bucket**: An existing S3 bucket named `mellonryon-fed-access-test-bucket-boluw-29jul-v2`.
    

## IV. Configuration Steps: Building the Workflow

This section outlines the final, successful steps to build the end-to-end workflow from a blank canvas.

### A. AWS Setup (Lambda Function & IAM Role)

1. **IAM Role for Lambda (Least Privilege)**:
    
    - A dedicated IAM Role was created for the Lambda function. This role was granted **only the necessary permissions** to perform its task, adhering to the principle of least privilege. The attached policy included:
        
        - `s3:PutObject`: To create the folder (an object with a trailing slash) in the S3 bucket.
            
        - `s3:ListBucket`: To list the contents of the S3 bucket.
            <img width="3653" height="808" alt="Screenshot 2025-08-07 104845" src="https://github.com/user-attachments/assets/3e9aa1e4-2a5c-4ddd-a613-6080c4eac34a" />
            <img width="3672" height="806" alt="Screenshot 2025-08-07 104918" src="https://github.com/user-attachments/assets/42c87a8e-9319-469e-a812-f7dab6a1887d" />

            <img width="2429" height="1301" alt="Screenshot 2025-08-07 105339" src="https://github.com/user-attachments/assets/0111cfec-ed84-49ed-8136-961a1af262dd" />

    - A separate IAM user was granted **`lambda:InvokeFunction`** permissions, allowing the Okta Workflows connection to trigger the Lambda.
       <img width="926" height="794" alt="Screenshot 2025-08-08 171240copy" src="https://github.com/user-attachments/assets/2504a37b-d85f-4206-84c4-753216177fe1" />
       
2. **AWS Lambda Function Code**:
    
    - A Python 3.9 Lambda function named `create-s3-folder-function` was deployed. The code was carefully written to handle the JSON payload from Okta Workflows and create the folder in S3.
        
    - The working Python code is as follows:
        
        ```
        import json
        import boto3
        
        def lambda_handler(event, context):
            s3 = boto3.client('s3')
        
            # Okta Workflows sends the payload directly as a dictionary
            body = event.get('body', {})
            bucket_name = body.get('bucket_name')
            folder_name = body.get('folder_name')
        
            if not bucket_name or not folder_name:
                return {
                    'statusCode': 400,
                    'headers': { 'Content-Type': 'application/json' },
                    'body': json.dumps({'message': 'Missing bucket_name or folder_name in request.'})
                }
        
            # S3 folders are objects with a trailing slash
            s3_folder_key = folder_name + '/'
        
            # Create the "folder" (an empty object with a trailing slash)
            try:
                s3.put_object(Bucket=bucket_name, Key=s3_folder_key)
                return {
                    'statusCode': 200,
                    'headers': { 'Content-Type': 'application/json' },
                    'body': json.dumps({'message': f'Folder {s3_folder_key} created successfully in bucket {bucket_name}.'})
                }
            except Exception as e:
                return {
                    'statusCode': 500,
                    'headers': { 'Content-Type': 'application/json' },
                    'body': json.dumps({'message': f'Error creating folder: {str(e)}'})
                }
        ```
        
    - The Lambda function's **Timeout** was increased to **10 seconds** to prevent execution failures.
        <img width="1733" height="1214" alt="Screenshot 2025-08-07 105505" src="https://github.com/user-attachments/assets/ff9bbf13-c4fb-4ae1-8bb6-0eed3e4a8398" />


### B. Okta Workflows Setup

1. **Create the Flow**:
    
    - In the Okta Workflows Console, create a new flow named `Mover - Automated AWS S3 Folder Creation`.
        
2. **Trigger (User Profile Updated)**:
    
    - Add an **`Okta - User Profile Updated`** event card. This is the trigger for the flow.
        
3. **Get User Profile**:
    
    - Add an **`Okta - Read User`** card.
        
    - Drag the **`ID`** pill from the "User Profile Updated" card into the `ID` field.
        
4. **Conditional Logic**:
    
    - Add a **`Branching - If/Else`** card.
        
    - Set the condition: `IF {{Okta Read User.Department}} equals Marketing`. This ensures the flow only proceeds for users in the `Marketing` department.
        
5. **Create Folder Name**:
    
    - Inside the `true` branch, add a **`Text - Compose`** card.
        
    - For the **Template**, type `marketing-` and then drag the **`firstName`** and **`lastName`** pills from the `Read User` card. The final template looks like: `marketing-{{Okta Read User.firstName}} {{Okta Read User.lastName}}`
        
6. **Invoke the AWS Lambda Function**:
    
    - Add an **`AWS Lambda - Invoke`** card to the right of the `Compose` card.
        
    - Select `AWS_Lambda_Connection`.
      <img width="1795" height="715" alt="Screenshot 2025-08-07 114731" src="https://github.com/user-attachments/assets/8c528cc4-c7b1-4cfb-82e0-d8e59ee3f2e6" />

      <img width="1584" height="986" alt="Screenshot 2025-08-07 115819" src="https://github.com/user-attachments/assets/d4aa95cb-bc88-4963-92b9-23077e93478e" />

    - For **Function Name**, type `create-s3-folder-function`.
        
    - In the `Payload` field, use the graphical editor to add the `output` pill from the `Compose` card to the `folder_name` parameter within the JSON payload. The payload should be structured as:
        
        ```
        {
          "body": {
            "bucket_name": "mellonryon-fed-access-test-bucket-boluw-29jul-v2",
            "folder_name": "{{Compose.output}}"
          }
        }
        ```
        
    - Set `invocationType` to **`RequestResponse`** and `logType` to **`Tail`**.
        
7. **Send the Notification Email**:
    
    - Add an **`Email - Send Email`** card.
        
    - Drag the **`Email`** pill from the `Read User` card into the `To` field.
        
    - For **Subject**, type `Your Personal S3 Folder is Ready!` and for **Body**, type a personalized message.
        
8. **Finalize Flow**:
    
    - Click **"Save"** and toggle the flow **"ON"**.
       <img width="1904" height="906" alt="Screenshot 2025-08-08 175826" src="https://github.com/user-attachments/assets/ed2e3267-ff8b-4910-b505-e8c8723c9574" />
       <img width="744" height="302" alt="Screenshot 2025-08-08 175841" src="https://github.com/user-attachments/assets/c4bbfc18-27ce-402c-b3cf-c65b97a9aba4" />
       <img width="1878" height="900" alt="Screenshot 2025-08-08 175654" src="https://github.com/user-attachments/assets/4ff9f9dd-c333-4aca-ac30-bf46e277815d" />


## V. General Analysis

This workflow successfully demonstrates a live, cross-cloud automation that uses attribute-based logic to orchestrate a serverless function. This showcases the practical application of Okta as a central hub for identity-driven actions. The successful troubleshooting process highlights the importance of debugging permissions, API payloads, and data-mapping in a cross-platform environment.

* **Identity-triggered automation:** Okta is the event source; cloud resources react.
* **Separation of secrets:** Workflows doesn’t hold AWS write perms; Lambda does the work under its own role.
* **RBAC enforcement:** Only users matching the condition trigger work.
* **Auditable:** Okta Execution History + CloudWatch logs + S3 object history give a clean trail.


## VI. Lessons Learned

The journey to a successful live workflow provided invaluable insights into best practices for cross-cloud automation:

- **Serverless Integration Pattern**: Using a dedicated AWS Lambda function invoked by Okta Workflows is a highly secure and flexible pattern for performing actions in a cloud provider. It allows for least-privilege permissions and avoids storing secrets in the workflow.
    
- **Precise Data Mapping**: Dynamic values (data pills) must be carefully mapped to ensure they are interpreted as dynamic values rather than literal strings, especially in JSON payloads.
    
- **Debugging Cross-Cloud**: When a flow fails, it is critical to check the specific log outputs from each system (e.g., Okta's Execution History, AWS CloudWatch logs) to pinpoint the exact cause of the error.
    
- **Granular Permissions**: The `invalid_grant` error underscored the importance of ensuring the IAM user has the specific, correct permissions (e.g., `lambda:InvokeFunction`) to perform the actions defined in the workflow.
    
- **Attribute-Based Logic**: Using a user's attributes (e.g., `Department`) as a decision point is a powerful way to automate complex, role-based provisioning scenarios.
