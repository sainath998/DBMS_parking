"""parkin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# from django.contrib.auth.views import views as auth_views

from personal.views import (
    home_view,
    user_home_view,
    aboutus_view,
    slot_status_view,
    slot_booking_view,
    add_vehicle_view,
    all_vehicles_view,
    changeParkingView,
    all_bookings_view,
)

from account.views import (
    UserAuthenticationView,
    UserRegistrationView,
    logout_view,
    UserProfileView,
    admin_page_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', admin_page_view, name="admin_page"),
    
    path('', home_view, name="siteHome"),
    path('slotStatus/', slot_status_view, name="slotStatus"),
    path('slotBooking/<slot_id>/', slot_booking_view, name="slotBooking"),
    path('userHome/', user_home_view , name="userHome"),
    path('add_vehicle/', add_vehicle_view, name="add_vehicle"),
    path('all_vehicles/', all_vehicles_view, name="all_vehicles"),
    path('changeParking/<parked_slot_id>/', changeParkingView, name="changeParking"),
    path('bookings/', all_bookings_view, name="all_bookings"),

    path('aboutus/', aboutus_view, name="about us"),
    path('userHome/logout/', logout_view, name="logout"),

    path('register/', UserRegistrationView, name="register"),
    path('login/', UserAuthenticationView, name="login"),
    path('userHome/profile/', UserProfileView, name="My Profile"),
]

