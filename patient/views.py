from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from blood import forms as bforms
from blood import models as bmodels
from django.contrib import messages


def patient_signup_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        
        # Debug: Print form errors
        if not userForm.is_valid():
            print("UserForm errors:", userForm.errors)
            for field, errors in userForm.errors.items():
                for error in errors:
                    messages.error(request, f'User form error - {field}: {error}')
        if not patientForm.is_valid():
            print("PatientForm errors:", patientForm.errors)
            for field, errors in patientForm.errors.items():
                for error in errors:
                    messages.error(request, f'Patient form error - {field}: {error}')
        
        if userForm.is_valid() and patientForm.is_valid():
            try:
                # Save user with proper password hashing
                user=userForm.save()
                
                # Save patient profile
                patient=patientForm.save(commit=False)
                patient.user=user
                patient.bloodgroup=patientForm.cleaned_data['bloodgroup']
                patient.save()
                
                # Add user to PATIENT group
                my_patient_group = Group.objects.get_or_create(name='PATIENT')
                my_patient_group[0].user_set.add(user)
                
                messages.success(request, 'Patient registration successful! Please login.')
                return HttpResponseRedirect('patientlogin')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
                # If user was created but patient failed, delete the user
                if user and user.id:
                    user.delete()
        else:
            messages.error(request, 'Please correct the errors below.')
    return render(request,'patient/patientsignup.html',context=mydict)

def patient_dashboard_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to access your dashboard.')
        return redirect('patientlogin')
    
    try:
        patient = models.Patient.objects.get(user=request.user)
    except models.Patient.DoesNotExist:
        messages.error(request, 'Patient profile not found. Please contact administrator.')
        return redirect('patientlogin')
    
    dict={
        'patient': patient,
        'requestpending': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Pending').count(),
        'requestapproved': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Approved').count(),
        'requestmade': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).count(),
        'requestrejected': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Rejected').count(),

    }
   
    return render(request,'patient/patient_dashboard.html',context=dict)

def make_request_view(request):
    request_form=bforms.RequestForm()
    if request.method=='POST':
        request_form=bforms.RequestForm(request.POST)
        if request_form.is_valid():
            blood_request=request_form.save(commit=False)
            blood_request.bloodgroup=request_form.cleaned_data['bloodgroup']
            patient= models.Patient.objects.get(user=request.user)
            blood_request.request_by_patient=patient
            blood_request.save()
            return HttpResponseRedirect('my-request')  
    return render(request,'patient/makerequest.html',{'request_form':request_form})

def my_request_view(request):
    patient= models.Patient.objects.get(user=request.user)
    blood_request=bmodels.BloodRequest.objects.all().filter(request_by_patient=patient)
    return render(request,'patient/my_request.html',{'blood_request':blood_request})

@login_required(login_url='patientlogin')
def patient_edit_profile_view(request):
    """View for patients to edit their profile information"""
    try:
        patient = models.Patient.objects.get(user=request.user)
    except models.Patient.DoesNotExist:
        messages.error(request, 'Patient profile not found.')
        return redirect('patient-dashboard')
    
    if request.method == 'POST':
        # Handle profile update
        user_form = forms.PatientEditForm(request.POST, instance=request.user)
        patient_form = forms.PatientForm(request.POST, request.FILES, instance=patient)
        
        # Debug: Print form errors
        if not user_form.is_valid():
            print("UserForm errors:", user_form.errors)
            if user_form.errors:
                for field, errors in user_form.errors.items():
                    for error in errors:
                        messages.error(request, f'User form error - {field}: {error}')
        if not patient_form.is_valid():
            print("PatientForm errors:", patient_form.errors)
            if patient_form.errors:
                for field, errors in patient_form.errors.items():
                    for error in errors:
                        messages.error(request, f'Patient form error - {field}: {error}')
        
        if user_form.is_valid() and patient_form.is_valid():
            try:
                # Update user information
                user = user_form.save(commit=False)
                if user_form.cleaned_data.get('password1'):
                    user.set_password(user_form.cleaned_data['password1'])
                user.save()
                
                # Update patient information
                patient = patient_form.save(commit=False)
                patient.user = user
                patient.save()
                
                messages.success(request, '✅ Profile updated successfully! Your changes have been saved.')
                return redirect('patient-dashboard')
            except Exception as e:
                messages.error(request, f'❌ Error updating profile: {str(e)}')
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        # Pre-populate forms with current data
        user_form = forms.PatientEditForm(instance=request.user)
        patient_form = forms.PatientForm(instance=patient)
    
    context = {
        'user_form': user_form,
        'patient_form': patient_form,
        'patient': patient,
        'debug': True,  # Add debug flag
    }
    
    # Debug: Print context to see what's being passed
    print("Context keys:", context.keys())
    print("Patient object:", patient)
    print("User form fields:", user_form.fields.keys())
    print("Patient form fields:", patient_form.fields.keys())
    
    return render(request, 'patient/edit_profile_simple.html', context)
