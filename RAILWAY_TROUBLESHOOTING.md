# 🚂 Railway Deployment Troubleshooting Guide

## Common Build Failures and Solutions

### 1. **"ModuleNotFoundError: No module named 'whitenoise'"**

**Solution:**

- Ensure `whitenoise==6.9.0` is in `requirements_production.txt`
- Check that the virtual environment is activated locally
- Run: `pip install whitenoise` locally to test

### 2. **"ModuleNotFoundError: No module named 'django'"**

**Solution:**

- Check that `Django==3.0.5` is in `requirements_production.txt`
- Ensure all dependencies are listed in requirements file
- Test locally: `pip install -r requirements_production.txt`

### 3. **"Build failed - Python version not found"**

**Solution:**

- Ensure `runtime.txt` contains: `python-3.9.18`
- Check `nixpacks.toml` has correct Python version
- Railway will auto-detect Python 3.9

### 4. **"Database connection failed"**

**Solution:**

- Add PostgreSQL plugin in Railway dashboard
- Ensure `DATABASE_URL` environment variable is set
- Check that `dj-database-url` and `psycopg2-binary` are in requirements

### 5. **"Static files not found"**

**Solution:**

- Ensure `STATIC_ROOT` is set correctly in settings
- Run `python manage.py collectstatic --noinput` during build
- Check that `whitenoise` is configured properly

## 🔧 Step-by-Step Railway Deployment Fix

### Step 1: Verify Files

Ensure these files exist in your project root:

```
✅ railway.json
✅ requirements_production.txt
✅ build.sh
✅ nixpacks.toml
✅ Procfile
✅ runtime.txt
```

### Step 2: Check Requirements

Your `requirements_production.txt` should contain:

```
Django==3.0.5
whitenoise==6.9.0
gunicorn==20.0.4
dj-database-url==0.5.0
psycopg2-binary==2.8.6
django-widget-tweaks==1.4.8
Pillow==8.0.1
```

### Step 3: Environment Variables

In Railway dashboard, set these variables:

```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-app-name.railway.app
DATABASE_URL=your-database-url (auto-provided by Railway)
```

### Step 4: Database Setup

1. Add PostgreSQL plugin in Railway dashboard
2. Railway will automatically provide `DATABASE_URL`
3. Run migrations: `python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`

## 🚨 Debugging Steps

### 1. Check Railway Logs

- Go to Railway dashboard
- Click on your project
- Go to "Deployments" tab
- Click on latest deployment
- Check "Build Logs" and "Deploy Logs"

### 2. Test Locally First

```bash
# Install production dependencies
pip install -r requirements_production.txt

# Test collectstatic
python manage.py collectstatic --noinput

# Test with production settings
export DEBUG=False
export SECRET_KEY=test-key
python manage.py check --deploy
```

### 3. Common Error Messages

**"Build failed - Command not found"**

- Check that `build.sh` is executable
- Ensure proper line endings (Unix format)

**"Port already in use"**

- Railway handles this automatically
- Check your start command in `railway.json`

**"Permission denied"**

- Ensure files have proper permissions
- Check that `build.sh` is executable

## 🔄 Redeployment Process

### If Build Fails:

1. Check the logs for specific error messages
2. Fix the issue locally first
3. Commit and push changes
4. Railway will automatically redeploy

### Manual Redeploy:

1. Go to Railway dashboard
2. Click "Deploy" button
3. Monitor the build logs
4. Check deployment logs

## 📞 Getting Help

### Railway Support:

- Check Railway documentation: https://docs.railway.app
- Join Railway Discord: https://discord.gg/railway
- Contact Railway support through dashboard

### Common Issues:

1. **Build timeout**: Reduce build complexity
2. **Memory issues**: Optimize requirements
3. **Database connection**: Check PostgreSQL plugin
4. **Static files**: Ensure whitenoise configuration

## ✅ Success Checklist

- [ ] Build completes without errors
- [ ] Application starts successfully
- [ ] Database migrations run
- [ ] Static files load correctly
- [ ] Admin interface accessible
- [ ] All forms work properly
- [ ] File uploads function
- [ ] Email settings configured (optional)

## 🎯 Quick Fix Commands

If you need to make quick changes:

```bash
# Update requirements
pip freeze > requirements_production.txt

# Test locally
python manage.py check --deploy

# Commit and push
git add .
git commit -m "Fix Railway deployment"
git push origin main
```

**Remember**: Railway will automatically redeploy when you push to your main branch!
