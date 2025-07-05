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

def donor_signup_view(request):
    userForm=forms.DonorUserForm()
    donorForm=forms.DonorForm()
    mydict={'userForm':userForm,'donorForm':donorForm}
    if request.method=='POST':
        userForm=forms.DonorUserForm(request.POST)
        donorForm=forms.DonorForm(request.POST,request.FILES)
        
        # Debug: Print form errors
        if not userForm.is_valid():
            print("UserForm errors:", userForm.errors)
            for field, errors in userForm.errors.items():
                for error in errors:
                    messages.error(request, f'User form error - {field}: {error}')
        if not donorForm.is_valid():
            print("DonorForm errors:", donorForm.errors)
            for field, errors in donorForm.errors.items():
                for error in errors:
                    messages.error(request, f'Donor form error - {field}: {error}')
        
        if userForm.is_valid() and donorForm.is_valid():
            try:
                # Save user with proper password hashing
                user=userForm.save()
                
                # Save donor profile
                donor=donorForm.save(commit=False)
                donor.user=user
                donor.bloodgroup=donorForm.cleaned_data['bloodgroup']
                donor.save()
                
                # Add user to DONOR group
                my_donor_group = Group.objects.get_or_create(name='DONOR')
                my_donor_group[0].user_set.add(user)
                
                messages.success(request, 'Donor registration successful! Please login.')
                return HttpResponseRedirect('donorlogin')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
                # If user was created but donor failed, delete the user
                if user and user.id:
                    user.delete()
        else:
            messages.error(request, 'Please correct the errors below.')
    return render(request,'donor/donorsignup.html',context=mydict)


def donor_dashboard_view(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('donorlogin')
    
    try:
        donor = models.Donor.objects.get(user=request.user)
        
        # Get donor requests (requests forwarded to this donor by admin)
        donor_requests = bmodels.DonorRequest.objects.filter(donor=donor)
        
        # Get blood requests made by this donor (if any)
        blood_requests_made = bmodels.BloodRequest.objects.filter(request_by_donor=donor)
        
        dict={
            'donor': donor,
            'requestpending': donor_requests.filter(status='Pending').count(),
            'requestapproved': donor_requests.filter(status='Donation_Confirmed').count(),
            'requestmade': blood_requests_made.count(),
            'requestrejected': donor_requests.filter(status='Rejected').count(),
        }
        return render(request,'donor/donor_dashboard.html',context=dict)
    except models.Donor.DoesNotExist:
        messages.error(request, 'Donor profile not found. Please contact administrator.')
        return redirect('donorlogin')


def donate_blood_view(request):
    if request.method=='POST':
        donation_form=forms.DonationForm(request.POST)
        if donation_form.is_valid():
            blood_donate=donation_form.save(commit=False)
            blood_donate.bloodgroup=donation_form.cleaned_data['blood_group']
            donor= models.Donor.objects.get(user=request.user)
            blood_donate.donor=donor
            blood_donate.save()
            
            # Auto-confirm pending donor requests for this donor
            pending_donor_requests = bmodels.DonorRequest.objects.filter(
                donor=donor,
                status='Donation_Pending'
            )
            
            for donor_request in pending_donor_requests:
                # Confirm the donation
                donor_request.status = 'Donation_Confirmed'
                donor_request.donation_confirmed = True
                donor_request.save()
                
                # Update the blood request status
                blood_request = donor_request.blood_request
                blood_request.status = 'Donation_Confirmed'
                blood_request.save()
                
                messages.success(request, f'Donation automatically confirmed for request: {blood_request.patient_name}')
            
            return HttpResponseRedirect('donation-history')
        else:
            # Form has errors, show them to user
            messages.error(request, 'Please correct the errors below.')
    else:
        donation_form=forms.DonationForm()
    
    return render(request,'donor/donate_blood.html',{'donation_form':donation_form})

def donation_history_view(request):
    donor= models.Donor.objects.get(user=request.user)
    blood_donate=models.BloodDonate.objects.all().filter(donor=donor)
    return render(request,'donor/donation_history.html',{'blood_donate':blood_donate})

@login_required(login_url='donorlogin')
def donor_requests_view(request):
    donor = models.Donor.objects.get(user=request.user)
    
    # Get donor requests (requests forwarded to this donor by admin)
    donor_requests = bmodels.DonorRequest.objects.filter(donor=donor).order_by('-response_date')
    
    # Get blood requests made by this donor (if any)
    blood_requests_made = bmodels.BloodRequest.objects.filter(request_by_donor=donor)
    
    # Get statistics for dashboard
    pending_requests = donor_requests.filter(status='Pending')
    accepted_requests = donor_requests.filter(status='Accepted')
    rejected_requests = donor_requests.filter(status='Rejected')
    closed_requests = donor_requests.filter(status='Closed')
    
    context = {
        'donor_requests': donor_requests,
        'blood_requests_made': blood_requests_made,
        'pending_requests': pending_requests,
        'accepted_requests': accepted_requests,
        'rejected_requests': rejected_requests,
        'closed_requests': closed_requests,
    }
    
    return render(request, 'donor/donor_requests.html', context)

@login_required(login_url='donorlogin')
def donor_edit_profile_view(request):
    """View for donors to edit their profile information"""
    try:
        donor = models.Donor.objects.get(user=request.user)
    except models.Donor.DoesNotExist:
        messages.error(request, 'Donor profile not found. Please contact administrator.')
        return redirect('donorlogin')
    
    if request.method == 'POST':
        # Handle profile update
        user_form = forms.DonorEditForm(request.POST, instance=request.user)
        donor_form = forms.DonorForm(request.POST, request.FILES, instance=donor)
        
        if user_form.is_valid() and donor_form.is_valid():
            try:
                # Update user information
                user = user_form.save(commit=False)
                if user_form.cleaned_data.get('password1'):
                    user.set_password(user_form.cleaned_data['password1'])
                user.save()
                
                # Update donor information
                donor = donor_form.save(commit=False)
                donor.user = user
                donor.save()
                
                messages.success(request, 'Profile updated successfully!')
                return redirect('donor-dashboard')
            except Exception as e:
                messages.error(request, f'Error updating profile: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-populate forms with current data
        user_form = forms.DonorEditForm(instance=request.user)
        donor_form = forms.DonorForm(instance=donor)
    
    context = {
        'user_form': user_form,
        'donor_form': donor_form,
        'donor': donor,
    }
    return render(request, 'donor/edit_profile.html', context)

@login_required(login_url='donorlogin')
def donor_respond_request_view(request, request_id):
    """View for donor to respond to blood requests"""
    if request.method == 'POST':
        donor = models.Donor.objects.get(user=request.user)
        action = request.POST.get('action')
        
        try:
            blood_request = bmodels.BloodRequest.objects.get(id=request_id)
            donor_request = bmodels.DonorRequest.objects.filter(
                blood_request=blood_request,
                donor=donor,
                status='Pending'
            ).first()
            
            if donor_request:
                if action == 'accept':
                    # Accept the request - status becomes Donation_Pending
                    donor_request.status = 'Donation_Pending'
                    donor_request.save()
                    
                    # Update blood request status
                    blood_request.status = 'Donation_Pending'
                    blood_request.accepted_by_donor = donor
                    blood_request.save()
                    
                    # Reject all other donor requests for this blood request
                    bmodels.DonorRequest.objects.filter(
                        blood_request=blood_request,
                        status='Pending'
                    ).exclude(donor=donor).update(status='Rejected')
                    
                    messages.success(request, 'Request accepted! Please donate blood to complete the process.')
                elif action == 'reject':
                    donor_request.status = 'Rejected'
                    donor_request.save()
                    messages.info(request, 'Request rejected.')
                
                return redirect('donor-requests')
            else:
                messages.error(request, 'Request not found or already processed.')
                return redirect('donor-requests')
                
        except bmodels.BloodRequest.DoesNotExist:
            messages.error(request, 'Blood request not found.')
            return redirect('donor-requests')
    
    return redirect('donor-requests')

@login_required(login_url='donorlogin')
def donor_confirm_donation_view(request, request_id):
    """View for donor to confirm they have donated blood"""
    if request.method == 'POST':
        donor = models.Donor.objects.get(user=request.user)
        
        try:
            blood_request = bmodels.BloodRequest.objects.get(id=request_id)
            donor_request = bmodels.DonorRequest.objects.filter(
                blood_request=blood_request,
                donor=donor,
                status='Donation_Pending'
            ).first()
            
            if donor_request and blood_request.accepted_by_donor == donor:
                # Confirm donation
                donor_request.status = 'Donation_Confirmed'
                donor_request.donation_confirmed = True
                donor_request.save()
                
                blood_request.status = 'Donation_Confirmed'
                blood_request.save()
                
                messages.success(request, 'Donation confirmed! Admin will review and approve your donation.')
                return redirect('donor-requests')
            else:
                messages.error(request, 'Request not found or you are not the accepted donor.')
                return redirect('donor-requests')
                
        except bmodels.BloodRequest.DoesNotExist:
            messages.error(request, 'Blood request not found.')
            return redirect('donor-requests')
    
    return redirect('donor-requests')
