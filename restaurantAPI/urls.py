from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register('tables', views.BookingViewSet, basename='booking')

urlpatterns = [
    path('', views.index, name='home'),
    path('about/',views.about, name='about'),
    path('restaurant/menu/', views.menu_items, name='menu'),
    path('restaurant/menu/<int:pk>/', views.single_menu_item, name='menu_item'),   
    path('restaurant/menu/delete_item/<int:pk>/', views.delete_menu_item, name='delete_item'), 
    path('restaurant/menu/add/', views.add_menu_item, name='add_item'), 
    path('restaurant/menu/edit_item/<int:pk>/', views.edit_menu_item, name='edit_item'), 
    # path('restaurant/booking/', include(router.urls)),
    path('restaurant/book', views.book, name='book'),
    path('restaurant/login/',views.user_login, name='login'),
    path('restaurant/logout/',views.logout_view, name='logout'),
    path('restaurant/register/', views.register, name='register'),
    path('restaurant/userinfo/', views.userInfo, name='userinfo'),
    path('restaurant/user/change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    # path('api-token-auth/', obtain_auth_token, name='api-auth'),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
]