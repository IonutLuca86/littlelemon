from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view, permission_classes
from .models import Menu, Booking
from .serializers import MenuItemSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, BookingForm, MenuForm
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from rest_framework.authtoken.models import Token
from django.contrib import messages
from django.http.response import HttpResponseNotAllowed
import datetime

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


@login_required
def add_menu_item(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = MenuForm()
    return render(request,'add_menu_item.html',{'form': form})


@login_required
def edit_menu_item(request,pk):   
    item = get_object_or_404(Menu,pk=pk)
    if request.method == 'POST':       
        form = MenuForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item has been successfully modified!")
            return redirect('menu_item',pk=pk)
    else:
        form = MenuForm(instance=item)
    return render(request,'edit_item.html',{'form': form, 'item': item})


@login_required
def delete_menu_item(request,pk):
    if request.method == 'POST':
        item = get_object_or_404(Menu,pk=pk)
        item.delete()
        messages.success(request, "Menu item has been deleted!")
        return redirect('menu')
    return HttpResponseNotAllowed(['POST'])


@login_required
def book(request):
    form = BookingForm()
    user_bookings = Booking.objects.filter(user_id = request.user)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user_id = request.user
            booking.save()
            messages.success(request, "Your booking has been registered!")
        else:
            messages.error(request,"There was an error with your booking registration! Please try again!")
    
    selected_date_str = request.GET.get('date', None)
    if selected_date_str:
        selected_date = datetime.datetime.strptime(selected_date_str, "%Y-%m-%d").date()
    else:
        selected_date = datetime.date.today()
    booked_slots = Booking.objects.filter(bookingDate=selected_date).values_list('reservation_time',flat=True)
    all_slots = list(range(9,21))
    current_hour = datetime.datetime.now().hour
    if selected_date == datetime.date.today():
        all_slots = [slot for slot in all_slots if slot > current_hour]
    available_slots = [slot for slot in all_slots if slot not in booked_slots]
    
    context = {'form':form,
               'available_slots': available_slots,
               'selected_date': selected_date,
               'user_bookings': user_bookings}
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
    
    
    
