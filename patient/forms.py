from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . import models

# Blood group choices
BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
]

class PatientUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())
    
    class Meta:
        model=User
        fields=['first_name','last_name','username','email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove password validation restrictions
        self.fields['password1'].help_text = "Enter your password"
        self.fields['password2'].help_text = "Confirm your password"
        self.fields['username'].help_text = "Enter any username you prefer"
        
        # Make email optional
        self.fields['email'].required = False
        
        # Remove all validators from password fields
        self.fields['password1'].validators = []
        self.fields['password2'].validators = []
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class PatientForm(forms.ModelForm):
    bloodgroup = forms.ChoiceField(
        choices=BLOOD_GROUP_CHOICES, 
        help_text="Select your blood group",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model=models.Patient
        fields=['age','bloodgroup','disease','address','doctorname','mobile','profile_pic']
        widgets = {
            'mobile': forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'class': 'form-control'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter your address', 'class': 'form-control'}),
            'doctorname': forms.TextInput(attrs={'placeholder': 'Enter your doctor name', 'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'disease': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }

class PatientEditForm(forms.ModelForm):
    """Form for editing patient profile - password fields are optional"""
    password1 = forms.CharField(label='New Password (optional)', widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(label='Confirm New Password (optional)', widget=forms.PasswordInput(), required=False)
    
    class Meta:
        model=User
        fields=['first_name','last_name','username','email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove password validation restrictions
        self.fields['password1'].help_text = "Leave blank to keep current password"
        self.fields['password2'].help_text = "Confirm new password"
        self.fields['username'].help_text = "Enter any username you prefer"
        
        # Make email optional
        self.fields['email'].required = False
        
        # Remove all validators from password fields
        self.fields['password1'].validators = []
        self.fields['password2'].validators = []
        
        # Add CSS classes for better styling
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get("password1"):
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
