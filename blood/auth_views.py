from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from functools import wraps


def role_required(allowed_roles):
    """
    Custom decorator to check if user has the required role(s)
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login-admin')  # Default to admin login
            
            user_groups = request.user.groups.all()
            user_roles = [group.name for group in user_groups]
            
            # Check if user has any of the allowed roles
            if not any(role in user_roles for role in allowed_roles):
                messages.error(request, "You don't have access to this section.")
                return HttpResponseForbidden(b"Access denied")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def admin_required(view_func):
    """Decorator to ensure user is admin"""
    return role_required(['ADMIN'])(view_func)


def donor_required(view_func):
    """Decorator to ensure user is donor"""
    return role_required(['DONOR'])(view_func)


def patient_required(view_func):
    """Decorator to ensure user is patient"""
    return role_required(['PATIENT'])(view_func)


def login_view(request, role):
    """
    Generic login view that handles authentication for all roles
    """
    if request.user.is_authenticated:
        # If user is already logged in, redirect to appropriate dashboard
        if role == 'admin' and request.user.groups.filter(name='ADMIN').exists():
            return redirect('admin-dashboard')
        elif role == 'donor' and request.user.groups.filter(name='DONOR').exists():
            return redirect('donor-dashboard')
        elif role == 'patient' and request.user.groups.filter(name='PATIENT').exists():
            return redirect('patient-dashboard')
        else:
            # User is logged in but doesn't have the right role for this login page
            messages.error(request, "You don't have access to this section.")
            return redirect('')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if user exists
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "No account found. Please register first.")
            return render(request, f'{role}/{role}login.html')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user has the correct role
            if role == 'admin' and user.groups.filter(name='ADMIN').exists():
                login(request, user)
                return redirect('admin-dashboard')
            elif role == 'donor' and user.groups.filter(name='DONOR').exists():
                login(request, user)
                return redirect('donor-dashboard')
            elif role == 'patient' and user.groups.filter(name='PATIENT').exists():
                login(request, user)
                return redirect('patient-dashboard')
            else:
                # User exists and credentials are valid, but wrong role
                messages.error(request, "You don't have access to this section.")
                return render(request, f'{role}/{role}login.html')
        else:
            # Invalid credentials
            messages.error(request, "Invalid username or password.")
            return render(request, f'{role}/{role}login.html')
    
    return render(request, f'{role}/{role}login.html')


def admin_login_view(request):
    """Admin login view"""
    return login_view(request, 'admin')


def donor_login_view(request):
    """Donor login view"""
    return login_view(request, 'donor')


def patient_login_view(request):
    """Patient login view"""
    return login_view(request, 'patient') 