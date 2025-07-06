# 🔧 Railway Environment Variable Fix

## 🚨 Error: "invalid key-value pair "= SECRET_KEY\n=4321": empty key"

This error occurs when Railway can't properly parse environment variables. Here's how to fix it:

## 🔧 Solution Steps:

### Step 1: Check Railway Dashboard

1. Go to your Railway project dashboard
2. Click on your project
3. Go to "Variables" tab
4. **Delete all existing environment variables**
5. **Add them one by one correctly**

### Step 2: Add Environment Variables Correctly

In Railway dashboard, add these variables **one at a time**:

```
Key: DEBUG
Value: False
```

```
Key: SECRET_KEY
Value: your-secret-key-here
```

```
Key: ALLOWED_HOSTS
Value: your-app-name.railway.app
```

### Step 3: Generate a Proper SECRET_KEY

Run this command locally to generate a secure key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Copy the output and use it as your SECRET_KEY value.

### Step 4: Alternative - Use Railway CLI

If the dashboard method doesn't work:

1. Install Railway CLI:

```bash
npm install -g @railway/cli
```

2. Login to Railway:

```bash
railway login
```

3. Link your project:

```bash
railway link
```

4. Set variables via CLI:

```bash
railway variables set DEBUG=False
railway variables set SECRET_KEY=your-generated-secret-key
railway variables set ALLOWED_HOSTS=your-app-name.railway.app
```

## 🚨 Common Mistakes to Avoid:

### ❌ Don't do this:

- Don't copy-paste from other sources
- Don't include quotes around values
- Don't add extra spaces
- Don't use special characters in keys

### ✅ Do this:

- Type each variable manually
- Use simple alphanumeric keys
- Use simple string values
- Test one variable at a time

## 🔍 Debugging Steps:

### 1. Check Variable Format

Ensure your variables look like this:

```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-app-name.railway.app
```

### 2. Test Locally First

```bash
# Test with environment variables
export DEBUG=False
export SECRET_KEY=test-key
export ALLOWED_HOSTS=localhost
python manage.py check --deploy
```

### 3. Check Railway Logs

- Go to Railway dashboard
- Click on your project
- Go to "Deployments" tab
- Check the latest deployment logs

## 🎯 Quick Fix Commands:

If you need to reset everything:

```bash
# Generate new secret key
python -c "import secrets; print(secrets.token_urlsafe(50))"

# Test locally
export DEBUG=False
export SECRET_KEY=your-new-key
python manage.py check --deploy
```

## 📞 If Problem Persists:

1. **Delete and recreate the project** in Railway
2. **Use Railway CLI** instead of dashboard
3. **Check for hidden characters** in your environment variables
4. **Contact Railway support** if the issue continues

## ✅ Success Checklist:

- [ ] All environment variables are set correctly
- [ ] No empty keys or values
- [ ] No special characters in variable names
- [ ] SECRET_KEY is properly generated
- [ ] DEBUG is set to False
- [ ] ALLOWED_HOSTS includes your Railway domain

**Remember**: Railway is sensitive to environment variable formatting. Always add them manually and one at a time!
