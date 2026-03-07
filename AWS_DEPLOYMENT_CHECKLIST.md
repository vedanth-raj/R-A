# ✅ AWS Deployment Checklist

Use this checklist to ensure a smooth deployment to AWS.

---

## 📋 PRE-DEPLOYMENT CHECKLIST

### Account Setup
- [ ] AWS account created and verified
- [ ] Credit card added (required even for free tier)
- [ ] Email verified
- [ ] Region selected (recommended: US East N. Virginia)
- [ ] Billing alerts configured (optional but recommended)

### API Keys Ready
- [ ] Gemini API key obtained
- [ ] Semantic Scholar API key obtained (optional)
- [ ] Keys tested locally
- [ ] Keys stored securely (not in code)

### Application Files
- [ ] All Python files present
- [ ] `application.py` exists in root directory
- [ ] `requirements.txt` is complete and up-to-date
- [ ] `templates/` folder with HTML files
- [ ] `static/` folder with CSS/JS files
- [ ] `.ebextensions/` folder configured (if using)
- [ ] `.ebignore` file created

### Local Testing
- [ ] Application runs locally without errors
- [ ] All features work (search, extract, generate)
- [ ] WebSocket connections work
- [ ] No missing dependencies
- [ ] Environment variables tested

### File Preparation
- [ ] ZIP file created with all necessary files
- [ ] ZIP file size < 512MB
- [ ] Excluded: .venv/, .git/, data/, __pycache__/
- [ ] Verified ZIP contents are correct

---

## 🚀 DEPLOYMENT CHECKLIST

### Step 1: AWS Console Access
- [ ] Logged into AWS Console
- [ ] Navigated to Elastic Beanstalk service
- [ ] Correct region selected

### Step 2: Create Application
- [ ] Clicked "Create Application"
- [ ] Application name: `ai-research-agent`
- [ ] Environment name: `ai-research-prod`
- [ ] Platform: Python 3.11 selected
- [ ] ZIP file uploaded successfully
- [ ] Preset: Single instance (free tier) selected

### Step 3: Service Configuration
- [ ] Service role created
- [ ] EC2 instance profile created
- [ ] Key pair created/selected (optional)

### Step 4: Network Configuration
- [ ] VPC selected (default)
- [ ] Public IP enabled
- [ ] Subnet selected
- [ ] Database skipped (for now)

### Step 5: Instance Configuration
- [ ] Instance type selected (t2.micro or t2.small)
- [ ] Root volume configured (10GB)
- [ ] Environment type: Single instance

### Step 6: Monitoring Setup
- [ ] Health reporting: Enhanced
- [ ] Managed updates: Enabled
- [ ] CloudWatch logs: Enabled
- [ ] Log streaming: Enabled

### Step 7: Review and Submit
- [ ] All settings reviewed
- [ ] Submitted for creation
- [ ] Waited for environment creation (10-15 min)
- [ ] Environment status: "Ok" (green)

### Step 8: Environment Variables
- [ ] Navigated to Configuration → Software
- [ ] Added GEMINI_API_KEY
- [ ] Added SEMANTIC_SCHOLAR_API_KEY
- [ ] Added FLASK_ENV=production
- [ ] Added SECRET_KEY
- [ ] Applied changes
- [ ] Waited for restart (2-3 min)

---

## ✅ POST-DEPLOYMENT CHECKLIST

### Verify Deployment
- [ ] Environment status is green "Ok"
- [ ] URL is accessible
- [ ] Application loads in browser
- [ ] No 502/503 errors
- [ ] No console errors in browser

### Test Functionality
- [ ] Search for papers works
- [ ] Papers are downloaded
- [ ] Text extraction works
- [ ] Section analysis works
- [ ] Draft generation works
- [ ] WebSocket real-time updates work
- [ ] All UI elements display correctly

### Check Logs
- [ ] Accessed logs (Logs → Request Logs)
- [ ] No critical errors in logs
- [ ] Application startup successful
- [ ] No missing dependencies errors

### Monitor Performance
- [ ] Checked monitoring dashboard
- [ ] CPU usage reasonable (<50%)
- [ ] Memory usage acceptable
- [ ] Network traffic normal
- [ ] Response times acceptable

### Security Check
- [ ] Environment variables not exposed
- [ ] No sensitive data in logs
- [ ] HTTPS considered (optional)
- [ ] Security group rules reviewed

---

## 💰 COST MANAGEMENT CHECKLIST

### Initial Setup
- [ ] Billing dashboard accessed
- [ ] Current charges reviewed ($0 expected for free tier)
- [ ] Billing alerts configured
- [ ] Budget set (e.g., $10/month alert)
- [ ] Cost Explorer enabled

### Ongoing Monitoring
- [ ] Weekly cost check scheduled
- [ ] Free tier usage monitored
- [ ] Unnecessary resources identified
- [ ] Scaling settings reviewed

### Cost Optimization
- [ ] Using t2.micro for testing
- [ ] Single instance (not load balanced)
- [ ] Auto-scaling disabled (for now)
- [ ] Unused resources terminated

---

## 🔧 TROUBLESHOOTING CHECKLIST

### If Application Won't Start
- [ ] Checked logs for errors
- [ ] Verified application.py exists
- [ ] Confirmed requirements.txt is complete
- [ ] Checked environment variables are set
- [ ] Verified Python version compatibility

### If 502 Bad Gateway
- [ ] Checked application logs
- [ ] Verified gunicorn is in requirements.txt
- [ ] Confirmed application variable exists
- [ ] Checked timeout settings
- [ ] Verified port 5000 is used

### If WebSocket Fails
- [ ] Verified .ebextensions/03_websocket.config exists
- [ ] Checked nginx configuration
- [ ] Confirmed eventlet in requirements.txt
- [ ] Tested WebSocket connection in browser console

### If Out of Memory
- [ ] Checked memory usage in monitoring
- [ ] Upgraded to t2.small if needed
- [ ] Optimized code for memory usage
- [ ] Reduced batch sizes

### If Slow Performance
- [ ] Checked CPU usage
- [ ] Reviewed response times
- [ ] Considered upgrading instance type
- [ ] Optimized database queries (if any)

---

## 📊 MONITORING CHECKLIST

### Daily Checks (First Week)
- [ ] Environment health status
- [ ] Application accessibility
- [ ] Error logs review
- [ ] Cost accumulation

### Weekly Checks
- [ ] Performance metrics review
- [ ] Cost analysis
- [ ] User feedback collection
- [ ] Feature usage analysis

### Monthly Checks
- [ ] Security updates applied
- [ ] Dependencies updated
- [ ] Backup strategy reviewed
- [ ] Scaling needs assessed

---

## 🔄 UPDATE CHECKLIST

### Before Updating
- [ ] Code tested locally
- [ ] Changes documented
- [ ] Version number incremented
- [ ] Backup of current version
- [ ] Rollback plan prepared

### During Update
- [ ] New ZIP file created
- [ ] Uploaded to Application Versions
- [ ] Version labeled correctly
- [ ] Deployed to environment
- [ ] Waited for deployment completion

### After Update
- [ ] Environment status checked
- [ ] Application tested
- [ ] Logs reviewed for errors
- [ ] Performance verified
- [ ] Users notified (if needed)

---

## 🛑 SHUTDOWN CHECKLIST

### Temporary Shutdown
- [ ] Reason documented
- [ ] Users notified
- [ ] Data backed up (if needed)
- [ ] Environment terminated
- [ ] Costs stopped

### Permanent Shutdown
- [ ] All environments terminated
- [ ] Application deleted
- [ ] S3 buckets cleaned
- [ ] CloudWatch logs deleted (optional)
- [ ] Key pairs deleted (if not needed)
- [ ] Final cost review

---

## 📞 SUPPORT CHECKLIST

### Before Contacting Support
- [ ] Checked logs thoroughly
- [ ] Reviewed documentation
- [ ] Searched Stack Overflow
- [ ] Tried basic troubleshooting
- [ ] Documented the issue

### Information to Provide
- [ ] Environment name
- [ ] Region
- [ ] Error messages
- [ ] Log excerpts
- [ ] Steps to reproduce
- [ ] Expected vs actual behavior

---

## 🎯 OPTIMIZATION CHECKLIST

### Performance Optimization
- [ ] Caching implemented
- [ ] Database queries optimized
- [ ] Static files compressed
- [ ] CDN considered (optional)
- [ ] Load testing performed

### Cost Optimization
- [ ] Right-sized instance type
- [ ] Unused resources removed
- [ ] Reserved instances considered (long-term)
- [ ] Spot instances evaluated (if applicable)

### Security Optimization
- [ ] HTTPS enabled
- [ ] Security groups tightened
- [ ] IAM roles reviewed
- [ ] Secrets Manager used (optional)
- [ ] Regular security audits scheduled

---

## ✅ FINAL SUCCESS CHECKLIST

### Deployment Complete When:
- [x] Environment is healthy (green)
- [x] Application is accessible via URL
- [x] All features work correctly
- [x] No errors in logs
- [x] Performance is acceptable
- [x] Costs are within budget
- [x] Monitoring is set up
- [x] Backup plan exists
- [x] Documentation is complete
- [x] Team is trained (if applicable)

---

## 🎉 CONGRATULATIONS!

If all items are checked, your deployment is successful!

**Next Steps**:
1. Share URL with users
2. Monitor for first 24 hours
3. Collect feedback
4. Plan improvements
5. Enjoy your deployed application!

---

**Need Help?** Refer to:
- AWS_DEPLOYMENT_GUIDE.md (detailed guide)
- AWS_CONSOLE_QUICK_GUIDE.md (visual guide)
- AWS Documentation
