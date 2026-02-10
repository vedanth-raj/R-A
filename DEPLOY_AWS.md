# Deploy to AWS - Complete Guide

## ✅ Recommended Deployment Method

AWS fully supports your application with:
- ✅ WebSocket support
- ✅ Long-running tasks
- ✅ File storage
- ✅ Background processing
- ✅ Scalability

---

## Deployment Options

### Option 1: AWS EC2 (Easiest, Full Control) ⭐ RECOMMENDED
- Full control over server
- Easy to set up
- Good for learning
- Free tier: 750 hours/month

### Option 2: AWS Elastic Beanstalk (Managed)
- Automated deployment
- Auto-scaling
- Load balancing
- Easier management

### Option 3: AWS ECS with Docker (Advanced)
- Container-based
- Highly scalable
- More complex setup

---

## Option 1: Deploy to AWS EC2 (Recommended)

### Prerequisites
1. AWS account (free tier available)
2. Credit/debit card (for verification, won't be charged on free tier)
3. Your GitHub repository

### Step 1: Create EC2 Instance

#### 1.1 Go to AWS Console
```
https://console.aws.amazon.com
```

#### 1.2 Navigate to EC2
- Search for "EC2" in top search bar
- Click "EC2"

#### 1.3 Launch Instance
1. Click **"Launch Instance"**
2. **Name**: `research-bot-server`
3. **AMI**: Ubuntu Server 22.04 LTS (Free tier eligible)
4. **Instance type**: t2.micro (Free tier eligible)
5. **Key pair**: 
   - Click "Create new key pair"
   - Name: `research-bot-key`
   - Type: RSA
   - Format: .pem (for Mac/Linux) or .ppk (for Windows)
   - Download and save securely!

6. **Network settings**:
   - ✅ Allow SSH traffic (port 22)
   - ✅ Allow HTTP traffic (port 80)
   - ✅ Allow HTTPS traffic (port 443)
   - Click "Edit" → Add rule:
     - Type: Custom TCP
     - Port: 5000
     - Source: Anywhere (0.0.0.0/0)

7. **Storage**: 8 GB (Free tier)

8. Click **"Launch Instance"**

#### 1.4 Wait for Instance
- Wait 2-3 minutes
- Status should be "Running"
- Note your **Public IPv4 address**

### Step 2: Connect to EC2 Instance

#### For Windows (using PuTTY):
1. Download PuTTY: https://www.putty.org/
2. Convert .pem to .ppk using PuTTYgen
3. Open PuTTY
4. Host: `ubuntu@your-ec2-ip`
5. Auth → Browse → Select .ppk file
6. Click "Open"

#### For Mac/Linux:
```bash
# Set permissions
chmod 400 research-bot-key.pem

# Connect
ssh -i research-bot-key.pem ubuntu@your-ec2-ip
```

### Step 3: Install Dependencies on EC2

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install Git
sudo apt install git -y

# Install nginx (optional, for production)
sudo apt install nginx -y
```

### Step 4: Clone Your Repository

```bash
# Clone from GitHub
git clone https://github.com/vedanth-raj/research-bot.git
cd research-bot

# Checkout your branch
git checkout Vedanth_Raj
```

### Step 5: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 6: Configure Environment Variables

```bash
# Create .env file
nano .env

# Add your API keys:
GEMINI_API_KEY=AIzaSyCZo1m9jpPHseH_0C6hKLGvJiqLDs2ajKM
SEMANTIC_SCHOLAR_API_KEY=Lpesj1rrkxaP2zMWV0oqH2PNQN3KcoZR9tLNjmld

# Save: Ctrl+X, Y, Enter
```

### Step 7: Test the Application

```bash
# Run the app
python web_app.py
```

Visit: `http://your-ec2-ip:5000`

If it works, press Ctrl+C to stop.

### Step 8: Set Up Production Server (Gunicorn + Nginx)

#### 8.1 Install Gunicorn
```bash
pip install gunicorn eventlet
```

#### 8.2 Create Gunicorn Service
```bash
sudo nano /etc/systemd/system/research-bot.service
```

Add:
```ini
[Unit]
Description=Research Bot Flask App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/research-bot
Environment="PATH=/home/ubuntu/research-bot/venv/bin"
ExecStart=/home/ubuntu/research-bot/venv/bin/gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 web_app:app

[Install]
WantedBy=multi-user.target
```

Save: Ctrl+X, Y, Enter

#### 8.3 Start Service
```bash
# Reload systemd
sudo systemctl daemon-reload

# Start service
sudo systemctl start research-bot

# Enable on boot
sudo systemctl enable research-bot

# Check status
sudo systemctl status research-bot
```

#### 8.4 Configure Nginx (Optional)
```bash
sudo nano /etc/nginx/sites-available/research-bot
```

Add:
```nginx
server {
    listen 80;
    server_name your-ec2-ip;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Save and enable:
```bash
sudo ln -s /etc/nginx/sites-available/research-bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 9: Access Your Application

Visit: `http://your-ec2-ip`

✅ Your app is now live on AWS!

---

## Option 2: AWS Elastic Beanstalk

### Step 1: Install EB CLI

```bash
pip install awsebcli
```

### Step 2: Initialize EB

```bash
cd research-bot
eb init

# Follow prompts:
# - Region: Choose closest to you
# - Application name: research-bot
# - Platform: Python 3.10
# - SSH: Yes
# - Key pair: Create new or use existing
```

### Step 3: Create Environment

```bash
eb create research-bot-env

# Wait 5-10 minutes for environment creation
```

### Step 4: Set Environment Variables

```bash
eb setenv GEMINI_API_KEY=your_key SEMANTIC_SCHOLAR_API_KEY=your_key
```

### Step 5: Deploy

```bash
eb deploy
```

### Step 6: Open Application

```bash
eb open
```

---

## Option 3: AWS ECS with Docker

### Step 1: Build Docker Image

```bash
# Build image
docker build -t research-bot .

# Test locally
docker run -p 5000:5000 --env-file .env research-bot
```

### Step 2: Push to ECR

```bash
# Create ECR repository
aws ecr create-repository --repository-name research-bot

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account-id.dkr.ecr.us-east-1.amazonaws.com

# Tag image
docker tag research-bot:latest your-account-id.dkr.ecr.us-east-1.amazonaws.com/research-bot:latest

# Push image
docker push your-account-id.dkr.ecr.us-east-1.amazonaws.com/research-bot:latest
```

### Step 3: Create ECS Cluster

1. Go to ECS console
2. Create cluster
3. Choose Fargate
4. Create task definition
5. Create service
6. Deploy

---

## Cost Comparison

### EC2 Free Tier (12 months):
- ✅ 750 hours/month t2.micro
- ✅ 30 GB storage
- ✅ 15 GB bandwidth
- **Cost after free tier**: ~$10/month

### Elastic Beanstalk:
- Uses EC2 underneath
- Same free tier
- Easier management
- **Cost**: Same as EC2

### ECS Fargate:
- Pay per use
- No free tier for Fargate
- **Cost**: ~$15-30/month

---

## Domain Name (Optional)

### Step 1: Buy Domain
- Namecheap, GoDaddy, or AWS Route 53
- Cost: ~$10-15/year

### Step 2: Point to EC2
1. Get EC2 Elastic IP (free if attached)
2. Add A record in DNS:
   ```
   Type: A
   Name: @
   Value: your-elastic-ip
   ```

### Step 3: Update Nginx
```bash
sudo nano /etc/nginx/sites-available/research-bot
```

Change `server_name` to your domain:
```nginx
server_name yourdomain.com www.yourdomain.com;
```

### Step 4: Add SSL (Free with Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## Monitoring & Maintenance

### View Logs
```bash
# Application logs
sudo journalctl -u research-bot -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Restart Service
```bash
sudo systemctl restart research-bot
```

### Update Application
```bash
cd /home/ubuntu/research-bot
git pull origin Vedanth_Raj
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart research-bot
```

---

## Security Best Practices

### 1. Use Security Groups
- Only open necessary ports
- Restrict SSH to your IP

### 2. Keep System Updated
```bash
sudo apt update && sudo apt upgrade -y
```

### 3. Use Environment Variables
- Never commit API keys
- Use .env file

### 4. Enable Firewall
```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 5. Regular Backups
- Snapshot EC2 instance weekly
- Backup data folder

---

## Troubleshooting

### App not accessible
```bash
# Check if service is running
sudo systemctl status research-bot

# Check logs
sudo journalctl -u research-bot -n 50

# Restart service
sudo systemctl restart research-bot
```

### Port 5000 not accessible
- Check Security Group rules
- Ensure port 5000 is open
- Check if app is binding to 0.0.0.0

### Out of memory
- Upgrade to t2.small ($10/month)
- Or add swap space:
```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## Summary

### Recommended: EC2 with Nginx + Gunicorn
✅ Full control
✅ WebSocket support
✅ File storage
✅ Easy to manage
✅ Free tier available

### Steps:
1. Create EC2 instance
2. Install dependencies
3. Clone repository
4. Set up environment
5. Configure Gunicorn + Nginx
6. Access your app!

### Cost:
- **Free tier**: $0/month (12 months)
- **After free tier**: ~$10/month

---

**Your app will be live at**: `http://your-ec2-ip:5000`

**With domain**: `https://yourdomain.com`

🎉 **Ready to deploy!**
