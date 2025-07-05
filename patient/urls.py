from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from blood.auth_views import patient_login_view

urlpatterns = [
    path('patientlogin', LoginView.as_view(template_name='patient/patientlogin.html'),name='patientlogin'),
    path('patientsignup', views.patient_signup_view,name='patientsignup'),
    path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),
    path('edit-profile', views.patient_edit_profile_view,name='patient-edit-profile'),
    path('make-request', views.make_request_view,name='make-request'),
    path('my-request', views.my_request_view,name='my-request'),
]