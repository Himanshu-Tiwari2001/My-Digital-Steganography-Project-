from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model 
from django.core.validators import RegexValidator
from dashboard.models import Image  # Import the Image model from the dashboard app

# class RegisterForm(UserCreationForm):
#     email=forms.CharField(widget=forms.EmailInput(attrs={"placeholder": "Enter email-address", "class": "form-control"}))
#     username=forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter email-username", "class": "form-control"}))
#     password1=forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Enter password", "class": "form-control"}))
#     password2=forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"placeholder": "Confirm password", "class": "form-control"}))
    
    
#     class Meta:
#         model = get_user_model()
#         fields = ["email", "username", "password1", "password2","date_of_birth"]class RegisterForm(UserCreationForm):
class RegisterForm(UserCreationForm):
    fullname = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter your name", "class": "form-control"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"placeholder": "Enter email-address", "class": "form-control"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter email-username", "class": "form-control"}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Enter password", "class": "form-control"}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"placeholder": "Confirm password", "class": "form-control"}))
    phone_number = forms.CharField(max_length=15, validators=[RegexValidator(regex=r'^\d{10,15}$', message="Phone number must be 10-15 digits")], widget=forms.TextInput(attrs={"placeholder": "Enter phone number", "class": "form-control"}))
    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={"placeholder": "Enter date of birth (YYYY-MM-DD)", "class": "form-control", "autocomplete": "off"},
            format='%Y-%m-%d'
        ),
        help_text='Format: YYYY-MM-DD'
    )
    # profile_image = forms.ImageField(label="Profile Image", required=False)  # Add a field for the profile image upload
    
    class Meta:
        model = get_user_model()
        fields = ["fullname","email", "username", "password1", "password2", "phone_number","date_of_birth"]