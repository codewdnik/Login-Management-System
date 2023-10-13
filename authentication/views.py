from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login, logout
# from django.core.mail import send_mail
# from django.core.mail import EmailMessage
import smtplib
from email.mime.text import MIMEText

from loginpage import settings


# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST ['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username):
            messages.error(request,"Username already exists!")
            return redirect('home')
        
        # if User.objects.filter(email=email):
        #     messages.error(request,"email already registered")
        #     return redirect('home')
    
        if len(username)> 15:
            messages.error(request, "username must be under 15 characters")

        if password1 != password2:
            messages.error(request,"password didn't match")

        if not username.isalnum():
            messages.error(request,"Username must be alpha numeric")
            return redirect('home')
        
        
        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your Account has been SUCCESSFULLY created. Please confirm your email to continue.")

        #welcome email

        subject = "Welcome to ND DESIGN Login"
        message= "Hello" + myuser.first_name + "!! \n" + "Welcome to ND DESIGN \n Thank You for visiting \n please verify your email to continue"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        # send_mail(subject, message, from_email, to_list, fail_silently=False)

        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
        
        # start TLS for security
        s.starttls()
        
        # Authentication
        s.login("**********@gmail.com", "********")
        
        # message to be sent
        message = "Message_you_need_to_send"
        
        # sending the mail
        s.sendmail("***********@gmail.com", myuser.email, message)
        
        # terminating the session
        s.quit()
        return redirect('signin')

    return render(request, "authentication/signup.html")


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']

        user= authenticate(username=username, password=password1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request,"authentication/index.html", {'fname': fname})

        else:
            messages.error(request, "bad credentials")
            return redirect('home')

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "logged out successfully")
    return redirect('home')