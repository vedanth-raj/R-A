# 🎯 AWS Console Step-by-Step Guide

Detailed instructions with exact button clicks and field values for AWS Console deployment.

---

## 🚀 STEP-BY-STEP DEPLOYMENT

### STEP 1: Sign In to AWS Console

1. Open your web browser
2. Go to: **https://console.aws.amazon.com/**
3. Click **"Sign In to the Console"**
4. Enter your **Root user email address** or **IAM user name**
5. Click **"Next"**
6. Enter your **Password**
7. Click **"Sign in"**
8. You should now see the AWS Management Console

**Region Selection** (Top-right corner):
- Click the region dropdown (e.g., "N. Virginia")
- Select: **US East (N. Virginia)** - us-east-1
- Or choose region closest to your users

---

### STEP 2: Navigate to Elastic Beanstalk

**Method 1: Using Search**
1. Look at the top of the page
2. Find the search bar (says "Search for services, features...")
3. Type: **"Elastic Beanstalk"**
4. Click on **"Elastic Beanstalk"** in the results
5. You'll see "Elastic Beanstalk" page

**Method 2: Using Services Menu**
1. Click **"Services"** in the top-left
2. Under "Compute", find **"Elastic Beanstalk"**
3. Click on it

**What you should see:**
- Page title: "Elastic Beanstalk"
- Orange button: "Create Application"
- Or list of existing applications (if any)

---

### STEP 3: Create Application - Page 1 (Application Info)

1. Click the orange **"Create Application"** button

**You'll see a form with multiple sections:**

#### Section 1: Application Information

**Field: Application name**
- Click in the text box
- Type: **ai-research-agent**
- (No spaces, lowercase recommended)

**Field: Application tags** (Optional)
- You can skip this
- Or add tags like:
  - Key: `Project`, Value: `AI Research`
  - Key: `Environment`, Value: `Production`

#### Section 2: Environment Information

**Field: Environment name**
- Auto-filled as: `ai-research-agent-env`
- Change to: **ai-research-prod**
- (This will be part of your URL)

**Field: Domain**
- Auto-filled based on environment name
- Shows: `ai-research-prod` (or similar)
- You can customize or leave as is
- Click **"Check availability"** to verify
- Should show: "✓ available"

**Note:** Your final URL will be:
`http://ai-research-prod.us-east-1.elasticbeanstalk.com`

#### Section 3: Platform

**Field: Platform**
- Click the dropdown
- Select: **Python**

**Field: Platform branch**
- Click the dropdown
- Select: **Python 3.11 running on 64bit Amazon Linux 2023**
- (Choose the latest Python 3.11 option)

**Field: Platform version**
- Leave as: **Recommended**
- (Latest stable version)

#### Section 4: Application Code

**Radio button: Upload your code**
- Click the radio button for **"Upload your code"**

**Field: Version label**
- Type: **v1.0**
- (Or any version name you prefer)

**Field: Source code origin**
- Click **"Choose file"** button
- Navigate to your **ai-research-agent.zip** file
- Select it
- Click **"Open"**
- You should see the filename appear

**Wait for upload:**
- Progress bar will show
- Wait until it says "Upload complete"
- May take 1-2 minutes depending on file size

#### Section 5: Presets

**Radio button: Single instance (free tier eligible)**
- Click this option
- (For production with more traffic, choose "High availability")

**What you should see now:**
- All fields filled in
- ZIP file uploaded
- Ready to proceed

2. Click the blue **"Next"** button at the bottom

---

### STEP 4: Configure Service Access - Page 2

#### Section 1: Service Access

**Service role**
- Select: **"Create and use new service role"**
- Role name will auto-fill as: `aws-elasticbeanstalk-service-role`

**EC2 key pair** (Optional but recommended)
- If you have a key pair:
  - Click dropdown
  - Select your existing key pair
- If you don't have one:
  - Click **"Create new key pair"** link
  - New window opens
  - Name: **ai-research-agent-key**
  - Key pair type: **RSA**
  - Private key format: **.pem**
  - Click **"Create key pair"**
  - File downloads automatically - **SAVE IT SECURELY**
  - Close the window
  - Refresh the dropdown
  - Select your new key pair

**EC2 instance profile**
- Select: **"Create and use new instance profile"**
- Profile name will auto-fill as: `aws-elasticbeanstalk-ec2-role`

**What you should see:**
- Service role: aws-elasticbeanstalk-service-role
- Key pair: (your key pair name or none)
- Instance profile: aws-elasticbeanstalk-ec2-role

2. Click the blue **"Next"** button at the bottom

---

### STEP 5: Set Up Networking, Database, and Tags - Page 3

#### Section 1: Networking

**VPC (Virtual Private Cloud)**
- Click dropdown
- Select: **Default VPC** (usually pre-selected)
- Shows something like: `vpc-xxxxx (default)`

**Public IP address**
- Check the box: ☑ **Activated**
- (This allows internet access to your app)

**Instance subnets**
- You'll see multiple checkboxes with subnet IDs
- Check **at least one** subnet
- Recommended: Check **all available subnets**
- Example: ☑ `subnet-xxxxx | us-east-1a`

#### Section 2: Database (Optional - Skip for now)

**Do NOT check "Enable database"**
- Leave unchecked
- (You can add database later if needed)

#### Section 3: Tags (Optional)

**Add tags if you want:**
- Click **"Add new tag"**
- Key: `Project`, Value: `AI-Research-Agent`
- Key: `Owner`, Value: `Your Name`
- (Helps organize resources)

**What you should see:**
- VPC selected
- Public IP activated
- At least one subnet checked
- Database unchecked

2. Click the blue **"Next"** button at the bottom

---

### STEP 6: Configure Instance Traffic and Scaling - Page 4

#### Section 1: Root Volume (EBS)

**Root volume type**
- Select: **General Purpose (SSD)**
- (Default and recommended)

**Size**
- Leave as: **10 GB**
- (Sufficient for most applications)

**IOPS**
- Leave as default (grayed out for GP2)

#### Section 2: EC2 Security Groups

**Leave as default**
- Auto-created security group will be used

#### Section 3: Instance Types

**Instance types**
- Click **"Add instance type"** if needed
- For free tier: Select **t2.micro** or **t3.micro**
- For better performance: Select **t2.small** or **t3.small**
- Check the box next to your chosen type

**Recommended:**
- ☑ **t2.micro** (free tier, 1GB RAM) - for testing
- ☑ **t2.small** (2GB RAM, ~$17/month) - for production

#### Section 4: Capacity

**Environment type**
- **Single instance** (already selected from presets)
- (For high availability, choose "Load balanced")

**What you should see:**
- Root volume: 10GB General Purpose SSD
- Instance type: t2.micro or t2.small selected
- Environment type: Single instance

2. Click the blue **"Next"** button at the bottom

---

### STEP 7: Configure Updates, Monitoring, and Logging - Page 5

#### Section 1: Monitoring

**Health reporting**
- Select: **Enhanced**
- (Provides detailed health information)

**Health event streaming to CloudWatch Logs**
- Check: ☑ **Enabled**

#### Section 2: Managed Platform Updates

**Managed updates**
- Check: ☑ **Activated**

**Update level**
- Select: **Minor and patch**
- (Automatically applies security updates)

**Maintenance window**
- Leave as default or customize
- Day: Any day
- Start time: Any time (e.g., 02:00 UTC)

#### Section 3: Platform Software

**Leave all as default**

#### Section 4: CloudWatch Logs

**Instance log streaming to CloudWatch Logs**
- Check: ☑ **Activated**

**Retention**
- Select: **7 days**
- (Or longer if you need more history)

**Lifecycle**
- Leave as default

**What you should see:**
- Health reporting: Enhanced ✓
- Managed updates: Activated ✓
- CloudWatch logs: Activated ✓

2. Click the blue **"Next"** button at the bottom

---

### STEP 8: Review - Page 6

**You'll see a summary of all your settings:**

#### Review Each Section:

**Application**
- Name: ai-research-agent ✓
- Environment: ai-research-prod ✓

**Platform**
- Platform: Python ✓
- Branch: Python 3.11 ✓
- Version: Recommended ✓

**Application code**
- Version: v1.0 ✓
- Source: (your ZIP file) ✓

**Presets**
- Type: Single instance ✓

**Service access**
- Service role: Created ✓
- Instance profile: Created ✓

**Networking**
- VPC: Default ✓
- Public IP: Activated ✓
- Subnets: Selected ✓

**Instance**
- Type: t2.micro or t2.small ✓
- Volume: 10GB ✓

**Monitoring**
- Health: Enhanced ✓
- Logs: Enabled ✓

**If everything looks correct:**

1. Click the orange **"Submit"** button at the bottom

**What happens next:**
- You'll be redirected to the environment page
- Status will show: "Creating environment..."
- Events will update in real-time
- Progress bar will show

---

### STEP 9: Wait for Environment Creation

**This takes 10-15 minutes. You'll see:**

#### Events Tab (Real-time updates):
```
Creating environment...
Creating security groups...
Creating load balancer...
Launching EC2 instance...
Installing application...
Application deployment successful
Environment health has transitioned to Ok
```

#### What to watch for:

**Status Indicator** (Top of page):
- 🟡 Yellow: Creating/Updating
- 🟢 Green: Ok (Success!)
- 🔴 Red: Severe (Error)

**Health Status:**
- Wait for: **Ok** with green checkmark ✓

**When complete, you'll see:**
- Status: **Ok** (green)
- Health: **Ok** (green)
- URL: `http://ai-research-prod.us-east-1.elasticbeanstalk.com`

**If you see errors:**
- Click on **"Events"** tab
- Look for error messages
- Refer to AWS_TROUBLESHOOTING_GUIDE.md

---

### STEP 10: Configure Environment Variables (CRITICAL!)

**Your app needs API keys to work!**

1. **Navigate to Configuration:**
   - You should be on your environment page
   - Look at the left sidebar
   - Click **"Configuration"**
   - Or click **"Configuration"** tab at the top

2. **Find Software Settings:**
   - Scroll down to find categories
   - Look for **"Software"** category
   - Click the **"Edit"** button on the right

3. **Scroll to Environment Properties:**
   - Scroll down the page
   - Find section: **"Environment properties"**
   - You'll see a table with Name/Value columns

4. **Add Your API Keys:**

   **First Property:**
   - Name field: Type **GEMINI_API_KEY**
   - Value field: Paste your actual Gemini API key
   - (No quotes, just the key)

   **Second Property:**
   - Click **"Add environment property"**
   - Name: **SEMANTIC_SCHOLAR_API_KEY**
   - Value: Your Semantic Scholar API key

   **Third Property:**
   - Click **"Add environment property"**
   - Name: **FLASK_ENV**
   - Value: **production**

   **Fourth Property:**
   - Click **"Add environment property"**
   - Name: **SECRET_KEY**
   - Value: Generate a random string (e.g., `my-secret-key-12345`)

**Your table should look like:**
```
Name                          | Value
------------------------------|---------------------------
GEMINI_API_KEY               | AIzaSy... (your key)
SEMANTIC_SCHOLAR_API_KEY     | abc123... (your key)
FLASK_ENV                    | production
SECRET_KEY                   | my-secret-key-12345
```

5. **Save Changes:**
   - Scroll to the bottom
   - Click the orange **"Apply"** button
   - Confirmation dialog appears
   - Click **"Confirm"**

6. **Wait for Update:**
   - Status changes to "Updating"
   - Takes 2-3 minutes
   - Environment will restart
   - Wait for status to return to **"Ok"** (green)

---

### STEP 11: Access Your Application! 🎉

1. **Find Your URL:**
   - Go back to environment overview
   - Look at the top of the page
   - Find the URL (blue link)
   - Format: `http://ai-research-prod.us-east-1.elasticbeanstalk.com`

2. **Open Your App:**
   - Click the URL
   - Or copy and paste into new browser tab
   - Your application should load!

3. **Test Your Application:**
   - Try searching for papers
   - Test text extraction
   - Try generating drafts
   - Verify real-time updates work

**If it works: Congratulations! 🎉**

**If it doesn't work:**
- Check environment status (should be green)
- View logs: Logs → Request Logs → Last 100 Lines
- Refer to AWS_TROUBLESHOOTING_GUIDE.md

---

## 📊 POST-DEPLOYMENT TASKS

### Task 1: View Logs

1. Click **"Logs"** in left sidebar
2. Click **"Request Logs"** button
3. Select **"Last 100 Lines"**
4. Click **"Download"**
5. Open the downloaded file
6. Check for any errors

### Task 2: Monitor Health

1. Click **"Monitoring"** in left sidebar
2. View graphs:
   - Environment Health
   - Requests
   - CPU Utilization
   - Network
3. Ensure all metrics look normal

### Task 3: Set Up Billing Alerts

1. Click your account name (top-right)
2. Click **"Billing Dashboard"**
3. Click **"Budgets"** in left sidebar
4. Click **"Create budget"**
5. Select **"Cost budget"**
6. Set amount: **$10** (or your limit)
7. Add your email for alerts
8. Click **"Create budget"**

### Task 4: Test All Features

- [ ] Search for papers
- [ ] Download PDFs
- [ ] Extract text
- [ ] Analyze sections
- [ ] Generate drafts
- [ ] WebSocket updates
- [ ] All UI elements

---

## 🔄 HOW TO UPDATE YOUR APPLICATION

When you make code changes:

### Step 1: Create New ZIP
1. Update your code locally
2. Test locally
3. Create new ZIP file (same as before)
4. Name it with new version (e.g., v1.1)

### Step 2: Upload New Version
1. Go to Elastic Beanstalk Console
2. Click **"Application versions"** (left sidebar)
3. Click **"Upload"** button
4. Version label: **v1.1**
5. Click **"Choose file"**
6. Select your new ZIP
7. Click **"Upload"**
8. Wait for upload to complete

### Step 3: Deploy New Version
1. Go back to your environment
2. Click **"Upload and deploy"** button
3. Click **"Choose file"**
4. Select your new ZIP
5. Version label: **v1.1**
6. Click **"Deploy"**
7. Wait 3-5 minutes
8. Verify deployment

---

## 🛑 HOW TO STOP YOUR APPLICATION

### To Save Costs:

1. Go to your environment
2. Click **"Actions"** dropdown (top-right)
3. Select **"Terminate environment"**
4. Type the environment name to confirm
5. Click **"Terminate"**
6. Wait for termination (5 minutes)

**Note:** You can recreate later with same settings

---

## ✅ VERIFICATION CHECKLIST

After deployment, verify:

- [ ] Environment status is green "Ok"
- [ ] URL is accessible
- [ ] Application loads without errors
- [ ] Can search for papers
- [ ] Can extract text
- [ ] Can generate drafts
- [ ] WebSocket works (real-time updates)
- [ ] No errors in browser console
- [ ] No errors in application logs
- [ ] API keys are working
- [ ] Performance is acceptable
- [ ] Billing alerts are set up

---

## 🆘 QUICK TROUBLESHOOTING

### Problem: Can't access URL
**Solution:** Wait 5 more minutes, clear browser cache, try incognito mode

### Problem: 502 Bad Gateway
**Solution:** Check logs, verify application.py exists, check environment variables

### Problem: Features not working
**Solution:** Verify API keys are set correctly in environment variables

### Problem: Slow performance
**Solution:** Upgrade from t2.micro to t2.small

**For detailed troubleshooting:** See AWS_TROUBLESHOOTING_GUIDE.md

---

## 📞 NEED HELP?

1. **Check logs first**: Logs → Request Logs → Last 100 Lines
2. **Review troubleshooting guide**: AWS_TROUBLESHOOTING_GUIDE.md
3. **Check AWS documentation**: https://docs.aws.amazon.com/elasticbeanstalk/
4. **Contact AWS support**: https://console.aws.amazon.com/support/

---

## 🎉 SUCCESS!

If you've completed all steps and your application is running:

**Congratulations! Your AI Research Agent is now live on AWS!**

**Your URL:** `http://ai-research-prod.[region].elasticbeanstalk.com`

**Next steps:**
1. Share the URL with users
2. Monitor performance daily (first week)
3. Set up custom domain (optional)
4. Enable HTTPS (recommended)
5. Plan for scaling as needed

---

**Happy deploying! 🚀**
