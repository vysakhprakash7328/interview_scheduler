from django.urls import path
from . import views

urlpatterns = [
    
    path('register_user/', views.Register_user.as_view(), name='register_user'),
    path('get_users/', views.Get_users.as_view(), name='get_users'),
    path('register_availability/', views.Register_Availability.as_view(), name='register_availability'),
    path('get_availabllity/', views.Get_Available_Timeslots.as_view(), name='get_availabllity'),
    
]