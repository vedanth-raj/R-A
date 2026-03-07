# 🔧 AWS Deployment Troubleshooting Guide

Quick solutions to common AWS deployment issues.

---

## 🚨 CRITICAL ISSUES

### Issue 1: Environment Creation Failed

**Symptoms:**
- Environment stuck in "Creating" status
- Red error message appears
- Environment health shows "Severe"

**Solutions:**

1. **Check Service Roles**
   - Go to IAM Console
   - Verify `aws-elasticbeanstalk-service-role` exists
   - Verify `aws-elasticbeanstalk-ec2-role` exists
   - If missing, recreate environment and let AWS create them

2. **Check Region Capacity**
   - Some regions may have capacity issues
   - Try different region (e.g., US East 1, US West 2)

3. **Verify Account Limits**
   - Go to Service Quotas
   - Check EC2 instance limits
   - Request increase if needed

4. **Review Error Logs**
   - Go to Events tab
   - Look for specific error messages
   - Address the root cause

**Quick Fix:**
```
1. Terminate failed environment
2. Wait 5 minutes
3. Try creating again with same settings
```

---

### Issue 2: 502 Bad Gateway Error

**Symptoms:**
- Browser shows "502 Bad Gateway"
- Application won't load
- Environment health is "Degraded"

**Solutions:**

1. **Check Application Entry Point**
   - Verify `application.py` exists in root
   - Ensure it contains: `application = app`
   - Check file name is exactly `application.py`

2. **Verify Requirements**
   - Ensure `gunicorn` is in requirements.txt
   - Ensure `eventlet` is in requirements.txt
   - Check all dependencies are listed

3. **Check Logs**
   ```
   Environment → Logs → Request Logs → Last 100 Lines
   ```
   - Look for Python import errors
   - Check for missing modules
   - Verify syntax errors

4. **Increase Timeout**
   - Create `.ebextensions/python.config`:
   ```yaml
   option_settings:
     aws:elasticbeanstalk:command:
       Timeout: 600
   ```

5. **Check Port Configuration**
   - Application must listen on port 5000
   - Verify in application.py: `port=5000`

**Quick Fix:**
```python
# Ensure application.py has:
from web_app import app, socketio

application = app

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
```

---

### Issue 3: Application Won't Start

**Symptoms:**
- Environment health "Severe" or "Degraded"
- Logs show Python errors
- Application never becomes accessible

**Solutions:**

1. **Check Python Version**
   - Verify platform is Python 3.11
   - Check requirements.txt compatibility
   - Update incompatible packages

2. **Review Import Errors**
   - Check logs for "ModuleNotFoundError"
   - Add missing packages to requirements.txt
   - Verify package names are correct

3. **Check Environment Variables**
   - Configuration → Software → Environment properties
   - Verify GEMINI_API_KEY is set
   - Verify no typos in variable names

4. **Test Locally First**
   ```bash
   # On your local machine:
   python application.py
   # Should start without errors
   ```

5. **Check File Structure**
   - Ensure all imports can be resolved
   - Verify relative paths are correct
   - Check templates/ and static/ folders exist

**Quick Fix:**
```
1. Download logs
2. Find first error in logs
3. Fix that specific error
4. Redeploy with updated code
```

---

## ⚠️ COMMON ISSUES

### Issue 4: Environment Variables Not Working

**Symptoms:**
- Application can't access API keys
- Errors about missing configuration
- Features requiring API keys fail

**Solutions:**

1. **Verify Variables Are Set**
   - Configuration → Software → Edit
   - Check Environment properties section
   - Ensure no extra spaces in keys/values

2. **Check Variable Names**
   - Must match exactly what code expects
   - Case-sensitive: `GEMINI_API_KEY` not `gemini_api_key`

3. **Restart Environment**
   - After adding variables, environment must restart
   - Wait for status to return to "Ok"

4. **Test in Code**
   ```python
   import os
   print(f"API Key: {os.getenv('GEMINI_API_KEY', 'NOT SET')}")
   ```

**Quick Fix:**
```
1. Configuration → Software → Edit
2. Add environment variables
3. Click Apply
4. Wait 2-3 minutes for restart
5. Check logs to verify variables are loaded
```

---

### Issue 5: Out of Memory / Application Crashes

**Symptoms:**
- Application randomly crashes
- 502 errors appear intermittently
- Logs show memory errors
- Environment health fluctuates

**Solutions:**

1. **Upgrade Instance Type**
   - Configuration → Instances → Edit
   - Change from t2.micro (1GB) to t2.small (2GB)
   - Or t2.medium (4GB) for heavy usage

2. **Optimize Code**
   - Process papers in smaller batches
   - Clear memory after processing
   - Use generators instead of lists

3. **Add Swap Space**
   - Create `.ebextensions/swap.config`:
   ```yaml
   commands:
     01_setup_swap:
       command: |
         /bin/dd if=/dev/zero of=/var/swapfile bs=1M count=2048
         /sbin/mkswap /var/swapfile
         /sbin/swapon /var/swapfile
   ```

4. **Monitor Memory Usage**
   - Monitoring → View graphs
   - Check memory usage patterns
   - Identify memory-intensive operations

**Quick Fix:**
```
Configuration → Instances → Edit
Change instance type to t2.small
Click Apply
Wait for restart
```

---

### Issue 6: WebSocket Connection Failed

**Symptoms:**
- Real-time updates don't work
- Console shows WebSocket errors
- Progress bars don't update

**Solutions:**

1. **Check WebSocket Configuration**
   - Verify `.ebextensions/03_websocket.config` exists
   - Ensure it's included in ZIP file

2. **Verify Eventlet**
   - Check `eventlet` is in requirements.txt
   - Version should be >= 0.33.0

3. **Check Nginx Configuration**
   - Create `.ebextensions/03_websocket.config`:
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
             }
         }
   ```

4. **Test WebSocket Locally**
   ```javascript
   // In browser console:
   const socket = io();
   socket.on('connect', () => console.log('Connected!'));
   ```

**Quick Fix:**
```
1. Add .ebextensions/03_websocket.config
2. Add eventlet to requirements.txt
3. Recreate ZIP file
4. Deploy updated version
```

---

### Issue 7: Slow Performance

**Symptoms:**
- Pages load slowly
- Operations take too long
- Timeouts occur

**Solutions:**

1. **Upgrade Instance**
   - Use t2.small or t2.medium
   - More CPU and memory = better performance

2. **Enable Caching**
   - Cache API responses
   - Cache processed papers
   - Use Redis (optional)

3. **Optimize Database Queries**
   - Add indexes
   - Reduce query complexity
   - Use pagination

4. **Use CDN for Static Files**
   - CloudFront for CSS/JS
   - Reduces load on application

5. **Profile Your Code**
   ```python
   import time
   start = time.time()
   # Your code here
   print(f"Took {time.time() - start} seconds")
   ```

**Quick Fix:**
```
Configuration → Instances → Edit
Change to t2.small or t2.medium
Click Apply
```

---

### Issue 8: Deployment Takes Too Long

**Symptoms:**
- Deployment stuck at "Updating"
- Takes more than 10 minutes
- Eventually times out

**Solutions:**

1. **Reduce ZIP File Size**
   - Remove unnecessary files
   - Exclude data/ folder
   - Exclude .git/ folder
   - Keep ZIP under 100MB

2. **Check .ebignore**
   ```
   .git/
   .venv/
   venv/
   __pycache__/
   *.pyc
   data/
   *.log
   ```

3. **Simplify Dependencies**
   - Remove unused packages from requirements.txt
   - Use specific versions (faster resolution)

4. **Check Network**
   - Ensure stable internet connection
   - Try uploading from different network

**Quick Fix:**
```
1. Create smaller ZIP file
2. Exclude data/ and .git/
3. Upload again
```

---

### Issue 9: Can't Access Application URL

**Symptoms:**
- URL doesn't load
- Connection timeout
- DNS errors

**Solutions:**

1. **Check Environment Status**
   - Must be green "Ok"
   - If yellow/red, check logs

2. **Verify Security Group**
   - Configuration → Instances → Edit
   - Ensure port 80 is open
   - Check inbound rules

3. **Check DNS**
   - Wait 5-10 minutes for DNS propagation
   - Try accessing from different device
   - Clear browser cache

4. **Verify Region**
   - Ensure you're in correct region
   - URL includes region name

**Quick Fix:**
```
1. Wait 5 minutes
2. Clear browser cache
3. Try incognito/private mode
4. Check environment status is "Ok"
```

---

### Issue 10: High Costs / Unexpected Charges

**Symptoms:**
- Bill higher than expected
- Free tier exceeded
- Multiple resources running

**Solutions:**

1. **Check Running Resources**
   - EC2 instances
   - Load balancers
   - RDS databases
   - S3 storage

2. **Review Billing Dashboard**
   - Identify highest costs
   - Check by service
   - Look for unexpected resources

3. **Terminate Unused Resources**
   - Stop/terminate environments not in use
   - Delete old application versions
   - Clean up S3 buckets

4. **Set Up Billing Alerts**
   - Billing → Budgets
   - Create budget alert
   - Set threshold (e.g., $10)

5. **Use Cost Explorer**
   - Analyze spending patterns
   - Identify cost drivers
   - Optimize accordingly

**Quick Fix:**
```
1. Go to EC2 Console
2. Check running instances
3. Terminate unused instances
4. Go to Elastic Beanstalk
5. Terminate unused environments
```

---

## 🔍 DEBUGGING TECHNIQUES

### How to Read Logs

1. **Access Logs**
   ```
   Environment → Logs → Request Logs → Last 100 Lines
   ```

2. **Look for Key Patterns**
   - `ERROR` - Critical errors
   - `WARNING` - Potential issues
   - `ModuleNotFoundError` - Missing dependency
   - `ImportError` - Import issues
   - `Traceback` - Python errors

3. **Common Log Locations**
   - `/var/log/eb-engine.log` - Deployment logs
   - `/var/log/web.stdout.log` - Application output
   - `/var/log/nginx/error.log` - Nginx errors

### How to Test Locally

```bash
# 1. Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# 2. Set environment variables
export GEMINI_API_KEY=your_key  # Linux/Mac
# or
set GEMINI_API_KEY=your_key  # Windows

# 3. Run application
python application.py

# 4. Test in browser
# Open: http://localhost:5000
```

### How to Debug in Production

1. **Enable Debug Logging**
   - Add to environment variables:
   ```
   FLASK_DEBUG=1
   LOG_LEVEL=DEBUG
   ```

2. **Add Print Statements**
   ```python
   print(f"DEBUG: Variable value = {variable}")
   ```

3. **Check CloudWatch Logs**
   - More detailed than EB logs
   - Real-time streaming
   - Better search capabilities

---

## 📞 WHEN TO CONTACT AWS SUPPORT

Contact support if:
- [ ] Issue persists after trying all solutions
- [ ] AWS service appears to be down
- [ ] Account-level issues (billing, limits)
- [ ] Security concerns
- [ ] Need quota increases

**Before Contacting:**
1. Document the issue clearly
2. Collect relevant logs
3. Note steps to reproduce
4. List what you've already tried

**Support Tiers:**
- Basic (Free): Account and billing
- Developer ($29/month): Technical support
- Business ($100/month): 24/7 support

---

## ✅ PREVENTION CHECKLIST

Avoid issues by:
- [ ] Testing locally before deploying
- [ ] Using version control (Git)
- [ ] Keeping dependencies updated
- [ ] Monitoring regularly
- [ ] Setting up alerts
- [ ] Documenting changes
- [ ] Having rollback plan
- [ ] Regular backups

---

## 🎯 QUICK REFERENCE

### Most Common Fixes

1. **502 Error** → Check application.py and logs
2. **Won't Start** → Check requirements.txt
3. **No API Access** → Check environment variables
4. **Out of Memory** → Upgrade instance type
5. **Slow** → Upgrade instance or optimize code
6. **WebSocket Fails** → Add websocket config
7. **High Costs** → Terminate unused resources

### Essential Commands

```bash
# View logs
Environment → Logs → Request Logs

# Check health
Environment → Monitoring

# Update code
Application Versions → Upload → Deploy

# Change instance
Configuration → Instances → Edit

# Add variables
Configuration → Software → Edit
```

---

## 🆘 EMERGENCY PROCEDURES

### If Everything Breaks

1. **Don't Panic**
2. **Check environment status**
3. **Download logs immediately**
4. **Terminate environment if needed**
5. **Recreate from scratch**
6. **Restore from backup**

### Rollback Procedure

```
1. Go to Application Versions
2. Find previous working version
3. Click "Deploy"
4. Select your environment
5. Confirm deployment
6. Wait for rollback to complete
```

---

**Need More Help?**
- AWS Documentation: https://docs.aws.amazon.com/elasticbeanstalk/
- AWS Forums: https://forums.aws.amazon.com/
- Stack Overflow: Tag `aws-elastic-beanstalk`
- AWS Support: https://console.aws.amazon.com/support/
