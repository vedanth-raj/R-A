# 🚀 AWS Deployment Guide - Manual Console Deployment

This guide provides step-by-step instructions for deploying your AI Research Agent application to AWS using the AWS Console (web interface).

## 📋 Prerequisites

1. **AWS Account** - Sign up at https://aws.amazon.com (Free tier available)
2. **Your Application Files** - Ensure all files are ready locally
3. **API Keys** - Have your Gemini API key and Semantic Scholar API key ready

---

## 🎯 PART 1: PREPARE YOUR APPLICATION

### Step 1: Prepare Application Files

Before deploying, ensure you have these files ready:

1. **Create a ZIP file** of your application:
   - Include all Python files (*.py)
   - Include requirements.txt
   - Include templates/ folder
   - Include static/ folder
   - Include .ebextensions/ folder (if exists)
   - Include application.py (entry point)
   - **EXCLUDE**: .venv/, .git/, data/, __pycache__/, *.pyc

2. **On Windows, create the ZIP**:
   ```bash
   # Navigate to your project folder
   cd path/to/your/project
   
   # Create a ZIP file (you can use Windows Explorer or 7-Zip)
   # Right-click → Send to → Compressed (zipped) folder
   # Name it: ai-research-agent.zip
   ```

---

## 🌐 PART 2: AWS CONSOLE DEPLOYMENT

### Step 2: Sign in to AWS Console

1. Go to https://console.aws.amazon.com/
2. Sign in with your AWS account credentials
3. Select your preferred region (top-right corner)
   - Recommended: **US East (N. Virginia)** - us-east-1
   - Or choose the region closest to your users

---

### Step 3: Create Elastic Beanstalk Application

1. **Navigate to Elastic Beanstalk**:
   - In the AWS Console search bar, type "Elastic Beanstalk"
   - Click on "Elastic Beanstalk" service

2. **Create Application**:
   - Click the orange "Create Application" button
   
3. **Configure Application**:
   
   **Application Information:**
   - Application name: `ai-research-agent`
   - Application tags (optional): Add tags if needed
   
   **Environment Information:**
   - Environment name: `ai-research-prod`
   - Domain: Leave auto-generated or customize (e.g., `my-research-agent`)
     - This will be your URL: `your-domain.elasticbeanstalk.com`
   
   **Platform:**
   - Platform: Select "Python"
   - Platform branch: "Python 3.11 running on 64bit Amazon Linux 2023"
   - Platform version: (Recommended - latest)
   
   **Application Code:**
   - Select "Upload your code"
   - Version label: `v1.0` (or any version name)
   - Click "Choose file" and select your `ai-research-agent.zip`
   - Wait for upload to complete (may take 1-2 minutes)
   
   **Presets:**
   - Select "Single instance (free tier eligible)" for testing
   - Or "High availability" for production (costs more)

4. **Click "Next"** to continue

---

### Step 4: Configure Service Access

1. **Service Role**:
   - Select "Create and use new service role"
   - Service role name: `aws-elasticbeanstalk-service-role` (auto-generated)

2. **EC2 Key Pair** (optional but recommended):
   - If you want SSH access, select an existing key pair
   - Or create a new one:
     - Click "Create new key pair"
     - Name it: `ai-research-agent-key`
     - Download the .pem file and save it securely

3. **EC2 Instance Profile**:
   - Select "Create and use new instance profile"
   - Or use existing: `aws-elasticbeanstalk-ec2-role`

4. **Click "Next"**

---

### Step 5: Configure Networking, Database, and Tags

1. **VPC**: Select default VPC

2. **Public IP address**: Check "Activated"

3. **Instance subnets**: Select at least one subnet (check one or more boxes)

4. **Database** (optional - skip for now):
   - You can add RDS database later if needed
   - For now, leave unchecked

5. **Tags** (optional):
   - Add tags for organization (e.g., Project: AI-Research)

6. **Click "Next"**

---

### Step 6: Configure Instance Traffic and Scaling

1. **Root volume type**: General Purpose (SSD)

2. **Size**: 10 GB (default is fine)

3. **Instance types**: 
   - For free tier: `t2.micro` or `t3.micro`
   - For better performance: `t2.small` or `t3.small`

4. **Environment type**:
   - Single instance (for testing/free tier)
   - Load balanced (for production)

5. **Click "Next"**

---

### Step 7: Configure Updates, Monitoring, and Logging

1. **Health reporting**: Enhanced (recommended)       

2. **Managed updates**: Enable (recommended)
   - Update level: Minor and patch

3. **CloudWatch logs**: Enable log streaming
   - Check "Stream logs to CloudWatch Logs"
   - Retention: 7 days (or as needed)

4. **Instance log streaming**: Enable

5. **Click "Next"**

---

### Step 8: Review and Submit

1. **Review all settings**:
   - Application name: ai-research-agent
   - Environment: ai-research-prod
   - Platform: Python 3.11
   - Instance type: t2.micro (or your choice)

2. **Click "Submit"**

3. **Wait for environment creation** (10-15 minutes):
   - You'll see a progress screen
   - Status will show: "Creating environment..."
   - Events will update in real-time
   - Wait until status shows "Ok" with green checkmark

---

### Step 9: Configure Environment Variables (API Keys)

**IMPORTANT**: Your application needs API keys to function!

1. **Navigate to your environment**:
   - Click on "ai-research-prod" environment name

2. **Go to Configuration**:
   - In the left sidebar, click "Configuration"
   - Or click "Configuration" in the environment overview

3. **Edit Software Settings**:
   - Scroll to "Software" category
   - Click "Edit" button

4. **Add Environment Properties**:
   - Scroll down to "Environment properties" section
   - Add the following properties:

   | Name | Value |
   |------|-------|
   | `GEMINI_API_KEY` | Your actual Gemini API key |
   | `SEMANTIC_SCHOLAR_API_KEY` | Your Semantic Scholar API key |
   | `FLASK_ENV` | `production` |
   | `SECRET_KEY` | `your-secret-key-here` (generate a random string) |

5. **Click "Apply"** at the bottom

6. **Wait for update** (2-3 minutes):
   - Environment will restart with new variables
   - Wait for status to return to "Ok"

---

### Step 10: Access Your Application

1. **Get your application URL**:
   - In the environment overview, you'll see the URL
   - Format: `http://ai-research-prod.us-east-1.elasticbeanstalk.com`
   - Or your custom domain if you set one

2. **Click the URL** or copy and paste into browser

3. **Test your application**:
   - The web interface should load
   - Try searching for papers
   - Verify all features work

---

## 🔧 PART 3: POST-DEPLOYMENT MANAGEMENT

### Monitor Your Application

1. **View Application Health**:
   - Go to Elastic Beanstalk Console
   - Click on your environment
   - Check the health status (should be green "Ok")

2. **View Logs**:
   - Click "Logs" in the left sidebar
   - Click "Request Logs" → "Last 100 Lines" or "Full Logs"
   - Download and view logs to troubleshoot issues

3. **Monitor Metrics**:
   - Click "Monitoring" in the left sidebar
   - View CPU, Network, Disk usage graphs
   - Set up alarms if needed

---

### Update Your Application

When you make code changes:

1. **Create new ZIP file** with updated code

2. **Upload new version**:
   - Go to Elastic Beanstalk Console
   - Click "Application versions" in left sidebar
   - Click "Upload" button
   - Choose your new ZIP file
   - Version label: `v1.1` (increment version)
   - Click "Upload"

3. **Deploy new version**:
   - Go back to your environment
   - Click "Upload and deploy" button
   - Select your new version
   - Click "Deploy"
   - Wait 3-5 minutes for deployment

---

### Scale Your Application

1. **Change Instance Type**:
   - Go to Configuration → Instances
   - Click "Edit"
   - Change instance type (e.g., t2.micro → t2.small)
   - Click "Apply"

2. **Add More Instances** (Load Balanced only):
   - Go to Configuration → Capacity
   - Click "Edit"
   - Set Min instances: 2, Max instances: 4
   - Click "Apply"

---

### Configure Custom Domain (Optional)

1. **Get a domain** from Route 53 or external registrar

2. **Create CNAME record**:
   - Point your domain to EB URL
   - Example: `app.yourdomain.com` → `ai-research-prod.us-east-1.elasticbeanstalk.com`

3. **Enable HTTPS** (recommended):
   - Go to Configuration → Load Balancer
   - Add HTTPS listener
   - Upload SSL certificate or use AWS Certificate Manager

---

## 🔧 TROUBLESHOOTING COMMON ISSUES

### Issue 1: Application Not Starting

**Symptoms**: Environment health is "Degraded" or "Severe"

**Solutions**:
1. Check logs:
   - Go to Logs → Request Logs → Full Logs
   - Look for Python errors or missing dependencies

2. Verify environment variables:
   - Configuration → Software → Environment properties
   - Ensure GEMINI_API_KEY is set correctly

3. Check requirements.txt:
   - Ensure all dependencies are listed
   - Verify versions are compatible

### Issue 2: 502 Bad Gateway Error

**Symptoms**: Browser shows "502 Bad Gateway"

**Solutions**:
1. Application might be taking too long to start
   - Increase timeout in .ebextensions/python.config
   - Add: `WSGIApplicationGroup %{GLOBAL}`

2. Check if application.py is correct:
   - Must have `application = app` variable
   - Must be in root directory

### Issue 3: WebSocket Connection Failed

**Symptoms**: Real-time updates not working

**Solutions**:
1. Ensure .ebextensions/03_websocket.config exists
2. Verify nginx configuration allows WebSocket upgrade
3. Check if eventlet is in requirements.txt

### Issue 4: Out of Memory

**Symptoms**: Application crashes, 502 errors

**Solutions**:
1. Upgrade instance type:
   - Configuration → Instances → Edit
   - Change from t2.micro to t2.small or t2.medium

2. Optimize your code:
   - Reduce memory usage in paper processing
   - Process papers in smaller batches

### Issue 5: Slow Performance

**Solutions**:
1. Enable caching
2. Upgrade to larger instance type
3. Use load balancing with multiple instances
4. Optimize database queries (if using RDS)

---

## 💰 COST ESTIMATION

### Free Tier (First 12 Months)
- ✅ 750 hours/month of t2.micro instance (FREE)
- ✅ 5GB of storage (FREE)
- ✅ 10GB data transfer out (FREE)
- **Estimated Cost**: $0/month for single t2.micro instance

### After Free Tier
- **t2.micro**: ~$8-10/month (1 GB RAM, 1 vCPU)
- **t2.small**: ~$17/month (2 GB RAM, 1 vCPU) - Recommended
- **t2.medium**: ~$34/month (4 GB RAM, 2 vCPU)
- **t3.small**: ~$15/month (2 GB RAM, 2 vCPU) - Better performance

### Additional Costs
- **Data transfer**: $0.09/GB after 10GB
- **Load balancer**: ~$16/month (if using high availability)
- **RDS database**: ~$15-30/month (if added)

### Cost Optimization Tips
1. Use t2.micro for development/testing
2. Stop environment when not in use (Configuration → Capacity → Edit → Min: 0)
3. Use single instance instead of load balanced
4. Monitor usage with AWS Cost Explorer

---

## 🛑 STOPPING AND DELETING RESOURCES

### Temporarily Stop Environment (Save Costs)

**Option 1: Reduce to Zero Instances**
1. Go to Configuration → Capacity
2. Click "Edit"
3. Set Environment type: Load balanced
4. Set Min instances: 0, Max instances: 1
5. Click "Apply"
6. **Note**: Only works with load balanced environments

**Option 2: Terminate Environment**
1. Go to Elastic Beanstalk Console
2. Select your environment
3. Click "Actions" → "Terminate environment"
4. Type environment name to confirm
5. Click "Terminate"
6. **Note**: You can recreate later from saved configuration

### Permanently Delete Application

1. **Terminate all environments first** (see above)

2. **Delete application**:
   - Go to Applications in left sidebar
   - Select your application
   - Click "Actions" → "Delete application"
   - Confirm deletion

3. **Clean up other resources**:
   - S3 buckets (if created)
   - CloudWatch logs (if you want to delete)
   - EC2 key pairs (if created)

---

## 📁 REQUIRED FILES FOR DEPLOYMENT

Ensure these files exist in your project:

### ✅ application.py (Entry Point)
```python
from web_app import app, socketio

application = app

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
```

### ✅ requirements.txt
Must include:
- flask>=2.3.0
- flask-socketio>=5.3.0
- gunicorn>=21.0.0
- eventlet>=0.33.0
- (all other dependencies)

### ✅ .ebextensions/python.config (Optional but Recommended)
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: application:application
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: "/var/app/current:$PYTHONPATH"
```

### ✅ .ebextensions/03_websocket.config (For WebSocket Support)
```yaml
files:
  "/etc/nginx/conf.d/websocket.conf":
    mode: "000644"
    owner: root
    group: root
    content: |
      upstream websocket {
          server 127.0.0.1:5000;
      }
      
      server {
          listen 80;
          
          location / {
              proxy_pass http://websocket;
              proxy_http_version 1.1;
              proxy_set_header Upgrade $http_upgrade;
              proxy_set_header Connection "upgrade";
              proxy_set_header Host $host;
              proxy_set_header X-Real-IP $remote_addr;
              proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          }
      }
```

### ✅ .ebignore (Exclude Unnecessary Files)
```
.git/
.venv/
venv/
__pycache__/
*.pyc
*.pyo
.env
.DS_Store
data/
*.log
.vscode/
.idea/
```

---

## 🎯 ALTERNATIVE: AWS EC2 MANUAL DEPLOYMENT

If you prefer more control over the server:

### Step 1: Launch EC2 Instance

1. **Go to EC2 Console**:
   - Search "EC2" in AWS Console
   - Click "Launch Instance"

2. **Configure Instance**:
   - Name: `ai-research-agent-server`
   - AMI: Ubuntu Server 22.04 LTS
   - Instance type: t2.micro (free tier) or t2.small
   - Key pair: Create new or select existing
   - Network: Default VPC
   - Security group: Create new
     - Allow SSH (port 22) from your IP
     - Allow HTTP (port 80) from anywhere
     - Allow HTTPS (port 443) from anywhere
     - Allow Custom TCP (port 5000) from anywhere

3. **Launch Instance**

### Step 2: Connect to Instance

1. **Get connection details**:
   - Select your instance
   - Click "Connect"
   - Copy the SSH command

2. **Connect via SSH**:
   ```bash
   ssh -i "your-key.pem" ubuntu@your-ec2-public-ip
   ```

### Step 3: Setup Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx git -y

# Create application directory
mkdir ~/ai-research-agent
cd ~/ai-research-agent

# Upload your files (use SCP or Git)
# Option 1: Using SCP from your local machine
# scp -i "your-key.pem" -r /path/to/your/project/* ubuntu@your-ec2-ip:~/ai-research-agent/

# Option 2: Using Git
# git clone https://github.com/your-username/your-repo.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
nano .env
# Add your API keys:
# GEMINI_API_KEY=your_key_here
# SEMANTIC_SCHOLAR_API_KEY=your_key_here

# Test application
python application.py
# Press Ctrl+C to stop
```

### Step 4: Setup Nginx Reverse Proxy

```bash
# Create nginx configuration
sudo nano /etc/nginx/sites-available/ai-research-agent
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # Or use EC2 public IP

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable and start:
```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/ai-research-agent /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

### Step 5: Setup as System Service

```bash
# Create service file
sudo nano /etc/systemd/system/ai-research-agent.service
```

Add this configuration:
```ini
[Unit]
Description=AI Research Agent Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/ai-research-agent
Environment="PATH=/home/ubuntu/ai-research-agent/venv/bin"
EnvironmentFile=/home/ubuntu/ai-research-agent/.env
ExecStart=/home/ubuntu/ai-research-agent/venv/bin/gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 application:application
Restart=always

[Install]
WantedBy=multi-user.target
```

Start the service:
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable ai-research-agent

# Start service
sudo systemctl start ai-research-agent

# Check status
sudo systemctl status ai-research-agent
```

### Step 6: Access Your Application

1. Get your EC2 public IP from AWS Console
2. Open browser: `http://your-ec2-public-ip`
3. Your application should be running!

---

## 🔒 SECURITY BEST PRACTICES

1. **Use HTTPS**:
   - Get free SSL certificate from Let's Encrypt
   - Configure nginx with SSL

2. **Restrict SSH Access**:
   - Only allow SSH from your IP
   - Use key-based authentication only

3. **Keep Secrets Safe**:
   - Never commit .env file to Git
   - Use AWS Secrets Manager for production

4. **Regular Updates**:
   - Keep system packages updated
   - Update Python dependencies regularly

5. **Firewall Rules**:
   - Only open necessary ports
   - Use AWS Security Groups effectively

---

## 📞 SUPPORT AND RESOURCES

### AWS Documentation
- Elastic Beanstalk: https://docs.aws.amazon.com/elasticbeanstalk/
- EC2: https://docs.aws.amazon.com/ec2/
- Python on EB: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-apps.html

### Troubleshooting Resources
- AWS Support: https://console.aws.amazon.com/support/
- Stack Overflow: Tag your questions with `aws-elastic-beanstalk`
- AWS Forums: https://forums.aws.amazon.com/

### Cost Management
- AWS Cost Explorer: https://console.aws.amazon.com/cost-management/
- AWS Pricing Calculator: https://calculator.aws/
- Free Tier Usage: https://console.aws.amazon.com/billing/home#/freetier

---

## ✅ DEPLOYMENT CHECKLIST

Before deploying, ensure:

- [ ] All code is tested locally
- [ ] requirements.txt is complete and up-to-date
- [ ] application.py exists and is correct
- [ ] .ebextensions/ folder is configured (if using EB)
- [ ] .ebignore excludes unnecessary files
- [ ] API keys are ready (GEMINI_API_KEY, SEMANTIC_SCHOLAR_API_KEY)
- [ ] ZIP file is created (for EB) or files are ready to upload (for EC2)
- [ ] AWS account is set up and verified
- [ ] Region is selected
- [ ] Budget alerts are configured (optional but recommended)

After deployment:

- [ ] Application URL is accessible
- [ ] All features work correctly
- [ ] API keys are configured in environment variables
- [ ] Logs are being generated
- [ ] Health status is "Ok" (green)
- [ ] Performance is acceptable
- [ ] Costs are within budget

---

## 🎉 CONGRATULATIONS!

Your AI Research Agent is now deployed on AWS!

**Recommended Next Steps**:
1. Test all features thoroughly
2. Set up monitoring and alerts
3. Configure custom domain (optional)
4. Enable HTTPS for security
5. Set up automated backups
6. Monitor costs regularly

**Need Help?**
- Check the Troubleshooting section above
- Review AWS documentation
- Check application logs for errors

---

**Ready to deploy? Start with PART 1: PREPARE YOUR APPLICATION above!**
