from django.shortcuts import render
from .forms import UserForm,UserProfileInfoForm,SignupForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


def index(request):
    return render(request, 'dappx/index.html')


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'dappx/index.html')


# =============================================== Register Method ================================================= #

"""
    This Method Is Used To Singup The New User 
    Take The Form Data As Post Then Rigister The User Account For Login
"""


def register(request):

    registered = False              # Assign register as False
    if request.method == 'POST':      # Check If Form Request Type Is Post
        user_form = UserForm(data=request.POST)                # If Request Is Post Then Read Form Data
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():   # Checking Form Validation 
            user = user_form.save()                             # Save Form To Database
            user.set_password(user.password)                    # Set Password
            # Assign Users Active State Is False It Will Assign True After Visiting The Activation Link
            user.is_active = False                              
            user.save()                 # Save User Data
            profile = profile_form.save(commit=False)       
            profile.user = user         
            current_site = get_current_site(request)  # Get Current Site Urt
            # Creating Message Body For Sending The Activation Link
            
            mail_subject = 'Activate Your Site Account'     # Mail Subject
            message = render_to_string('dappx/acc_active.html', {   # Redirect To Activation Link Template
                'user': user,                                          # User Name
                'domain': current_site.domain,                          # Current Site Domain
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),     # Encode UserId
                # takes user id and generates the base64 code(uidb64)
                # Here we receive uidb64, token. By using the "urlsafe_base64_decode"
                # we decode the base64 encoded uidb64 user id.
                # We query the database with user id to get user
                'token': account_activation_token.make_token(user),     # Token
                # takes the user object and generates the onetime usable token for the user(token)
            })
            email = EmailMessage(mail_subject, message, to=[user.email] # Make EmailMessage Object With Message
            )
            email.send()            # Send Mail To Given Email
            return HttpResponse('Please confirm your email address to complete the registration')
            # Response For Activation
            if 'profile_pic' in request.FILES:  
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
                profile.save()
                registered = True       # Save register True
            else:
                print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'dappx/registration.html',
                          {'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})


# ======================================== Account Activation Method ========================================== #

"""
    
    This Method Is Use To Activate The Account Take 3 Params
    It Get Fired When The User Clicks On The Activation Link
    1. Request Default
    2. Uid
    3. The Generated Token

"""


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))  # Decode The UID
        user = User.objects.get(pk=uid)                  # Get User ID
    except(TypeError, ValueError, OverflowError, User.DoesNotExist): # Except The Value Error
        user = None             
    # Check If User Is Not None And Validate The Token With User 
    if user is not None and account_activation_token.check_token(user, token):  
        # If Both The Conditions Are True Then Update The Users Active Status As True
        user.is_active = True                                                       
        user.save()             # Save The User Data
        login(request, user)    # Login The User
        return HttpResponseRedirect(reverse('index'))       # Redirect To The Index Page
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:                           
        return HttpResponse('Activation link is invalid Or Deactivated Account..!')  # Else Print The Message


# ======================================== Login Method ========================================== #

"""
    The User_Login Method Do The Login Process

"""


def user_login(request):                
    if request.method == 'POST':        # Chek The Method Of The Form If Post Then 
        username = request.POST.get('username')     # Take User Name From Forms Post Method
        password = request.POST.get('password')     # Take Password From Forms Post Method
        user = authenticate(username=username, password=password)    # Authentocate the Username And Password
        if user:                    # If It Returns The True Then Check The
            if user.is_active:      # Check The Uer Activation Status If True Then Login 
                # payload = {
                # 'id': user.id,
                # }
                # encoded_token = jwt.encode({'user_id': user.id}, 'SECRET', algorithm='HS256')
                login(request, user)         # User Login Method Call
                return HttpResponseRedirect(reverse('index'))   # Return To The Index
            else:                                               # Else Write Response
                return HttpResponse("Your Account Is Inactive.")    # Account Is Inactive
        else:
            print("Someone tried to login and failed.")             # Printing The Validation Messages
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'dappx/login.html', {})          # Return Back To Login


def reset_password(request):
    return render(request,'dappx/password_reset_complete.html')
    

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return HttpResponseRedirect('dappx/index.html')