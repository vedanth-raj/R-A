# 🚀 AWS Deployment Documentation

Complete guide for deploying your AI Research Agent to AWS.

---

## 📚 Documentation Overview

This folder contains comprehensive guides for deploying your application to AWS:

### 1. **AWS_DEPLOYMENT_GUIDE.md** (Main Guide)
   - **Purpose**: Complete step-by-step deployment instructions
   - **Best for**: First-time deployers, detailed reference
   - **Contents**:
     - Part 1: Prepare Your Application
     - Part 2: AWS Console Deployment (10 detailed steps)
     - Part 3: Post-Deployment Management
     - Alternative EC2 deployment
     - Security best practices
     - Cost estimation

### 2. **AWS_CONSOLE_QUICK_GUIDE.md** (Quick Reference)
   - **Purpose**: Simplified visual guide with screenshots references
   - **Best for**: Quick deployment, visual learners
   - **Contents**:
     - Quick 10-step deployment
     - Visual indicators and tips
     - Common checks
     - Quick troubleshooting

### 3. **AWS_DEPLOYMENT_CHECKLIST.md** (Checklist)
   - **Purpose**: Ensure nothing is missed
   - **Best for**: Systematic deployment, verification
   - **Contents**:
     - Pre-deployment checklist
     - Deployment step checklist
     - Post-deployment verification
     - Cost management checklist
     - Update checklist

### 4. **AWS_TROUBLESHOOTING_GUIDE.md** (Problem Solving)
   - **Purpose**: Fix common issues
   - **Best for**: When things go wrong
   - **Contents**:
     - Critical issues (502 errors, won't start)
     - Common issues (memory, performance)
     - Debugging techniques
     - Emergency procedures

---

## 🎯 Quick Start

### For First-Time Deployers

1. **Read**: AWS_DEPLOYMENT_GUIDE.md (Part 1 & 2)
2. **Use**: AWS_DEPLOYMENT_CHECKLIST.md (check off items)
3. **Reference**: AWS_CONSOLE_QUICK_GUIDE.md (for quick steps)
4. **If issues**: AWS_TROUBLESHOOTING_GUIDE.md

### For Experienced Users

1. **Use**: AWS_CONSOLE_QUICK_GUIDE.md (quick deployment)
2. **Verify**: AWS_DEPLOYMENT_CHECKLIST.md (final checks)
3. **If issues**: AWS_TROUBLESHOOTING_GUIDE.md

---

## 📋 Prerequisites

Before starting, ensure you have:

- [ ] AWS account (sign up at https://aws.amazon.com)
- [ ] Credit card (required even for free tier)
- [ ] Gemini API key
- [ ] Semantic Scholar API key (optional)
- [ ] Application files ready
- [ ] ZIP file created (excluding .venv, .git, data)

---

## 🌐 Deployment Options

### Option 1: Elastic Beanstalk (Recommended)
- **Difficulty**: Easy
- **Time**: 20-30 minutes
- **Cost**: Free tier eligible
- **Best for**: Most users, automatic management
- **Guide**: AWS_DEPLOYMENT_GUIDE.md (Part 2)

### Option 2: EC2 Manual Setup
- **Difficulty**: Advanced
- **Time**: 1-2 hours
- **Cost**: Free tier eligible
- **Best for**: Full control, custom configuration
- **Guide**: AWS_DEPLOYMENT_GUIDE.md (Alternative section)

---

## 💰 Cost Estimate

### Free Tier (First 12 Months)
- **t2.micro instance**: 750 hours/month FREE
- **Storage**: 5GB FREE
- **Data transfer**: 10GB/month FREE
- **Estimated cost**: $0/month

### After Free Tier
- **t2.micro**: ~$8-10/month (1GB RAM)
- **t2.small**: ~$17/month (2GB RAM) - Recommended
- **t2.medium**: ~$34/month (4GB RAM)

### Cost Optimization
- Use t2.micro for testing
- Terminate when not in use
- Monitor with billing alerts
- Single instance (not load balanced)

---

## 🔧 Required Files

Ensure these files exist before deployment:

```
your-project/
├── application.py          # Entry point (REQUIRED)
├── web_app.py             # Main Flask app
├── requirements.txt       # Dependencies (REQUIRED)
├── config.py              # Configuration
├── templates/             # HTML templates (REQUIRED)
│   └── index.html
├── static/                # CSS/JS files (REQUIRED)
│   ├── css/
│   └── js/
├── .ebextensions/         # AWS configuration (optional)
│   ├── python.config
│   └── 03_websocket.config
└── .ebignore             # Exclude files (REQUIRED)
```

### Critical Files

**application.py** (must exist):
```python
from web_app import app, socketio

application = app

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
```

**.ebignore** (must exist):
```
.git/
.venv/
venv/
__pycache__/
*.pyc
data/
*.log
```

**requirements.txt** (must include):
```
flask>=2.3.0
flask-socketio>=5.3.0
gunicorn>=21.0.0
eventlet>=0.33.0
# ... other dependencies
```

---

## 🚀 Deployment Steps (Summary)

### Phase 1: Preparation (5 minutes)
1. Create ZIP file with all necessary files
2. Exclude .venv, .git, data folders
3. Verify application.py exists
4. Have API keys ready

### Phase 2: AWS Setup (15 minutes)
1. Sign in to AWS Console
2. Navigate to Elastic Beanstalk
3. Create new application
4. Upload ZIP file
5. Configure settings
6. Submit and wait

### Phase 3: Configuration (5 minutes)
1. Add environment variables (API keys)
2. Verify deployment
3. Test application
4. Check logs

### Phase 4: Verification (5 minutes)
1. Access application URL
2. Test all features
3. Monitor performance
4. Set up billing alerts

**Total Time**: ~30 minutes

---

## ✅ Success Criteria

Your deployment is successful when:

- [x] Environment status is green "Ok"
- [x] Application URL is accessible
- [x] Can search for papers
- [x] Can extract text from PDFs
- [x] Can generate drafts
- [x] Real-time updates work (WebSocket)
- [x] No errors in logs
- [x] Performance is acceptable
- [x] Costs are within budget

---

## 🔍 Common Issues & Solutions

### Issue: 502 Bad Gateway
**Solution**: Check application.py exists and logs for errors
**Guide**: AWS_TROUBLESHOOTING_GUIDE.md → Issue 2

### Issue: Application Won't Start
**Solution**: Verify requirements.txt and environment variables
**Guide**: AWS_TROUBLESHOOTING_GUIDE.md → Issue 3

### Issue: Out of Memory
**Solution**: Upgrade from t2.micro to t2.small
**Guide**: AWS_TROUBLESHOOTING_GUIDE.md → Issue 5

### Issue: WebSocket Not Working
**Solution**: Add .ebextensions/03_websocket.config
**Guide**: AWS_TROUBLESHOOTING_GUIDE.md → Issue 6

**For all issues**: See AWS_TROUBLESHOOTING_GUIDE.md

---

## 📊 Monitoring Your Deployment

### Daily Checks (First Week)
- Environment health status
- Application accessibility
- Error logs
- Cost accumulation

### Weekly Checks
- Performance metrics
- Cost analysis
- User feedback
- Feature usage

### Monthly Checks
- Security updates
- Dependency updates
- Backup verification
- Scaling needs

---

## 🔄 Updating Your Application

When you make code changes:

1. **Test locally first**
2. **Create new ZIP file**
3. **Upload to Application Versions**
4. **Deploy to environment**
5. **Verify deployment**
6. **Check logs**

**Time**: 5-10 minutes per update

---

## 🛑 Stopping Your Application

### Temporary Stop
```
Environment → Actions → Terminate Environment
```
- Stops all charges
- Can recreate later
- Configuration is saved

### Permanent Delete
```
1. Terminate all environments
2. Delete application
3. Clean up S3 buckets
4. Remove CloudWatch logs
```

---

## 📞 Getting Help

### Documentation
- **AWS Docs**: https://docs.aws.amazon.com/elasticbeanstalk/
- **Python on EB**: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-apps.html

### Community Support
- **Stack Overflow**: Tag `aws-elastic-beanstalk`
- **AWS Forums**: https://forums.aws.amazon.com/
- **Reddit**: r/aws

### AWS Support
- **Basic (Free)**: Account and billing questions
- **Developer ($29/mo)**: Technical support
- **Business ($100/mo)**: 24/7 support
- **Console**: https://console.aws.amazon.com/support/

### Before Asking for Help
1. Check AWS_TROUBLESHOOTING_GUIDE.md
2. Review logs thoroughly
3. Document the issue
4. List what you've tried
5. Provide error messages

---

## 🎯 Best Practices

### Development
- ✅ Test locally before deploying
- ✅ Use version control (Git)
- ✅ Keep dependencies updated
- ✅ Document changes

### Deployment
- ✅ Use checklist for each deployment
- ✅ Verify after each step
- ✅ Keep ZIP files small (<100MB)
- ✅ Exclude unnecessary files

### Production
- ✅ Monitor regularly
- ✅ Set up billing alerts
- ✅ Enable CloudWatch logs
- ✅ Have rollback plan
- ✅ Regular backups

### Security
- ✅ Use environment variables for secrets
- ✅ Enable HTTPS (production)
- ✅ Restrict security groups
- ✅ Regular security updates
- ✅ Never commit .env files

---

## 🎓 Learning Path

### Beginner
1. Read AWS_DEPLOYMENT_GUIDE.md completely
2. Follow AWS_CONSOLE_QUICK_GUIDE.md step-by-step
3. Use AWS_DEPLOYMENT_CHECKLIST.md
4. Deploy to free tier t2.micro

### Intermediate
1. Understand Elastic Beanstalk concepts
2. Customize .ebextensions configurations
3. Set up monitoring and alerts
4. Optimize for performance

### Advanced
1. Implement CI/CD pipeline
2. Use multiple environments (dev, staging, prod)
3. Set up auto-scaling
4. Implement blue-green deployments
5. Use RDS for database
6. Configure custom domain with HTTPS

---

## 📈 Scaling Your Application

### When to Scale

Scale up when:
- Response times > 2 seconds
- CPU usage > 70%
- Memory usage > 80%
- User complaints about speed

### How to Scale

**Vertical Scaling** (Bigger instance):
```
Configuration → Instances → Edit
Change: t2.micro → t2.small → t2.medium
```

**Horizontal Scaling** (More instances):
```
Configuration → Capacity → Edit
Environment type: Load balanced
Min instances: 2, Max instances: 4
```

---

## 🔐 Security Checklist

- [ ] Environment variables used for secrets
- [ ] No sensitive data in logs
- [ ] HTTPS enabled (production)
- [ ] Security groups properly configured
- [ ] IAM roles follow least privilege
- [ ] Regular security updates
- [ ] Backup strategy in place
- [ ] Monitoring and alerts configured

---

## 💡 Tips & Tricks

### Faster Deployments
- Keep ZIP files small
- Use .ebignore effectively
- Specify exact package versions
- Remove unused dependencies

### Cost Savings
- Use t2.micro for development
- Terminate when not in use
- Single instance for low traffic
- Monitor with Cost Explorer
- Set up billing alerts

### Better Performance
- Use t2.small or larger for production
- Enable caching
- Optimize database queries
- Use CDN for static files
- Monitor and optimize bottlenecks

### Easier Debugging
- Enable CloudWatch logs
- Add logging to your code
- Test locally first
- Use version control
- Keep deployment history

---

## 🎉 Success Stories

After successful deployment, you can:

- ✅ Access your app from anywhere
- ✅ Share URL with users worldwide
- ✅ Scale as needed
- ✅ Monitor performance
- ✅ Update easily
- ✅ Focus on features, not infrastructure

---

## 📝 Deployment Log Template

Keep track of your deployments:

```
Date: _______________
Version: _______________
Changes: _______________
Deployment Time: _______________
Issues: _______________
Resolution: _______________
Status: _______________
```

---

## 🚀 Ready to Deploy?

1. **Choose your guide**:
   - First time? → AWS_DEPLOYMENT_GUIDE.md
   - Quick deploy? → AWS_CONSOLE_QUICK_GUIDE.md
   - Need checklist? → AWS_DEPLOYMENT_CHECKLIST.md

2. **Prepare your files**:
   - Create ZIP file
   - Verify required files
   - Have API keys ready

3. **Start deploying**:
   - Follow the guide step-by-step
   - Check off items in checklist
   - Verify each step

4. **After deployment**:
   - Test thoroughly
   - Monitor for 24 hours
   - Collect feedback
   - Optimize as needed

---

## 📞 Quick Links

- **AWS Console**: https://console.aws.amazon.com/
- **Elastic Beanstalk**: https://console.aws.amazon.com/elasticbeanstalk/
- **EC2**: https://console.aws.amazon.com/ec2/
- **Billing**: https://console.aws.amazon.com/billing/
- **Support**: https://console.aws.amazon.com/support/
- **Documentation**: https://docs.aws.amazon.com/

---

**Good luck with your deployment! 🚀**

If you encounter any issues, refer to AWS_TROUBLESHOOTING_GUIDE.md or reach out for help.
