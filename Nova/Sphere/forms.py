from django import forms
from .models import ContactMessage, PaymentVerification
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

class PaymentVerificationForm(forms.ModelForm):
    class Meta:
        model = PaymentVerification
        fields = ['full_name', 'phone_number', 'email', 'mpesa_code']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'John Doe'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'e.g. 0712345678'}),
            'email': forms.EmailInput(attrs={'placeholder': 'e.g. john@example.com'}),
            'mpesa_code': forms.TextInput(attrs={'placeholder': 'e.g. QBC4XYZ123'}),
        }

#SWAS TASKS
class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']