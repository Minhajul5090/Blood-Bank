"""bloodbankmanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static
from blood import views
from blood.auth_views import admin_login_view, donor_login_view, patient_login_view
urlpatterns = [
    path('admin/', admin.site.urls),

    
    path('donor/',include('donor.urls')),
    path('patient/',include('patient.urls')),

    
    path('',views.home_view,name=''),
    path('logout', views.custom_logout_view,name='logout'),
    path('logout-now', views.simple_logout_view,name='logout-now'),

    # New role-based login URLs
    path('login/admin/', admin_login_view, name='login-admin'),
    path('login/donor/', donor_login_view, name='login-donor'),
    path('login/patient/', patient_login_view, name='login-patient'),
    
    # After login redirect URL
    path('afterlogin', views.afterlogin_view, name='afterlogin'),
    
    # Legacy login URLs (for backward compatibility)
    path('adminlogin', LoginView.as_view(template_name='blood/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('admin-blood', views.admin_blood_view,name='admin-blood'),
    path('admin-donor', views.admin_donor_view,name='admin-donor'),
    path('admin-donor-profile/<int:pk>', views.admin_donor_profile_view,name='admin-donor-profile'),
    path('admin-patient', views.admin_patient_view,name='admin-patient'),
    path('admin-patient-profile/<int:pk>', views.admin_patient_profile_view,name='admin-patient-profile'),
    path('update-donor/<int:pk>', views.update_donor_view,name='update-donor'),
    path('delete-donor/<int:pk>', views.delete_donor_view,name='delete-donor'),
    path('admin-request', views.admin_request_view,name='admin-request'),
    path('admin-handle-request/<int:pk>/', views.admin_handle_request_view,name='admin-handle-request'),
    path('update-patient/<int:pk>', views.update_patient_view,name='update-patient'),
    path('delete-patient/<int:pk>', views.delete_patient_view,name='delete-patient'),
    path('admin-donation', views.admin_donation_view,name='admin-donation'),
    path('approve-donation/<int:pk>', views.approve_donation_view,name='approve-donation'),
    path('reject-donation/<int:pk>', views.reject_donation_view,name='reject-donation'),
    path('admin-request-history', views.admin_request_history_view,name='admin-request-history'),
    path('update-approve-status/<int:pk>', views.update_approve_status_view,name='update-approve-status'),
    path('update-reject-status/<int:pk>', views.update_reject_status_view,name='update-reject-status'),
    

   
]

# Add media URL pattern for serving uploaded files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

