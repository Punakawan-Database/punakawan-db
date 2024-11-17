# forms.py di app authentication
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class PenggunaRegistrationForm(UserCreationForm):
    # Form Fields
    full_name = forms.CharField(max_length=100, required=True, label="Nama Lengkap")
    gender = forms.ChoiceField(choices=[('L', 'Laki-laki'), ('P', 'Perempuan')], widget=forms.RadioSelect, required=True, label="Jenis Kelamin")
    phone_number = forms.CharField(max_length=15, required=True, label="Nomor HP")
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True, label="Tanggal Lahir")
    address = forms.CharField(widget=forms.Textarea, required=True, label="Alamat")

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'full_name', 'email', 'gender', 'phone_number', 'birth_date', 'address']

    # Custom Validation for Phone Number Uniqueness
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Nomor HP ini telah terdaftar. Silakan login.")
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'customer'  # Set the default role to customer
        if commit:
            user.save()
        return user
        
class PekerjaRegistrationForm(UserCreationForm):
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
