# 🚀 AWS Deployment Guide

## 📋 Prerequisites

1. **AWS Account** - Sign up at https://aws.amazon.com
2. **AWS CLI** - Install from https://aws.amazon.com/cli/
3. **EB CLI** - Elastic Beanstalk CLI tool

## 🛠️ Step 1: Install AWS Tools

### Install AWS CLI
```bash
# Download from: https://awscli.amazonaws.com/AWSCLIV2.msi
# Or use pip:
pip install awscli
```

### Install EB CLI
```bash
pip install awsebcli
```

### Configure AWS Credentials
```bash
aws configure
```

You'll need:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., us-east-1)
- Output format: json

## 🎯 Step 2: Initialize Elastic Beanstalk

```bash
eb init
```

Follow the prompts:
1. Select region (e.g., us-east-1)
2. Create new application: "ai-research-agent"
3. Platform: Python 3.11
4. Use CodeCommit: No
5. Setup SSH: Yes (optional)

## 🚀 Step 3: Create Environment

```bash
eb create ai-research-prod
```

Options:
- Environment name: ai-research-prod
- DNS CNAME: (auto-generated or custom)
- Load balancer: Application

## 🔐 Step 4: Set Environment Variables

```bash
eb setenv GEMINI_API_KEY=your_gemini_key_here
eb setenv SEMANTIC_SCHOLAR_API_KEY=your_semantic_scholar_key_here
eb setenv FLASK_ENV=production
```

Or use AWS Console:
1. Go to Elastic Beanstalk Console
2. Select your environment
3. Configuration → Software → Environment properties
4. Add your API keys

## 📦 Step 5: Deploy

```bash
eb deploy
```

Wait for deployment to complete (5-10 minutes)

## 🌐 Step 6: Access Your App

```bash
eb open
```

Or get the URL:
```bash
eb status
```

Your app will be at: `http://ai-research-prod.us-east-1.elasticbeanstalk.com`

## 📊 Monitoring & Management

### View Logs
```bash
eb logs
```

### Check Health
```bash
eb health
```

### SSH into Instance
```bash
eb ssh
```

### Scale Up/Down
```bash
eb scale 2  # Run 2 instances
```

## 💰 Cost Estimation

**Free Tier (First 12 months):**
- 750 hours/month of t2.micro instance
- 5GB of storage
- Likely FREE for development

**After Free Tier:**
- t2.micro: ~$8-10/month
- t2.small: ~$17/month
- t3.medium: ~$30/month

## 🔧 Troubleshooting

### Deployment Failed
```bash
eb logs --all
```

### App Not Starting
Check environment variables:
```bash
eb printenv
```

### WebSocket Issues
- Ensure nginx config is applied
- Check .ebextensions/03_websocket.config

### Memory Issues
Upgrade instance type:
```bash
eb scale --instance-type t2.small
```

## 🔄 Update Deployment

After making code changes:
```bash
git add .
git commit -m "Update features"
eb deploy
```

## 🛑 Terminate Environment (Stop Costs)

```bash
eb terminate ai-research-prod
```

## 📁 Files Created for AWS

- ✅ `application.py` - EB entry point
- ✅ `.ebextensions/` - Configuration files
- ✅ `.ebignore` - Files to exclude
- ✅ `Procfile` - Process configuration
- ✅ Updated `requirements.txt` - Added gunicorn

## 🎯 Alternative: AWS EC2 (Manual Setup)

If you prefer more control:

### 1. Launch EC2 Instance
- AMI: Ubuntu 22.04
- Instance Type: t2.micro (free tier)
- Security Group: Allow ports 22, 80, 443, 5000

### 2. Connect via SSH
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

### 3. Setup Server
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3-pip python3-venv nginx -y

# Clone your repo
git clone https://github.com/vedanth-raj/R-A.git
cd R-A

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
nano .env
# Add your API keys

# Run with gunicorn
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 application:application
```

### 4. Setup Nginx Reverse Proxy
```bash
sudo nano /etc/nginx/sites-available/research-agent
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/research-agent /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. Setup as Service
```bash
sudo nano /etc/systemd/system/research-agent.service
```

Add:
```ini
[Unit]
Description=AI Research Agent
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/R-A
Environment="PATH=/home/ubuntu/R-A/venv/bin"
ExecStart=/home/ubuntu/R-A/venv/bin/gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 application:application

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl enable research-agent
sudo systemctl start research-agent
```

## 🎯 Recommended: Elastic Beanstalk

For easiest deployment, use Elastic Beanstalk (Steps 1-6 above).

## 📞 Support

- AWS Documentation: https://docs.aws.amazon.com/elasticbeanstalk/
- EB CLI Guide: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3.html

---

**Ready to deploy! Run `eb init` to get started.**
