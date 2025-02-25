from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Booking, Menu

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        

class BookingForm(forms.ModelForm):    
    class Meta:
        model = Booking
        exclude = ['user_id']
        fields = ['name','no_of_guests','bookingDate','reservation_time']
        widgets = {
            'bookingDate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reservation_time': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'no_of_guests': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
        
class CustomChangePasswordForm(PasswordChangeForm):
    old_password = forms.PasswordInput
    new_password1 = forms.PasswordInput
    new_password2 = forms.PasswordInput
    
    
class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['title','description','price','inventory']