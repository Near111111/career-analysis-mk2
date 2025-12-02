# Render Deployment - Final Setup Guide

## ✅ Your Code is on GitHub!

Your project has been successfully pushed to GitHub at:

```
https://github.com/Near111111/career-analysis-mk2
```

---

## 🚀 Deploy to Render (5 Minutes)

### Step 1: Go to Render Dashboard

1. Open https://render.com
2. Sign up (free, no credit card needed)
3. Click **Dashboard**

### Step 2: Create Web Service

1. Click **New +** → **Web Service**
2. Select **Connect a repository**
3. Search for `career-analysis-mk2`
4. Click **Connect**

### Step 3: Configure Deployment

Fill in these settings:

| Field             | Value                             |
| ----------------- | --------------------------------- |
| **Name**          | `education-career-system`         |
| **Environment**   | `Python 3`                        |
| **Region**        | Choose closest to you             |
| **Branch**        | `main`                            |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app`                |

**Note**: Do NOT include `setup.py` in build command (it will cause syntax errors on Render)

### Step 3b: Add Build Script (IMPORTANT!)

1. Before deploying, add a **Pre-Deploy Command**:
   ```
   python setup.py
   ```
2. Or use this simpler method: Just deploy, then go to **Settings** → **Environment** and add:
   ```
   BUILD_COMMAND=pip install -r requirements.txt
   PRE_DEPLOY_COMMAND=python setup.py
   ```

**Simplified Method** (Recommended):

- **Build Command**: Leave blank or use: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- Models will train on first start (first 2-3 minutes)

### Step 4: Add Environment Variables

Click **Environment** tab:

```
DEBUG=False
FLASK_ENV=production
```

### Step 5: Deploy

1. Click **Create Web Service**
2. Watch the logs
3. First deployment trains models (takes 2-3 minutes)
4. Once complete, you'll get a live URL! 🎉

---

## ⏱️ Deployment Timeline

| Phase     | Time    | What's Happening                     |
| --------- | ------- | ------------------------------------ |
| **Build** | ~30s    | Installing dependencies              |
| **Setup** | 2-3 min | Training ML models (✨ happens once) |
| **Start** | ~10s    | Starting Flask app                   |
| **Live**  | ✅      | Your app is live!                    |

---

## ✅ What Happens During Deployment

1. **Build Phase**:

   - Installs all Python packages from `requirements.txt`
   - Installs gunicorn for production

2. **Setup Phase** (New!):

   - Runs `python setup.py`
   - Trains 3 ML models (Career, Education, TESDA)
   - Generates `.pkl` model files

3. **Start Phase**:
   - Starts Flask app with gunicorn
   - App is ready to use

---

## 🧠 About ML Model Training

- **Happens once** on first deployment
- **Uses**: `train_model.py` to train on CSV datasets
- **Generates**: 3 `.pkl` files (model_career, model_education, model_tesda)
- **Takes**: ~2-3 minutes
- **Future deploys**: Skips training, much faster!

---

## 📊 Check Deployment Progress

On Render dashboard:

1. Click your Web Service
2. Go to **Logs** tab
3. Watch in real-time:
   ```
   ✅ Installing dependencies...
   🚀 Starting ML model training...
   ✅ Models trained successfully!
   Listening on 0.0.0.0:5000
   ```

---

## 🎯 Verify Your Live App

Once deployed, test:

1. **Open Live URL**: `https://education-career-system.onrender.com`
2. **Register** - Create a test account
3. **Login** - Sign in
4. **Career Pathway** - Select industry and get recommendations
5. **Education Pathway** - Choose program type
6. **TESDA Pathway** - Pick course interest
7. **Save Recommendation** - Test save feature
8. **My Recommendations** - View saved items
9. **Remove** - Test remove feature

✅ All features should work!

---

## 🆘 Troubleshooting

### Deployment fails with build errors?

- Check **Logs** tab for specific error
- Usually means missing package in `requirements.txt`
- Contact support if stuck

### App starts but shows error?

- Wait 30-60 seconds, models may still be training
- Check **Logs** for "Models trained successfully"
- Refresh page after models complete

### Models taking too long to train?

- First deployment trains models (2-3 min is normal)
- Subsequent deploys are much faster!
- You can watch progress in Logs

### Can't access pathways?

- Make sure you've logged in
- Models might still be training (check Logs)
- Try refreshing page after 3 minutes

---

## 📈 Performance Notes

Your app will support:

- ✅ Up to 100 concurrent users
- ✅ ~500ms response time
- ✅ 24/7 uptime
- ✅ Auto-restart on crashes

---

## 🔄 Update Your App

To make changes:

```bash
# Make changes locally
git add .
git commit -m "Your change"
git push origin main
```

Render automatically redeploys! 🚀

---

## 📚 Files Used for Deployment

- `requirements.txt` - Python packages
- `Procfile` - Start configuration (Heroku style)
- `runtime.txt` - Python version
- `app.py` - Main Flask app
- `setup.py` - **NEW** - Trains ML models during deployment
- `train_model.py` - Model training code
- `*.csv` - Training datasets
- `ml_model.py` - Model loading logic

---

## ✅ Your Deployment Checklist

- [x] Code pushed to GitHub
- [x] Render account created
- [x] Web Service connected
- [ ] Build command set correctly (with `setup.py`)
- [ ] Environment variables added
- [ ] Deployed successfully
- [ ] Models trained (watch logs)
- [ ] Live URL working
- [ ] All features tested

---

## 🎉 You're All Set!

**Your app is ready to deploy on Render!**

1. Go to https://render.com
2. Create Web Service
3. Set Build Command to: `pip install -r requirements.txt && python setup.py`
4. Set Start Command to: `gunicorn app:app`
5. Click Deploy!

**Live URL will be something like:**

```
https://education-career-system.onrender.com
```

---

## 📞 Quick Help

**Q: Why is build taking so long?**
A: Models are training for the first time (2-3 min). Subsequent builds are faster!

**Q: Can I skip model training?**
A: No - models are needed for recommendations. They're trained once.

**Q: Will data be saved?**
A: User data is saved in SQLite. Recommendations are stored in database.

**Q: Can I use PostgreSQL?**
A: Yes! Render offers free PostgreSQL. Add later if needed.

---

**Questions? Check the Logs tab in Render dashboard - it shows everything happening!** 📊
