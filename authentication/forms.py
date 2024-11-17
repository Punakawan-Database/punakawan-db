# forms.py di app authentication
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True)
    age = forms.IntegerField(required=True)
    gender = forms.ChoiceField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'full_name', 'email', 'age', 'gender', 'phone_number', 'role']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'age', 'gender', 'phone_number']

class EditPhotoForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_photo']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
