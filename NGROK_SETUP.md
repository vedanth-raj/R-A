# Ngrok Deployment Guide

## Quick Setup (5 minutes)

### Step 1: Install Ngrok

1. Go to https://ngrok.com/download
2. Download ngrok for Windows
3. Extract `ngrok.exe` to this project folder

### Step 2: Get Auth Token

1. Sign up at https://ngrok.com (free account)
2. Go to https://dashboard.ngrok.com/get-started/your-authtoken
3. Copy your auth token
4. Run in terminal:
   ```
   ngrok config add-authtoken YOUR_TOKEN_HERE
   ```

### Step 3: Deploy

**Option A: Using Batch Script (Easiest)**
```
start_ngrok.bat
```

**Option B: Using Python Script**
```
python deploy_ngrok.py
```

**Option C: Manual (Two Terminals)**

Terminal 1 - Start Flask:
```
python web_app.py
```

Terminal 2 - Start Ngrok:
```
ngrok http 5000
```

### Step 4: Access Your App

1. Look for the "Forwarding" line in ngrok output
2. Copy the URL (e.g., `https://abc123.ngrok.io`)
3. Share this URL - anyone can access your app!

## Features

- ✅ Full SocketIO support (real-time updates)
- ✅ All features working (search, extract, generate drafts)
- ✅ Public URL accessible from anywhere
- ✅ HTTPS enabled automatically

## Stopping the App

Press `Ctrl+C` in both terminals (or close the windows)

## Troubleshooting

**"ngrok not found"**
- Make sure ngrok.exe is in this folder or added to PATH
- Try running: `.\ngrok.exe http 5000` directly

**"Failed to start tunnel"**
- Make sure you've added your auth token
- Check if port 5000 is already in use

**Flask app not starting**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check if .env file exists with API keys

## Notes

- Free ngrok accounts have session limits (2 hours)
- URL changes each time you restart ngrok
- For permanent URL, upgrade to ngrok paid plan
