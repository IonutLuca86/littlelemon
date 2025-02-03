from django.shortcuts import render, redirect
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view, permission_classes
from .models import Menu, Booking
from .serializers import MenuItemSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, BookingForm, CustomChangePasswordForm
from django.contrib.auth.models import Group
from rest_framework.response import Response
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from rest_framework.authtoken.models import Token

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request,'about.html')

def menu_items(request):
    menu_items = Menu.objects.all()
    return render(request,'menu.html',{'menu': menu_items})

def single_menu_item(request,pk):
    item = Menu.objects.get(pk=pk)
    return render(request, 'menu_item.html',{'item': item})

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)

@login_required
@permission_classes([IsAuthenticated])
def userInfo(request):
    user = request.user
    data = {
        'username': user.username,
        'email': user.email,
        'firstname': user.first_name,
        'lastname': user.last_name,
    }
    return render(request, 'userinfo.html',{'context': data})


# @api_view()
# @permission_classes([IsAuthenticated])
# def msg(request):
#     return Response({'msg':'This view is protected'})

class MenuItemList(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuItemSerializer
    

class MenuItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuItemSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
# def MenuItemsView(request):
#     queryset = Menu.objects.all()
#     permission_classes = [IsAuthenticated]
#     serializer_class = MenuItemSerializer
    

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            customer_group = Group.objects.get(name='customer')
            user.groups.add(customer_group)
            
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect('home')
    else:
        form = RegisterForm()
        
    return render(request, 'register.html', {'form': form})   
    
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':        
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()  
            logout(request)  
        return redirect('home')

class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')
    template_name = 'change_password.html'
    