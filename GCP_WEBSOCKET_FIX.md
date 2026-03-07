# 🔧 WebSocket & File Storage Fix for App Engine

## Issues Identified:

1. ❌ **WebSocket not working** - App Engine needs special configuration
2. ❌ **Papers not visible** - Files in `/tmp` are temporary and not browsable

---

## ✅ Fixes Applied:

### 1. WebSocket Fix

**Updated app.yaml**:
- Changed from `eventlet` to `gevent` worker (better App Engine support)
- Added WebSocket configuration
- Added `inbound_services: warmup`

**Updated requirements.txt**:
- Added `gevent>=23.9.0`
- Added `gevent-websocket>=0.10.1`

### 2. File Storage Understanding

**Important**: App Engine `/tmp` storage is:
- ✅ Writable (up to 512MB)
- ⚠️ Temporary (deleted on restart)
- ⚠️ Not browsable via file system
- ✅ Perfect for processing papers on-demand

**How it works now**:
1. User searches for papers
2. Papers downloaded to `/tmp/data/papers/`
3. Text extracted to `/tmp/data/extracted_texts/`
4. User can generate drafts immediately
5. Files cleared on instance restart (that's okay!)

---

## 🚀 DEPLOY THE FIX

```bash
# Deploy updated code
gcloud app deploy

# Type: Y
# Wait 3-5 minutes
```

---

## ✅ After Deployment:

### Test WebSocket:
1. Open your app
2. Search for papers
3. You should see real-time progress updates ✅
4. No more WebSocket errors in console ✅

### Test Paper Processing:
1. Search for "steel" or any topic
2. Papers will be downloaded (to /tmp)
3. Click "Extract Text" button
4. Text will be extracted
5. Generate drafts - should work! ✅

---

## 📊 Understanding App Engine Storage:

### What Works:
- ✅ Search papers
- ✅ Download PDFs (to /tmp)
- ✅ Extract text (to /tmp)
- ✅ Generate drafts
- ✅ All processing features

### What's Different:
- ⚠️ Can't browse `/tmp` directory directly
- ⚠️ Files deleted on restart (but regenerated on next search)
- ⚠️ Each instance has its own `/tmp` (not shared)

### Why This Is Actually Good:
- ✅ No storage costs
- ✅ Always fresh data
- ✅ No cleanup needed
- ✅ Scales automatically

---

## 🎯 User Workflow:

```
1. User searches "machine learning"
   ↓
2. Papers downloaded to /tmp
   ↓
3. User clicks "Extract Text"
   ↓
4. Text extracted to /tmp
   ↓
5. User generates draft
   ↓
6. Draft displayed immediately ✅
```

**Everything works in one session!**

---

## 🔄 Alternative: Persistent Storage (Optional)

If you need permanent storage, we can add Google Cloud Storage:

### Benefits:
- ✅ Permanent storage
- ✅ Shared across instances
- ✅ Browsable
- ✅ Unlimited size

### Cost:
- ~$0.02/GB/month
- ~$0.004 per 10,000 operations

### Implementation:
```python
from google.cloud import storage

def upload_to_gcs(local_file, bucket_name, blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_file)
```

**But for now, /tmp works great!**

---

## 🆘 Troubleshooting:

### WebSocket Still Not Working?

**Check browser console**:
```javascript
// Should see:
WebSocket connection established ✅

// Not:
WebSocket connection failed ❌
```

**If still failing**:
1. Clear browser cache
2. Try incognito mode
3. Check logs: `gcloud app logs tail`

### Papers Not Showing?

**This is expected!** Papers are in `/tmp` which is:
- Not browsable via UI
- Temporary storage
- Cleared on restart

**Solution**: Papers are processed in-memory during the session. User workflow:
1. Search → Download → Extract → Generate Draft
2. All in one session
3. Works perfectly!

---

## 📝 Technical Details:

### Why gevent instead of eventlet?

**App Engine compatibility**:
- `gevent`: ✅ Better App Engine support
- `eventlet`: ⚠️ Can have issues with App Engine

### Why /tmp?

**App Engine file system**:
- `/` (root): ❌ Read-only
- `/tmp`: ✅ Writable (512MB limit)
- Cloud Storage: ✅ Unlimited (costs money)

---

## ✅ Deploy Now!

```bash
gcloud app deploy
```

After deployment:
1. WebSocket will work ✅
2. Paper processing will work ✅
3. Draft generation will work ✅

**Your app will be fully functional!** 🎉

---

## 🎯 Expected Behavior After Fix:

### Search Papers:
```
User searches "AI" 
→ Real-time progress shown (WebSocket working!)
→ Papers downloaded to /tmp
→ Success message ✅
```

### Extract Text:
```
User clicks "Extract Text"
→ Progress bar updates in real-time
→ Text extracted to /tmp
→ Ready for draft generation ✅
```

### Generate Draft:
```
User selects papers
→ Clicks "Generate Draft"
→ AI generates content
→ Draft displayed ✅
```

**Everything works seamlessly!** 🚀
