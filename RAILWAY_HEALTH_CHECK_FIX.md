# Railway Health Check Fix Guide

## 🚨 Current Issue: Health Check Failure

The Railway health check is failing. Here's how to fix it:

## 🔧 Quick Fix Steps

### 1. Environment Variables

Make sure these are set in Railway:

```
DJANGO_SETTINGS_MODULE=bloodbankmanagement.settings_railway
SECRET_KEY=w@k#6^!z8$1b2r4e7u0p9s3c5t!g&h@j*lqzv
```

### 2. Railway Configuration

The `railway.json` is now configured with:

- Health check path: `/` (root)
- Timeout: 600 seconds
- Gunicorn timeout: 120 seconds

### 3. Health Check Endpoints

Two endpoints are available:

- `/health/` - Simple health check
- `/` - Root endpoint (used by Railway)

## 🐛 Troubleshooting

### If Health Check Still Fails:

1. **Check Railway Logs**

   - Go to Railway dashboard
   - Click on your project
   - Check "Deployments" tab
   - Look for error messages

2. **Test Endpoints Manually**

   - Visit: `https://your-app.railway.app/health/`
   - Visit: `https://your-app.railway.app/`
   - Both should return JSON responses

3. **Common Issues & Solutions**

   **Issue: "ModuleNotFoundError: No module named 'whitenoise'"**

   - Solution: Ensure whitenoise is in requirements.txt

   **Issue: "Database is locked"**

   - Solution: This is normal for SQLite in production

   **Issue: "Static files not found"**

   - Solution: Check that collectstatic ran successfully

   **Issue: "Port binding error"**

   - Solution: Ensure gunicorn binds to 0.0.0.0:$PORT

4. **Manual Deployment Test**
   ```bash
   # Test locally with Railway settings
   export DJANGO_SETTINGS_MODULE=bloodbankmanagement.settings_railway
   python manage.py runserver
   ```

## 📋 Deployment Checklist

- [ ] All files committed to GitHub
- [ ] Environment variables set in Railway
- [ ] Railway configuration updated
- [ ] Health check endpoints working
- [ ] Database migrations completed
- [ ] Static files collected

## 🎯 Success Indicators

When working correctly, you should see:

- ✅ Build completed successfully
- ✅ Health check passing
- ✅ Application accessible at Railway URL
- ✅ JSON response at `/health/` endpoint

## 📞 Next Steps

1. Push all changes to GitHub
2. Wait for Railway to redeploy
3. Check Railway logs for any errors
4. Test the health endpoints manually
5. If still failing, check the logs and share error messages

## 🔍 Debug Commands

```bash
# Test health endpoint locally
curl http://localhost:8000/health/

# Test with Railway settings
DJANGO_SETTINGS_MODULE=bloodbankmanagement.settings_railway python manage.py runserver

# Check if all dependencies are installed
pip list | grep -E "(django|gunicorn|whitenoise)"
```
