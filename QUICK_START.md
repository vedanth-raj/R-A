# 🚀 Quick Start Guide - Running Your App with Ngrok

## ✅ One-Click Start (Easiest Way)

Just double-click this file:
```
START_NGROK.bat
```

That's it! Your app will start and you'll get a public URL.

---

## 📋 Manual Start (If you prefer)

### Option 1: Single Command
Open terminal and run:
```bash
START_NGROK.bat
```

### Option 2: Two Separate Terminals

**Terminal 1 - Start Flask:**
```bash
python web_app.py
```

**Terminal 2 - Start Ngrok:**
```bash
.\ngrok.exe http 5000
```

---

## 🌐 Finding Your Public URL

After starting, look for this line in the ngrok window:
```
Forwarding    https://xxxxx.ngrok-free.dev -> http://localhost:5000
```

The `https://xxxxx.ngrok-free.dev` is your public URL!

---

## 📱 Accessing Your App

- **Public URL**: Share with anyone (from ngrok output)
- **Local**: http://localhost:5000
- **Ngrok Dashboard**: http://127.0.0.1:4040

---

## 🛑 Stopping the App

Press `Ctrl+C` in both terminal windows, or just close them.

---

## 🔧 Troubleshooting

**"ngrok.exe not found"**
- Make sure ngrok.exe is in this folder
- Re-extract from ngrok.zip if needed

**"Port 5000 already in use"**
- Close any other Flask apps running
- Or change port: `.\ngrok.exe http 5001` (and update web_app.py)

**"Authentication failed"**
- Your token is already configured, should work fine
- If issues, run: `.\ngrok.exe config add-authtoken YOUR_TOKEN`

---

## ⚡ Features Available

✅ Real-time updates (SocketIO)
✅ Paper search
✅ PDF text extraction
✅ Draft generation
✅ AI conversation
✅ All original features

---

## 📝 Notes

- Free ngrok sessions last 2 hours
- URL changes each time you restart
- For permanent URL, upgrade ngrok plan
- Your auth token is already saved

---

## 🎯 Current Setup

- Auth Token: ✅ Configured
- Ngrok: ✅ Installed
- Flask App: ✅ Ready
- Status: **Ready to use!**

Just run `START_NGROK.bat` anytime!
