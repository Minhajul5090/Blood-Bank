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

class DonorUserForm(forms.ModelForm):
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

class DonorForm(forms.ModelForm):
    bloodgroup = forms.ChoiceField(choices=BLOOD_GROUP_CHOICES, help_text="Select your blood group")
    age = forms.IntegerField(min_value=18, max_value=65, help_text="Age must be between 18 and 65 years")
    
    class Meta:
        model=models.Donor
        fields=['bloodgroup','age','address','mobile','profile_pic']
        widgets = {
            'mobile': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter your address'}),
        }

class DonationForm(forms.ModelForm):
    # New blood group field with better styling and functionality
    blood_group = forms.ChoiceField(
        label='Blood Group',
        choices=[('', '-- Select Blood Group --')] + BLOOD_GROUP_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control blood-group-select',
            'required': 'true',
            'name': 'blood_group',
            'id': 'blood_group',
            'style': 'width: 100%; padding: 15px 20px; border: 2px solid #e1e5e9; border-radius: 10px; font-size: 1rem; transition: all 0.3s ease; background: #f8f9fa; cursor: pointer;'
        })
    )
    
    class Meta:
        model=models.BloodDonate
        fields=['disease','unit']
        widgets = {
            'disease': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter any disease or "Nothing"',
                'required': 'true',
                'style': 'width: 100%; padding: 15px 20px; border: 2px solid #e1e5e9; border-radius: 10px; font-size: 1rem; transition: all 0.3s ease; background: #f8f9fa;'
            }),
            'unit': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter blood unit in ml',
                'min': '1',
                'max': '500',
                'required': 'true',
                'style': 'width: 100%; padding: 15px 20px; border: 2px solid #e1e5e9; border-radius: 10px; font-size: 1rem; transition: all 0.3s ease; background: #f8f9fa;'
            }),
        }

class DonorEditForm(forms.ModelForm):
    """Form for editing donor profile - password fields are optional"""
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
