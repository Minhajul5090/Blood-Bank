# Railway Environment Variables Setup

## 🚨 **Error Fixed: "export could not be found"**

The error occurred because Railway containers don't support the `export` command.

## ✅ **Solution Applied:**

1. **Removed `export` from railway.json** - Now uses simple commands
2. **Updated Railway settings** - Handles environment variables properly
3. **Environment variables must be set in Railway dashboard**

## 🔧 **Required Environment Variables:**

In your Railway project dashboard, add these environment variables:

### **Step 1: Go to Railway Dashboard**

1. Open your Railway project
2. Click on your project
3. Go to the **Variables** tab

### **Step 2: Add Environment Variables**

Add these variables:

| Variable Name            | Value                                   |
| ------------------------ | --------------------------------------- |
| `DJANGO_SETTINGS_MODULE` | `bloodbankmanagement.settings_railway`  |
| `SECRET_KEY`             | `w@k#6^!z8$1b2r4e7u0p9s3c5t!g&h@j*lqzv` |

### **Step 3: Save and Redeploy**

1. Click **Save** after adding the variables
2. Railway will automatically redeploy
3. Check the deployment logs

## 📋 **Current railway.json Configuration:**

```json
{
  "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn bloodbankmanagement.wsgi:application --bind 0.0.0.0:$PORT --timeout 120",
  "healthcheckPath": "/health/",
  "healthcheckTimeout": 600
}
```

## 🎯 **Expected Results:**

After setting environment variables:

- ✅ Container creation successful
- ✅ Build completed
- ✅ Health check passing
- ✅ Application accessible

## 🔍 **Troubleshooting:**

If you still see errors:

1. **Check Railway logs** - Look for specific error messages
2. **Verify environment variables** - Make sure they're set correctly
3. **Test health endpoint** - Visit `/health/` on your Railway URL

## 📞 **Next Steps:**

1. Set the environment variables in Railway dashboard
2. Wait for automatic redeployment
3. Test the health endpoint: `https://your-app.railway.app/health/`
4. Check Railway logs for any remaining issues
