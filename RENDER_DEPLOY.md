# Deploy to Render (Free, No Credit Card)

## ✅ Why Render?

- **Completely Free** - No credit card required
- **Easy Setup** - Takes 5 minutes
- **GitHub Integration** - Auto-deploy on git push
- **Built-in Database** - PostgreSQL available
- **Good Performance** - Suitable for small to medium apps

---

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your Code

1. Make sure you're in the project directory:

```bash
cd education_system
```

2. Verify all files are ready:

```bash
git init
git add .
git commit -m "Initial commit"
```

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Click **Sign Up**
3. Choose **GitHub** (recommended) or Email
4. Authorize Render to access your GitHub

### Step 3: Connect GitHub Repository

1. Push your code to GitHub:

```bash
git remote add origin https://github.com/yourusername/education-system.git
git branch -M main
git push -u origin main
```

2. On Render dashboard, click **New +**
3. Select **Web Service**
4. Connect your GitHub repo
5. Select the `education_system` folder (if in subfolder)

### Step 4: Configure Render Settings

Fill in these settings:

| Field             | Value                             |
| ----------------- | --------------------------------- |
| **Name**          | `education-career-system`         |
| **Environment**   | `Python 3`                        |
| **Region**        | Choose closest to you             |
| **Branch**        | `main`                            |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app`                |

### Step 5: Environment Variables

Click **Environment** tab and add:

```
DEBUG=False
FLASK_ENV=production
```

### Step 6: Deploy!

1. Click **Create Web Service**
2. Render will automatically start deploying
3. Watch the logs for any errors
4. Once complete, you'll get a live URL like:
   ```
   https://education-career-system.onrender.com
   ```

---

## 🗄️ Add Free Database (Optional but Recommended)

### Using Render's Free PostgreSQL:

1. In Render Dashboard, click **New +**
2. Select **PostgreSQL**
3. Name it `education-db`
4. Leave other settings default
5. Create
6. Copy the **Internal Database URL**

### Update your app.py to use PostgreSQL:

Instead of SQLite, add this to your `app.py`:

```python
import psycopg2
from psycopg2 import sql

# Use PostgreSQL in production
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///education_system.db')

if 'postgres' in DATABASE_URL:
    # PostgreSQL connection
    conn = psycopg2.connect(DATABASE_URL)
else:
    # SQLite fallback for local development
    conn = sqlite3.connect('education_system.db')
```

**Note:** For now, SQLite with Render works fine for small projects.

---

## ✅ Verify Deployment

1. Click the live URL from Render dashboard
2. Test these features:
   - [ ] Homepage loads
   - [ ] Register works
   - [ ] Login works
   - [ ] Career pathway loads
   - [ ] Education pathway loads
   - [ ] TESDA pathway loads
   - [ ] Recommendations display
   - [ ] Can save recommendations
   - [ ] Can remove recommendations

---

## 🔄 Auto-Deploy on Updates

1. Make changes locally
2. Commit to Git:
   ```bash
   git add .
   git commit -m "Your message"
   git push origin main
   ```
3. Render automatically redeploys!

---

## 📊 Monitor Your App

On Render Dashboard:

- **Logs** - See error messages
- **Metrics** - Check CPU and memory
- **Events** - Deployment history

---

## 🆘 Troubleshooting

### Deploy fails with error?

1. Check the **Logs** tab
2. Common issues:
   - Missing `gunicorn` in requirements.txt ✅ (Already added)
   - Wrong start command ✅ (Already set)
   - Missing dependencies - Add to `requirements.txt`

### App shows "Service Unavailable"?

1. Wait 1-2 minutes for deployment to complete
2. Check logs for errors
3. Restart the service from dashboard

### Can't access the database?

1. Check the database URL in environment variables
2. Ensure `education_system.db` is being created
3. Use PostgreSQL if issues persist

---

## 🎯 Performance Tips

1. **Scale Down** - Use free tier (limited but fine for testing)
2. **Monitor Logs** - Check for errors regularly
3. **Optimize Database** - Clean old data periodically
4. **Use Caching** - For ML model predictions

---

## 📝 Your Current Status

✅ **requirements.txt** - Ready with gunicorn
✅ **Procfile** - Ready for deployment
✅ **app.py** - Production-ready
✅ **All features** - Working

**You are 100% ready to deploy on Render!**

---

## 🚀 Quick Deploy Checklist

- [ ] GitHub account created
- [ ] Code pushed to GitHub repo
- [ ] Render account created (no credit card!)
- [ ] Web Service connected to GitHub
- [ ] Build and Start commands set
- [ ] Deployed successfully
- [ ] Live URL working
- [ ] All features tested

---

## 📚 Render Docs

- Official Docs: https://render.com/docs
- Python Guide: https://render.com/docs/deploy-python
- Help & Support: https://render.com/help

---

## 🎉 Done!

Your app is now live on Render for **FREE** with **NO credit card required**!

Share your live URL: `https://education-career-system.onrender.com`

**Need help? Let me know!**
