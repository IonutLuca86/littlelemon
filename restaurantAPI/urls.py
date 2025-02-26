from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('about/',views.about, name='about'),
    
    path('restaurant/menu/', views.menu_items, name='menu'),
    path('restaurant/menu/<int:pk>/', views.single_menu_item, name='menu_item'),   
    path('restaurant/menu/delete_item/<int:pk>/', views.delete_menu_item, name='delete_item'), 
    path('restaurant/menu/add/', views.add_menu_item, name='add_item'), 
    path('restaurant/menu/edit_item/<int:pk>/', views.edit_menu_item, name='edit_item'), 
    
    path('restaurant/book', views.book, name='book'),
    path('restaurant/booking/<int:pk>', views.single_booking, name='booking'),
    path('restaurant/booking/delete/<int:pk>', views.delete_booking, name='delete_booking'),
    path('restaurant/booking/edit/<int:pk>', views.edit_booking, name='edit_booking'),
    path('restaurant/bookings/', views.all_reservations, name="bookings"),

    path('restaurant/login/',views.user_login, name='login'),
    path('restaurant/logout/',views.logout_view, name='logout'),
    path('restaurant/register/', views.register, name='register'),
    path('restaurant/userinfo/', views.userInfo, name='userinfo'),
    path('restaurant/user/change_password/', views.ChangePasswordView.as_view(), name='change_password'),

]