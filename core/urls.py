from django.urls import path
from .views import (
    appointment_view, 
    contact_view, 
    load_doctors, 
    index_view, 
    login_view, 
    register_view, 
    logout_view,
    profile_view,
    update_profile,
    )

urlpatterns = [
    path("", index_view, name="index"), # here we'll load the full landing page
    
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path('profile/edit/', update_profile, name='update-profile'),
    
    path("appointment/", appointment_view, name="appointment"),
    path("load-doctors/", load_doctors, name="load-doctors"),
    path("contact/", contact_view, name="contact"),
]
