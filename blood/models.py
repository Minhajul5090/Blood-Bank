from django.db import models
from patient import models as pmodels
from donor import models as dmodels
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Stock(models.Model):
    bloodgroup=models.CharField(max_length=10)
    unit=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.bloodgroup

class BloodRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Forwarded', 'Forwarded to Donors'),
        ('Accepted', 'Accepted by Donor'),
        ('Donation_Pending', 'Donation Pending'),
        ('Donation_Confirmed', 'Donation Confirmed'),
        ('Approved', 'Approved by Admin'),
        ('Closed', 'Closed'),
        ('Rejected', 'Rejected'),
    ]
    
    request_by_patient=models.ForeignKey(pmodels.Patient,null=True,on_delete=models.CASCADE)
    request_by_donor=models.ForeignKey(dmodels.Donor,null=True,on_delete=models.CASCADE)
    patient_name=models.CharField(max_length=30)
    patient_age=models.PositiveIntegerField()
    reason=models.CharField(max_length=500)
    bloodgroup=models.CharField(max_length=10)
    unit=models.PositiveIntegerField(default=0)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="Pending")
    date=models.DateField(auto_now=True)
    accepted_by_donor=models.ForeignKey(dmodels.Donor,null=True,blank=True,on_delete=models.SET_NULL,related_name='accepted_requests')
    admin_notes=models.TextField(blank=True,null=True)
    
    def __str__(self):
        return f"{self.patient_name} - {self.bloodgroup} - {self.status}"
    
    def get_available_stock(self):
        try:
            stock = Stock.objects.get(bloodgroup=self.bloodgroup)
            return stock.unit
        except Stock.DoesNotExist:
            return 0
    
    def is_stock_available(self):
        return self.get_available_stock() >= self.unit
    
    def forward_to_donors(self):
        """Forward request to all donors with matching blood group"""
        if self.status == 'Pending' and not self.is_stock_available():
            donors = dmodels.Donor.objects.filter(bloodgroup=self.bloodgroup)
            for donor in donors:
                DonorRequest.objects.get_or_create(
                    blood_request=self,
                    donor=donor,
                    defaults={'status': 'Pending', 'donation_confirmed': False}
                )
            self.status = 'Forwarded'
            self.save()
            return True
        return False
    
    def accept_by_donor(self, donor):
        """Accept request by a donor"""
        if self.status == 'Forwarded':
            donor_request = DonorRequest.objects.filter(
                blood_request=self,
                donor=donor,
                status='Pending'
            ).first()
            
            if donor_request:
                # Reject all other donor requests
                DonorRequest.objects.filter(
                    blood_request=self,
                    status='Pending'
                ).exclude(donor=donor).update(status='Rejected')
                
                donor_request.status = 'Donation_Pending'
                donor_request.save()
                
                self.status = 'Donation_Pending'
                self.accepted_by_donor = donor
                self.save()
                return True
        return False
    
    def confirm_donation(self, donor):
        """Confirm that donor has donated blood"""
        if self.status == 'Donation_Pending' and self.accepted_by_donor == donor:
            donor_request = DonorRequest.objects.filter(
                blood_request=self,
                donor=donor,
                status='Donation_Pending'
            ).first()
            
            if donor_request:
                donor_request.status = 'Donation_Confirmed'
                donor_request.donation_confirmed = True
                donor_request.save()
                
                self.status = 'Donation_Confirmed'
                self.save()
                return True
        return False
    
    def approve_by_admin(self):
        """Approve the donation confirmed request by admin"""
        if self.status == 'Donation_Confirmed':
            self.status = 'Approved'
            self.save()
            
            # Update stock
            stock, created = Stock.objects.get_or_create(bloodgroup=self.bloodgroup)
            stock.unit += self.unit
            stock.save()
            
            # Close all donor requests
            DonorRequest.objects.filter(blood_request=self).update(status='Closed')
            return True
        return False

class DonorRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Donation_Pending', 'Donation Pending'),
        ('Donation_Confirmed', 'Donation Confirmed'),
        ('Rejected', 'Rejected'),
        ('Closed', 'Closed'),
    ]
    
    blood_request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, related_name='donor_requests')
    donor = models.ForeignKey(dmodels.Donor, on_delete=models.CASCADE, related_name='blood_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    response_date = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)
    donation_confirmed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['blood_request', 'donor']
    
    def __str__(self):
        return f"{self.donor} - {self.blood_request.patient_name} - {self.status}"

# Signal to send email notifications
@receiver(post_save, sender=DonorRequest)
def send_donor_notification(sender, instance, created, **kwargs):
    if created and instance.status == 'Pending':
        # Send email to donor about new request
        subject = f'New Blood Request - {instance.blood_request.bloodgroup}'
        message = f"""
        Hello {instance.donor.get_name},
        
        A new blood request has been forwarded to you:
        
        Patient: {instance.blood_request.patient_name}
        Blood Group: {instance.blood_request.bloodgroup}
        Units Needed: {instance.blood_request.unit}
        Reason: {instance.blood_request.reason}
        
        Please log in to your donor dashboard to accept or ignore this request.
        
        Best regards,
        Blood Bank Management System
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.donor.user.email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Failed to send email: {e}")

@receiver(post_save, sender=BloodRequest)
def send_admin_notification(sender, instance, **kwargs):
    if instance.status == 'Accepted':
        # Send email to admin about accepted request
        subject = f'Blood Request Accepted - {instance.patient_name}'
        message = f"""
        A blood request has been accepted by a donor:
        
        Patient: {instance.patient_name}
        Blood Group: {instance.bloodgroup}
        Units: {instance.unit}
        Accepted By: {instance.accepted_by_donor.get_name}
        
        Please review and approve this request in the admin dashboard.
        
        Best regards,
        Blood Bank Management System
        """
        
        try:
            # Send to admin email (you can configure this in settings)
            admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@bloodbank.com')
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [admin_email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Failed to send admin email: {e}")

        