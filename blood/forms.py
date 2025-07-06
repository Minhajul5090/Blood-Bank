from django import forms

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

class BloodForm(forms.ModelForm):
    class Meta:
        model=models.Stock
        fields=['bloodgroup','unit']

class RequestForm(forms.ModelForm):
    bloodgroup = forms.ChoiceField(
        choices=[('', '-- Select Blood Group --')] + BLOOD_GROUP_CHOICES,
        help_text="Select the required blood group"
    )
    
    class Meta:
        model=models.BloodRequest
        fields=['patient_name','patient_age','reason','bloodgroup','unit']
        widgets = {
            'patient_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter patient\'s full name',
                'required': 'true'
            }),
            'patient_age': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter patient\'s age',
                'min': '1',
                'max': '120',
                'required': 'true'
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Please describe the reason for blood request (e.g., surgery, accident, medical condition)',
                'required': 'true',
                'rows': '4'
            }),
            'unit': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter units needed (in ml)',
                'min': '1',
                'max': '10000',
                'required': 'true'
            }),
        }
