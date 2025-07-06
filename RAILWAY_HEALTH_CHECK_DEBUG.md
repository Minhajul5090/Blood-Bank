# Railway Health Check Debugging Guide

## 🚨 **Current Issue: Health Check Failing**

The health check is returning "service unavailable" which means the application isn't starting properly.

## 🔍 **Debugging Steps:**

### **1. Check Railway Logs**

Go to Railway dashboard → Your project → **Deployments** → Click on latest deployment → **View logs**

Look for:

- Import errors
- Database errors
- Port binding issues
- Environment variable issues

### **2. Test Locally with Railway Settings**

```bash
# Set environment variables
export DJANGO_SETTINGS_MODULE=bloodbankmanagement.settings_railway
export SECRET_KEY=w@k#6^!z8$1b2r4e7u0p9s3c5t!g&h@j*lqzv

# Test the application
python manage.py runserver 8000
```

### **3. Test Health Endpoint Locally**

```bash
# Start server
python manage.py runserver

# Test health endpoint
curl http://localhost:8000/health/
```

Expected response:

```json
{
  "status": "healthy",
  "message": "Blood Bank Management System is running",
  "service": "django",
  "version": "1.0.0"
}
```

## 🔧 **Fixes Applied:**

### **1. Updated WSGI Configuration**

- Modified `wsgi.py` to use Railway settings by default
- Added fallback to development settings

### **2. Created Startup Script**

- `start_railway.py` provides better error handling
- Shows environment information during startup
- Handles migrations and static files

### **3. Simplified Health Check**

- Removed all imports except basic Django
- Uses `HttpResponse` instead of `JsonResponse`
- No database dependencies

### **4. Updated Railway Configuration**

```json
{
  "startCommand": "python start_railway.py",
  "healthcheckPath": "/health/",
  "healthcheckTimeout": 600
}
```

## 📋 **Environment Variables Required:**

Make sure these are set in Railway dashboard:

| Variable                 | Value                                   |
| ------------------------ | --------------------------------------- |
| `DJANGO_SETTINGS_MODULE` | `bloodbankmanagement.settings_railway`  |
| `SECRET_KEY`             | `w@k#6^!z8$1b2r4e7u0p9s3c5t!g&h@j*lqzv` |

## 🎯 **Expected Startup Logs:**

When working correctly, you should see:

```
🚀 Starting Blood Bank Management System on Railway...
📋 Environment:
   - DJANGO_SETTINGS_MODULE: bloodbankmanagement.settings_railway
   - PORT: 8000
   - SECRET_KEY: Set
🗄️ Running database migrations...
📁 Collecting static files...
🌐 Starting Gunicorn on port 8000...
```

## 🚨 **Common Issues & Solutions:**

### **Issue: "ModuleNotFoundError: No module named 'whitenoise'"**

**Solution**: Whitenoise is in requirements.txt, but Railway settings disable it

### **Issue: "Database is locked"**

**Solution**: This is normal for SQLite in production

### **Issue: "Port already in use"**

**Solution**: Railway handles port binding automatically

### **Issue: "Environment variable not set"**

**Solution**: Set variables in Railway dashboard

## 📞 **Next Steps:**

1. **Push changes to GitHub**
2. **Set environment variables in Railway**
3. **Check Railway logs for specific errors**
4. **Test health endpoint manually**
5. **Share any error messages from logs**

## 🔍 **Manual Testing:**

After deployment, test these URLs:

- `https://your-app.railway.app/health/` - Should return JSON
- `https://your-app.railway.app/` - Should show homepage
- `https://your-app.railway.app/admin/` - Should show admin login
