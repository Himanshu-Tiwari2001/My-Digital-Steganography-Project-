
from django.urls import path
from . import views 
from dashboard.views import dashboard

from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.signup, name="register"),
    path("verify-email/<str:username>", views.verify_email, name="verify-email"),
    path("resend-otp", views.resend_otp, name="resend-otp"),
    path("login", views.signin, name="signin"),
    path('aboutus/' , views.aboutUS,  name ="aboutUs"),
    path('contact/' , views.contact,  name ="contact"),
    path('mainwork/',views.mainwork,name='mainwork'),
    path('execute/',views.execute_image, name='execute_image'),
    path('executeaudio/',views.execute_audio, name='execute_audio'),
    path('executevideo/',views.execute_video, name='execute_video'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    

    path('', auth_views.LogoutView.as_view(), name='logout'),
    
]
