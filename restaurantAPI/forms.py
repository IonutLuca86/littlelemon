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
        
        
class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100, required=True, 
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=10, min_length=10, required=True, 
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123 456 78 90'}))
    address = forms.CharField(max_length=255, required=True, 
                              widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    card_number = forms.CharField(max_length=16, min_length=16, required=True, 
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234 5678 9012 3456'}))
    expiration_date = forms.CharField(max_length=5, required=True, 
                                      widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'}))
    cvv = forms.CharField(max_length=3, min_length=3, required=True, 
                          widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'CVV'}))
