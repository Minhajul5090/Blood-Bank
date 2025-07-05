from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Set up user groups for role-based authentication'

    def handle(self, *args, **options):
        # Create groups if they don't exist
        admin_group, created = Group.objects.get_or_create(name='ADMIN')
        donor_group, created = Group.objects.get_or_create(name='DONOR')
        patient_group, created = Group.objects.get_or_create(name='PATIENT')
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created user groups: ADMIN, DONOR, PATIENT')
            )
        else:
            self.stdout.write(
                self.style.WARNING('User groups already exist: ADMIN, DONOR, PATIENT')
            )
        
        # Assign users to groups based on their existing roles
        from django.contrib.auth.models import User
        from donor.models import Donor
        from patient.models import Patient
        
        # Assign admin users (users not in donor or patient models)
        admin_users = User.objects.filter(is_staff=True, is_superuser=True)
        for user in admin_users:
            user.groups.add(admin_group)
            self.stdout.write(f'Added {user.username} to ADMIN group')
        
        # Assign donor users
        donors = Donor.objects.all()
        for donor in donors:
            if donor.user:
                donor.user.groups.add(donor_group)
                self.stdout.write(f'Added {donor.user.username} to DONOR group')
        
        # Assign patient users
        patients = Patient.objects.all()
        for patient in patients:
            if patient.user:
                patient.user.groups.add(patient_group)
                self.stdout.write(f'Added {patient.user.username} to PATIENT group')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully set up role-based authentication system')
        ) 