from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta, datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User
from donor import models as dmodels
from patient import models as pmodels
from donor import forms as dforms
from patient import forms as pforms
from django.contrib import messages
from .auth_views import admin_required, donor_required, patient_required

def health_check(request):
    """Simple health check endpoint for Railway"""
    return JsonResponse({
        'status': 'healthy', 
        'message': 'Blood Bank Management System is running',
        'timestamp': str(datetime.now())
    })

def root_health_check(request):
    """Root endpoint for Railway health checks"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Blood Bank Management System - Root Endpoint',
        'timestamp': str(datetime.now())
    })

def home_view(request):
    x=models.Stock.objects.all()
    print(x)
    if len(x)==0:
        blood1=models.Stock()
        blood1.bloodgroup="A+"
        blood1.save()

        blood2=models.Stock()
        blood2.bloodgroup="A-"
        blood2.save()

        blood3=models.Stock()
        blood3.bloodgroup="B+"
        blood3.save()        

        blood4=models.Stock()
        blood4.bloodgroup="B-"
        blood4.save()

        blood5=models.Stock()
        blood5.bloodgroup="AB+"
        blood5.save()

        blood6=models.Stock()
        blood6.bloodgroup="AB-"
        blood6.save()

        blood7=models.Stock()
        blood7.bloodgroup="O+"
        blood7.save()

        blood8=models.Stock()
        blood8.bloodgroup="O-"
        blood8.save()

    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    
    # Get blood stock data for homepage with error handling
    try:
        blood_stock = {
            'A1': models.Stock.objects.get(bloodgroup="A+"),
            'A2': models.Stock.objects.get(bloodgroup="A-"),
            'B1': models.Stock.objects.get(bloodgroup="B+"),
            'B2': models.Stock.objects.get(bloodgroup="B-"),
            'AB1': models.Stock.objects.get(bloodgroup="AB+"),
            'AB2': models.Stock.objects.get(bloodgroup="AB-"),
            'O1': models.Stock.objects.get(bloodgroup="O+"),
            'O2': models.Stock.objects.get(bloodgroup="O-"),
        }
    except models.Stock.DoesNotExist:
        # If any stock doesn't exist, create default values
        blood_stock = {
            'A1': models.Stock(bloodgroup="A+", unit=0),
            'A2': models.Stock(bloodgroup="A-", unit=0),
            'B1': models.Stock(bloodgroup="B+", unit=0),
            'B2': models.Stock(bloodgroup="B-", unit=0),
            'AB1': models.Stock(bloodgroup="AB+", unit=0),
            'AB2': models.Stock(bloodgroup="AB-", unit=0),
            'O1': models.Stock(bloodgroup="O+", unit=0),
            'O2': models.Stock(bloodgroup="O-", unit=0),
        }
    
    # Calculate cumulative statistics from the beginning
    total_lives_saved = models.BloodRequest.objects.filter(status='Approved').count()
    total_donors = dmodels.Donor.objects.all().count()
    total_blood_units = models.Stock.objects.aggregate(Sum('unit'))['unit__sum'] or 0
    total_requests = models.BloodRequest.objects.all().count()
    
    # Add statistics to context
    blood_stock.update({
        'total_lives_saved': total_lives_saved,
        'total_donors': total_donors,
        'total_blood_units': total_blood_units,
        'total_requests': total_requests,
    })
    
    return render(request,'blood/index.html', context=blood_stock)

def is_donor(user):
    return user.groups.filter(name='DONOR').exists()

def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


@login_required(login_url='login-admin')
def afterlogin_view(request):
    if is_donor(request.user):
        return redirect('donor-dashboard')
    elif is_patient(request.user):
        return redirect('patient-dashboard')
    else:
        return redirect('admin-dashboard')

@login_required(login_url='login-admin')
def custom_logout_view(request):
    """Custom logout view that redirects to specific login pages"""
    user = request.user
    
    # Check user type before logout
    if is_donor(user):
        user_type = 'Donor'
        redirect_url = 'login-donor'
    elif is_patient(user):
        user_type = 'Patient'
        redirect_url = 'login-patient'
    else:
        user_type = 'Admin'
        redirect_url = 'login-admin'
    
    # Logout the user directly without confirmation
    from django.contrib.auth import logout
    logout(request)
    return redirect(redirect_url)  # Redirect to specific login page

def simple_logout_view(request):
    """Simple logout view for direct logout links"""
    user = request.user
    
    # Check user type before logout
    if is_donor(user):
        user_type = 'Donor'
        redirect_url = 'login-donor'
    elif is_patient(user):
        user_type = 'Patient'
        redirect_url = 'login-patient'
    else:
        user_type = 'Admin'
        redirect_url = 'login-admin'
    
    # Logout the user
    from django.contrib.auth import logout
    logout(request)
    return redirect(redirect_url)  # Redirect to specific login page

@admin_required
def admin_dashboard_view(request):
    totalunit=models.Stock.objects.aggregate(Sum('unit'))
    
    # Get counts for notifications
    pending_donations = dmodels.BloodDonate.objects.filter(status='Pending').count()
    pending_blood_requests = models.BloodRequest.objects.filter(status='Pending').count()
    forwarded_blood_requests = models.BloodRequest.objects.filter(status='Forwarded').count()
    donation_confirmed_requests = models.BloodRequest.objects.filter(status='Donation_Confirmed').count()
    
    # Total pending items for red color notification
    total_pending_items = pending_donations + pending_blood_requests + forwarded_blood_requests + donation_confirmed_requests
    
    dict={
        'A1':models.Stock.objects.get(bloodgroup="A+"),
        'A2':models.Stock.objects.get(bloodgroup="A-"),
        'B1':models.Stock.objects.get(bloodgroup="B+"),
        'B2':models.Stock.objects.get(bloodgroup="B-"),
        'AB1':models.Stock.objects.get(bloodgroup="AB+"),
        'AB2':models.Stock.objects.get(bloodgroup="AB-"),
        'O1':models.Stock.objects.get(bloodgroup="O+"),
        'O2':models.Stock.objects.get(bloodgroup="O-"),
        'totaldonors':dmodels.Donor.objects.all().count(),
        'totalbloodunit':totalunit['unit__sum'],
        'totalrequest':models.BloodRequest.objects.all().count(),
        'totalapprovedrequest':models.BloodRequest.objects.all().filter(status='Approved').count(),
        'pendingrequests':models.BloodRequest.objects.filter(status='Pending').count(),
        'forwardedrequests':models.BloodRequest.objects.filter(status='Forwarded').count(),
        'acceptedrequests':models.BloodRequest.objects.filter(status='Accepted').count(),
        # New notification counts
        'pending_donations': pending_donations,
        'pending_blood_requests': pending_blood_requests,
        'forwarded_blood_requests': forwarded_blood_requests,
        'donation_confirmed_requests': donation_confirmed_requests,
        'total_pending_items': total_pending_items,
        'has_pending_items': total_pending_items > 0,
    }
    return render(request,'blood/admin_dashboard.html',context=dict)

@admin_required
def admin_blood_view(request):
    dict={
        'bloodForm':forms.BloodForm(),
        'A1':models.Stock.objects.get(bloodgroup="A+"),
        'A2':models.Stock.objects.get(bloodgroup="A-"),
        'B1':models.Stock.objects.get(bloodgroup="B+"),
        'B2':models.Stock.objects.get(bloodgroup="B-"),
        'AB1':models.Stock.objects.get(bloodgroup="AB+"),
        'AB2':models.Stock.objects.get(bloodgroup="AB-"),
        'O1':models.Stock.objects.get(bloodgroup="O+"),
        'O2':models.Stock.objects.get(bloodgroup="O-"),
    }
    if request.method=='POST':
        bloodForm=forms.BloodForm(request.POST)
        if bloodForm.is_valid() :        
            bloodgroup=bloodForm.cleaned_data['bloodgroup']
            stock=models.Stock.objects.get(bloodgroup=bloodgroup)
            stock.unit=bloodForm.cleaned_data['unit']
            stock.save()
        return HttpResponseRedirect('admin-blood')
    return render(request,'blood/admin_blood.html',context=dict)


@login_required(login_url='adminlogin')
def admin_donor_view(request):
    donors=dmodels.Donor.objects.all()
    return render(request,'blood/admin_donor.html',{'donors':donors})

@login_required(login_url='adminlogin')
def admin_donor_profile_view(request, pk):
    """Admin view to see donor profile details without editing access"""
    try:
        donor = dmodels.Donor.objects.get(id=pk)
        # Get donation history
        donations = dmodels.BloodDonate.objects.filter(donor=donor).order_by('-date')
        # Get request history if any
        requests = models.BloodRequest.objects.filter(request_by_donor=donor).order_by('-date')
        
        context = {
            'donor': donor,
            'donations': donations,
            'requests': requests,
        }
        return render(request, 'blood/admin_donor_profile.html', context)
    except dmodels.Donor.DoesNotExist:
        messages.error(request, 'Donor not found.')
        return redirect('admin-donor')

@login_required(login_url='adminlogin')
def update_donor_view(request,pk):
    donor=dmodels.Donor.objects.get(id=pk)
    user=dmodels.User.objects.get(id=donor.user_id)
    userForm=dforms.DonorUserForm(instance=user)
    donorForm=dforms.DonorForm(request.FILES,instance=donor)
    mydict={'userForm':userForm,'donorForm':donorForm}
    if request.method=='POST':
        userForm=dforms.DonorUserForm(request.POST,instance=user)
        donorForm=dforms.DonorForm(request.POST,request.FILES,instance=donor)
        if userForm.is_valid() and donorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            donor=donorForm.save(commit=False)
            donor.user=user
            donor.bloodgroup=donorForm.cleaned_data['bloodgroup']
            donor.save()
            return redirect('admin-donor')
    return render(request,'blood/update_donor.html',context=mydict)


@login_required(login_url='adminlogin')
def delete_donor_view(request,pk):
    donor=dmodels.Donor.objects.get(id=pk)
    user=User.objects.get(id=donor.user_id)
    user.delete()
    donor.delete()
    return HttpResponseRedirect('/admin-donor')

@login_required(login_url='adminlogin')
def admin_patient_view(request):
    patients=pmodels.Patient.objects.all()
    return render(request,'blood/admin_patient.html',{'patients':patients})


@login_required(login_url='adminlogin')
def admin_patient_profile_view(request, pk):
    """Admin view to see patient profile details without editing access"""
    try:
        patient = pmodels.Patient.objects.get(id=pk)
        # Get request history
        requests = models.BloodRequest.objects.filter(request_by_patient=patient).order_by('-date')
        
        context = {
            'patient': patient,
            'requests': requests,
        }
        return render(request, 'blood/admin_patient_profile.html', context)
    except pmodels.Patient.DoesNotExist:
        messages.error(request, 'Patient not found.')
        return redirect('admin-patient')


@login_required(login_url='adminlogin')
def update_patient_view(request,pk):
    patient=pmodels.Patient.objects.get(id=pk)
    user=pmodels.User.objects.get(id=patient.user_id)
    userForm=pforms.PatientUserForm(instance=user)
    patientForm=pforms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=pforms.PatientUserForm(request.POST,instance=user)
        patientForm=pforms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.bloodgroup=patientForm.cleaned_data['bloodgroup']
            patient.save()
            return redirect('admin-patient')
    return render(request,'blood/update_patient.html',context=mydict)


@login_required(login_url='adminlogin')
def delete_patient_view(request,pk):
    patient=pmodels.Patient.objects.get(id=pk)
    user=User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return HttpResponseRedirect('/admin-patient')

@login_required(login_url='adminlogin')
def admin_request_view(request):
    requests = models.BloodRequest.objects.all().order_by('-date')
    return render(request,'blood/admin_request.html',{'requests':requests})

@login_required(login_url='adminlogin')
def admin_handle_request_view(request, pk):
    """Admin view to handle blood requests with 3 options: Approve, Reject, Donor Request"""
    blood_request = models.BloodRequest.objects.get(id=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        admin_notes = request.POST.get('admin_notes', '')
        
        if action == 'approve':
            # Check if stock is available
            try:
                stock = models.Stock.objects.get(bloodgroup=blood_request.bloodgroup)
                if stock.unit >= blood_request.unit:
                    # Update stock
                    stock.unit = stock.unit - blood_request.unit
                    stock.save()
                    
                    # Approve request
                    blood_request.status = 'Approved'
                    blood_request.admin_notes = admin_notes
                    blood_request.save()
                    
                    messages.success(request, 'Request approved successfully!')
                else:
                    messages.error(request, f'Insufficient stock. Only {stock.unit} units available for {blood_request.bloodgroup}.')
            except models.Stock.DoesNotExist:
                messages.error(request, f'No stock available for blood group {blood_request.bloodgroup}.')
        
        elif action == 'reject':
            blood_request.status = 'Rejected'
            blood_request.admin_notes = admin_notes
            blood_request.save()
            messages.info(request, 'Request rejected.')
        
        elif action == 'donor_request':
            # Forward to donors with matching blood group
            donors = dmodels.Donor.objects.filter(bloodgroup=blood_request.bloodgroup)
            if donors.exists():
                # Create donor requests for each matching donor
                for donor in donors:
                    models.DonorRequest.objects.get_or_create(
                        blood_request=blood_request,
                        donor=donor,
                        defaults={'status': 'Pending', 'donation_confirmed': False}
                    )
                
                blood_request.status = 'Forwarded'
                blood_request.admin_notes = admin_notes
                blood_request.save()
                
                messages.success(request, f'Request forwarded to {donors.count()} donors with blood group {blood_request.bloodgroup}.')
            else:
                messages.error(request, f'No donors found with blood group {blood_request.bloodgroup}.')
        
        elif action == 'approve_donation':
            # Approve donation confirmed request
            if blood_request.status == 'Donation_Confirmed':
                try:
                    stock = models.Stock.objects.get(bloodgroup=blood_request.bloodgroup)
                    stock.unit = stock.unit + blood_request.unit
                    stock.save()
                    
                    blood_request.status = 'Approved'
                    blood_request.admin_notes = admin_notes
                    blood_request.save()
                    
                    # Close all donor requests
                    models.DonorRequest.objects.filter(blood_request=blood_request).update(status='Closed')
                    
                    messages.success(request, 'Donation approved and blood added to stock!')
                except models.Stock.DoesNotExist:
                    messages.error(request, f'No stock record found for blood group {blood_request.bloodgroup}.')
            else:
                messages.error(request, 'Only donation confirmed requests can be approved.')
        
        return redirect('admin-request')
    
    # Get stock information
    try:
        stock = models.Stock.objects.get(bloodgroup=blood_request.bloodgroup)
        stock_available = stock.unit
        stock_sufficient = stock.unit >= blood_request.unit
    except models.Stock.DoesNotExist:
        stock_available = 0
        stock_sufficient = False
    
    # Get donor count for matching blood group
    donor_count = dmodels.Donor.objects.filter(bloodgroup=blood_request.bloodgroup).count()
    
    context = {
        'blood_request': blood_request,
        'stock_available': stock_available,
        'stock_sufficient': stock_sufficient,
        'donor_count': donor_count,
    }
    return render(request, 'blood/admin_handle_request.html', context)

@login_required(login_url='adminlogin')
def admin_request_history_view(request):
    requests=models.BloodRequest.objects.all().exclude(status='Pending')
    return render(request,'blood/admin_request_history.html',{'requests':requests})

@login_required(login_url='adminlogin')
def admin_donation_view(request):
    donations=dmodels.BloodDonate.objects.all()
    return render(request,'blood/admin_donation.html',{'donations':donations})

@login_required(login_url='adminlogin')
def update_approve_status_view(request,pk):
    req=models.BloodRequest.objects.get(id=pk)
    message=None
    bloodgroup=req.bloodgroup
    unit=req.unit
    stock=models.Stock.objects.get(bloodgroup=bloodgroup)
    if stock.unit > unit:
        stock.unit=stock.unit-unit
        stock.save()
        req.status="Approved"
        
    else:
        message="Stock Doest Not Have Enough Blood To Approve This Request, Only "+str(stock.unit)+" Unit Available"
    req.save()

    requests=models.BloodRequest.objects.all().filter(status='Pending')
    return render(request,'blood/admin_request.html',{'requests':requests,'message':message})

@login_required(login_url='adminlogin')
def update_reject_status_view(request,pk):
    req=models.BloodRequest.objects.get(id=pk)
    req.status="Rejected"
    req.save()
    return HttpResponseRedirect('/admin-request')

@login_required(login_url='adminlogin')
def approve_donation_view(request,pk):
    donation=dmodels.BloodDonate.objects.get(id=pk)
    donation_blood_group=donation.bloodgroup
    donation_blood_unit=donation.unit

    stock=models.Stock.objects.get(bloodgroup=donation_blood_group)
    stock.unit=stock.unit+donation_blood_unit
    stock.save()

    donation.status='Approved'
    donation.save()
    return HttpResponseRedirect('/admin-donation')


@login_required(login_url='adminlogin')
def reject_donation_view(request,pk):
    donation=dmodels.BloodDonate.objects.get(id=pk)
    donation.status='Rejected'
    donation.save()
    return HttpResponseRedirect('/admin-donation')

