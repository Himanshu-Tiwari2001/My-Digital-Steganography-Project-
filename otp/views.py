from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import OtpToken
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from subprocess import Popen
from django.contrib.auth.decorators import login_required
from dashboard.models import UserActivity
import os
from django.views.decorators.csrf import csrf_protect

from django.db.models import Count
import logging

logger = logging.getLogger(__name__)


# Create your views here.

def index(request):
    return render(request, "index.html")



def signup(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! An OTP was sent to your Email")
            return redirect("verify-email", username=request.POST['username'])
    context = {"form": form}
    return render(request, "signup.html", context)




def verify_email(request, username):
    user = get_user_model().objects.get(username=username)
    user_otp = OtpToken.objects.filter(user=user).last()
    
    
    if request.method == 'POST':
        # valid token
        if user_otp.otp_code == request.POST['otp_code']:
            
            # checking for expired token
            if user_otp.otp_expires_at > timezone.now():
                user.is_active=True
                user.save()
                messages.success(request, "Account activated successfully!! You can Login.")
                return redirect("signin")
            
            # expired token
            else:
                messages.warning(request, "The OTP has expired, get a new OTP!")
                return redirect("verify-email", username=user.username)
        
        
        # invalid otp code
        else:
            messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
            return redirect("verify-email", username=user.username)
        
    context = {}
    return render(request, "verify_token.html", context)




def resend_otp(request):
    if request.method == 'POST':
        user_email = request.POST["otp_email"]
        
        if get_user_model().objects.filter(email=user_email).exists():
            user = get_user_model().objects.get(email=user_email)
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            
            
            # email variables
            subject="Email Verification"
            message = f"""
                                Hi {user.username}, here is your OTP {otp.otp_code} 
                                it expires in 5 minute, use the url below to redirect back to the website
                                http://127.0.0.1:8000/verify-email/{user.username}
                                
                                """
            sender = "virathimanshu99@gmail.com"
            receiver = [user.email, ]
        
        
            # send email
            send_mail(
                    subject,
                    message,
                    sender,
                    receiver,
                    fail_silently=False,
                )
            
            messages.success(request, "A new OTP has been sent to your email-address")
            return redirect("verify-email", username=user.username)

        else:
            messages.warning(request, "This email dosen't exist in the database")
            return redirect("resend-otp")
        
           
    context = {}
    return render(request, "resend_otp.html", context)




def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:    
            login(request, user)
            # messages.success(request, f"Welcome {request.user.username}, you are now logged-in")
            return redirect("mainwork")
        
        else:
            messages.warning(request, "Invalid credentials")
            return redirect("signin")
        
    return render(request, "login.html")

def aboutUS(request):
    return render(request,"aboutus.html")

def contact(request):
    return render(request,"contact.html")    

def mainwork(request):
    return render(request, 'mainwork.html') 

# def dashboard(request):
#     return render(request, 'dashboard.html') 

def profile(request):
    return render(request, 'profile.html')     

# def execute_image(request):
#     # Execute the Tkinter UI-based Python script using subprocess
#    Popen(["python", "D:\\finalproject\\finalproject\\finalproject\\imagestego.py"])
#    return render(request, 'mainwork.html')    
    
# def execute_audio(request):
#     # Execute the Tkinter UI-based Python script using subprocess
#    Popen(["python", "D:\\finalproject\\finalproject\\finalproject\\audiostego.py"])
#    return render(request, 'mainwork.html')  

# def execute_video(request):
#     # Execute the Tkinter UI-based Python script using subprocess
#    Popen(["python", "D:\\finalproject\\finalproject\\finalproject\\videostego.py"])
#    return render(request, 'mainwork.html')     

def record_activity(user, activity_type):
    UserActivity.objects.create(user=user, activity_type=activity_type)
    
@csrf_protect
@login_required
def execute_image(request):
    record_activity(request.user, 'image')
    Popen(["python", os.path.join("D:\\finalyearprojectt\\finalyearproject\\final_year_project\\imagestego.py")])
    return render(request, 'mainwork.html') 

# Ensure the path to the template is correct
@csrf_protect
@login_required
def execute_audio(request):
    record_activity(request.user, 'audio')
    Popen(["python", os.path.join("D:\\finalyearprojectt\\finalyearproject\\final_year_project\\audiostego.py")])
    return render(request, 'mainwork.html')  # Ensure the path to the template is correct

@csrf_protect
@login_required
def execute_video(request):
    record_activity(request.user, 'video')
    Popen(["python", os.path.join("D:\\finalyearprojectt\\finalyearproject\\final_year_project\\videostegofinal.py")])
    return render(request, 'mainwork.html')  # Ensure the path to the template is correct

@csrf_protect
@login_required
def dashboard(request):
    activities = UserActivity.objects.filter(user=request.user).order_by('-timestamp')
    # print(f"User: {request.user}")  # Debug line to print the user
    # print(f"Activities: {activities}")  # Debug line to print the activities
    # context = {'activities': activities}
    # return render(request, 'dashboard.html')

    logger.debug(f"User {request.user.username} activities: {activities}")
    activity_counts = activities.values('activity_type').annotate(count=Count('activity_type'))
    logger.debug(f"User {request.user.username} activity counts: {activity_counts}")
    context = {
        'activities': activities,
        'activity_counts': activity_counts,
    }
    return render(request, 'dashboard.html', context)


def logout(request):
    return render(request, 'index.html')     