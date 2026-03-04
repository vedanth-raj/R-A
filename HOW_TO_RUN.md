# 🎯 How to Run Your AI Research Agent

## 🚀 Quick Start (Recommended)

**Just double-click this file:**
```
START_NGROK.bat
```

**What happens:**
1. Flask app starts on port 5000
2. Ngrok creates a public URL
3. You get a link like: `https://xxxxx.ngrok-free.dev`
4. Share that link with anyone!

---

## 📖 Step-by-Step (First Time)

### ✅ Already Done (You're all set!)
- ✅ Ngrok downloaded and extracted
- ✅ Auth token configured
- ✅ Python dependencies installed
- ✅ Environment variables set

### 🎬 Every Time You Want to Run

**Option 1: One-Click (Easiest)**
```
Double-click: START_NGROK.bat
```

**Option 2: Command Line**
```bash
START_NGROK.bat
```

**Option 3: Manual Control (Two Terminals)**

Terminal 1:
```bash
python web_app.py
```

Terminal 2:
```bash
.\ngrok.exe http 5000
```

---

## 🌐 Your Public URL

After starting, look for this in the ngrok window:
```
Forwarding    https://curtailedly-noncleistogamic-thao.ngrok-free.dev -> http://localhost:5000
```

**Note:** The URL changes each time you restart ngrok (free plan limitation)

---

## 📱 Access Points

- **Public URL**: From ngrok output (share with anyone)
- **Local**: http://localhost:5000
- **Ngrok Dashboard**: http://127.0.0.1:4040 (see traffic, requests)

---

## 🛑 How to Stop

- Press `Ctrl+C` in both windows
- Or just close the terminal windows

---

## 🔥 Features Available

✅ **Real-time updates** - SocketIO for live progress
✅ **Paper search** - Semantic Scholar integration
✅ **PDF extraction** - Extract text from papers
✅ **Section analysis** - Intelligent section detection
✅ **Draft generation** - AI-powered research drafts
✅ **Conversational AI** - Chat with your research assistant
✅ **Custom instructions** - Personalize your drafts

---

## 🎨 Deployment Options

### 1. Ngrok (Current - Best for Development)
- ✅ Full features including SocketIO
- ✅ Public URL
- ✅ Easy to use
- ⏱️ 2-hour sessions (free)
- 🔄 URL changes on restart

### 2. Vercel (Alternative - Production)
- ✅ Permanent URL
- ✅ Always online
- ❌ No SocketIO (simplified features)
- 🌐 Already deployed: https://airsearchagent0001.vercel.app

---

## 💡 Tips

1. **Keep both windows open** while using the app
2. **Copy the ngrok URL** before sharing
3. **Restart if needed** - just run START_NGROK.bat again
4. **Check logs** in the Flask window for debugging

---

## 🆘 Troubleshooting

**"Port already in use"**
- Close other Flask apps
- Or restart your computer

**"Ngrok not found"**
- Make sure ngrok.exe is in this folder
- Re-run: `.\ngrok.exe config add-authtoken YOUR_TOKEN`

**"Can't access public URL"**
- Check if both Flask and ngrok are running
- Try the local URL first: http://localhost:5000

---

## 📞 Current Status

- **Ngrok**: ✅ Installed & Configured
- **Auth Token**: ✅ Saved
- **Flask App**: ✅ Ready
- **Dependencies**: ✅ Installed

**You're ready to go! Just run START_NGROK.bat**

---

## 🎓 What You Built

A full-featured AI Research Agent with:
- Paper search and retrieval
- Intelligent text extraction
- AI-powered draft generation
- Real-time conversational interface
- Public web access via ngrok

**Congratulations! 🎉**
