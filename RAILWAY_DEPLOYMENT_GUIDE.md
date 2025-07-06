# Railway Deployment Guide for Blood Bank Management System

## 🚀 Quick Deploy to Railway

### Step 1: Prepare Your Repository

1. Make sure all changes are committed to your GitHub repository
2. Ensure you have the following files in your project root:
   - `railway.json` - Railway configuration
   - `requirements.txt` - Python dependencies
   - `nixpacks.toml` - Build configuration
   - `bloodbankmanagement/settings_railway.py` - Railway settings

### Step 2: Deploy to Railway

1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will automatically detect the configuration and deploy

### Step 3: Configure Environment Variables

In your Railway project dashboard, add these environment variables:

```
DJANGO_SETTINGS_MODULE=bloodbankmanagement.settings_railway
SECRET_KEY=your-secret-key-here
```

To generate a secure SECRET_KEY, run:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 4: Verify Deployment

1. Check the deployment logs in Railway dashboard
2. Visit your Railway URL
3. Test the health check endpoint: `https://your-app.railway.app/health/`

## 🔧 Troubleshooting

### Health Check Issues

If you see "Healthcheck healthcheck failure":

1. **Check the health endpoint**: Visit `/health/` directly
2. **Check logs**: Look at Railway deployment logs
3. **Verify settings**: Ensure `DJANGO_SETTINGS_MODULE` is set correctly

### Database Issues

If you see database-related errors:

1. **Run migrations**: The deployment should run migrations automatically
2. **Check database**: Ensure SQLite file is being created
3. **Reset database**: If needed, you can reset the database in Railway

### Static Files Issues

If static files aren't loading:

1. **Check static collection**: Ensure `collectstatic` ran successfully
2. **Verify STATIC_ROOT**: Check that static files are in the correct location
3. **Check whitenoise**: Ensure whitenoise is in requirements.txt

## 📁 File Structure for Railway

```
bloodbankmanagement-master/
├── railway.json                    # Railway configuration
├── nixpacks.toml                  # Build configuration
├── requirements.txt                # Python dependencies
├── manage.py                      # Django management
├── bloodbankmanagement/
│   ├── settings.py                # Development settings
│   ├── settings_railway.py       # Railway production settings
│   ├── urls.py                   # URL configuration
│   └── wsgi.py                   # WSGI application
├── blood/                         # Blood app
├── donor/                         # Donor app
├── patient/                       # Patient app
└── templates/                     # HTML templates
```

## 🔍 Health Check Endpoint

The application includes a health check endpoint at `/health/` that returns:

```json
{
  "status": "healthy",
  "message": "Blood Bank Management System is running"
}
```

## 🌐 Accessing Your Application

Once deployed, you can access:

- **Main Application**: `https://your-app.railway.app/`
- **Admin Panel**: `https://your-app.railway.app/admin/`
- **Health Check**: `https://your-app.railway.app/health/`

## 📊 Monitoring

Railway provides:

- **Deployment logs**: View in Railway dashboard
- **Application logs**: Real-time logs from your app
- **Metrics**: CPU, memory, and network usage
- **Health status**: Automatic health checks

## 🔒 Security Notes

1. **SECRET_KEY**: Always use a secure, unique SECRET_KEY
2. **DEBUG**: Set to False in production
3. **ALLOWED_HOSTS**: Configured for Railway domains
4. **HTTPS**: Railway provides automatic HTTPS

## 🚨 Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'whitenoise'"

**Solution**: Ensure whitenoise is in requirements.txt

### Issue: "Database is locked"

**Solution**: This is normal for SQLite in production. Consider using PostgreSQL for better performance.

### Issue: "Static files not found"

**Solution**:

1. Check that `collectstatic` ran successfully
2. Verify STATIC_ROOT is set correctly
3. Ensure whitenoise middleware is enabled

### Issue: "Health check timeout"

**Solution**:

1. Check application startup time
2. Verify the health endpoint is accessible
3. Increase healthcheckTimeout in railway.json if needed

## 📞 Support

If you encounter issues:

1. Check Railway deployment logs
2. Verify all configuration files are present
3. Test locally with Railway settings
4. Check the health endpoint manually

## 🎉 Success!

Once deployed successfully, you should see:

- ✅ Build completed
- ✅ Health check passing
- ✅ Application accessible at your Railway URL
- ✅ Admin panel working
- ✅ All features functional
