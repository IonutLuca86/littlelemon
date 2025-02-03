from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Booking

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        

class BookingForm(forms.ModelForm):
    
    class Meta:
        model = Booking
        fields = ['name','no_of_guests','bookingDate','reservation_time']
        
class CustomChangePasswordForm(PasswordChangeForm):
    old_password = forms.PasswordInput
    new_password1 = forms.PasswordInput
    new_password2 = forms.PasswordInput