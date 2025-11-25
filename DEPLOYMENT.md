# Deployment Guide for Education Career Analysis System

## Quick Start Options

### **Option 1: Deploy to Heroku (Recommended for beginners)**

**Prerequisites:**

- Heroku account (free)
- Git installed
- Heroku CLI installed

**Steps:**

1. Initialize git repository:

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. Create Heroku app:

   ```bash
   heroku login
   heroku create your-app-name
   ```

3. Deploy:

   ```bash
   git push heroku main
   ```

4. Initialize database:

   ```bash
   heroku run python -c "from app import init_db; init_db()"
   ```

5. Open your app:
   ```bash
   heroku open
   ```

---

### **Option 2: Deploy to PythonAnywhere (No credit card needed)**

**Steps:**

1. Sign up at www.pythonanywhere.com
2. Go to "Files" tab, upload your project files
3. Create a new web app → Flask framework → Python 3.11
4. Configure WSGI file:
   ```python
   import sys
   path = '/home/yourusername/education_system'
   if path not in sys.path:
       sys.path.append(path)
   from app import app as application
   ```
5. Reload web app
6. Visit your live URL

---

### **Option 3: Deploy to DigitalOcean (Production-grade, $5/month)**

**Steps:**

1. Create DigitalOcean account
2. Create Ubuntu app platform
3. Connect your GitHub repo
4. Set environment variables (if needed)
5. Deploy

---

### **Option 4: Deploy to Railway (Modern & Simple)**

**Steps:**

1. Sign up at railway.app
2. Connect GitHub repo
3. Select Python
4. Auto-deploys on git push

---

## Important Notes Before Deploying

### **Security:**

1. Update `app.py` line with production settings:

   ```python
   if __name__ == '__main__':
       app.run(debug=False)  # Change to False in production
   ```

2. Add secret key to `app.py`:

   ```python
   app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
   ```

3. Move database to proper location or use PostgreSQL

### **Database:**

- SQLite works for small apps but consider PostgreSQL for production
- Add migration script for production database

### **Environment Variables (Heroku/Railway):**

```
SECRET_KEY=your-secure-random-key
DEBUG=False
```

---

## Files Ready for Deployment

✅ `Procfile` - Tells server how to run the app
✅ `requirements.txt` - Python dependencies
✅ `app.py` - Main Flask application
✅ `ml_model.py` - ML model loading
✅ `.gitignore` - Excludes unnecessary files

---

## Which Option Should You Choose?

| Platform             | Cost      | Setup Time | Best For                         |
| -------------------- | --------- | ---------- | -------------------------------- |
| **Heroku**           | Free/Paid | 5 min      | Small projects, quick testing    |
| **PythonAnywhere**   | Free/Paid | 5 min      | Solo projects, learning          |
| **Railway**          | Free/Paid | 5 min      | Modern stack, GitHub integration |
| **DigitalOcean**     | $5/month  | 15 min     | Production apps, more control    |
| **AWS/Google Cloud** | Varies    | 30+ min    | Large scale, enterprise          |

---

## After Deployment

1. Test all features (login, pathways, recommendations)
2. Monitor errors in platform logs
3. Set up automatic backups if using database
4. Monitor performance and costs

Need help with any specific platform?
