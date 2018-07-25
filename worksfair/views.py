from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

# Create your views here.
# index page view
def index(request):
  signed_in = request.user.is_authenticated
  if signed_in:
    username = request.user.username
    user = User.objects.get(username=username)
    firstname = user.first_name
    lastname = user.last_name
    context = {
      'signed_in': signed_in,
      'username': username,
      'firstname': firstname,
      'lastname': lastname
    }
    return render(request, 'worksfair/index.html', context)
  else:
    return render(request, 'worksfair/index.html')


# login page
def signin(request):
  return render(request, 'worksfair/sign-in.html', {})


# handle login post
def login_view(request):

  if request.method == 'POST':
    try:
      email = request.POST['username']
      password = request.POST['password']
    except (KeyError):
      context = {
        "login_error": 'Fill in the values in the form'
      }
      return render(request, "worksfair/sign-in", context)

    if len(email) < 1 or len(password) < 1:
      context = {
        "login_error": 'Fill in the values in the form'
      }
      return render(request, "worksfair/sign-in.html", context)
    
    try:
      user_email = User.objects.get(email=email)
    except (KeyError, User.DoesNotExist):
      context = {
        "login_error": 'Incorrect email or password',
        "email": email
      }
      return render(request, "worksfair/sign-in.html", context)

    user = authenticate(username=user_email.username, password=password)

    if user is not None:
      login(request, user)
      return redirect('/worksfair/')
    else:
      context = {
        "login_error": 'Incorrect email or password',
        "email": email
      }
      return render(request, "worksfair/sign-in.html", context)

    
# handle logout post
def logout_view(request):
  logout(request)
  return redirect('/worksfair/')


# handle register post
def register_view(request):
  if request.method == 'POST':

    try:
      firstname = request.POST['username2']
      lastname = request.POST['username3']
      username = request.POST['username4']
      email = request.POST['email']
      password = request.POST['password1']
      confirm_password = request.POST['password2']
    except (KeyError):
      context = {
        "signup_error": 'Fill in the values in the form'
      }
      return render(request, 'worksfair/sign-in.html', context)

    if (
        len(firstname) < 1 or
        len(lastname) < 1 or
        len(username) < 1 or
        len(email) < 1 or
        len(password) < 1 or
        len(confirm_password) < 1
      ) :
      context = {
        "signup_error": 'Fill in the values in the form'
      }
      return render(request, "worksfair/sign-in.html", context)

    if (password == confirm_password):
      existing_user = False
      try:
        user = User.objects.get(username=username)
      except (KeyError, User.DoesNotExist):
        existing_user = True

      if not existing_user:
        context = {
          "signup_error": 'A user already exists with this username',
          "firstname": firstname,
          "lastname": lastname,
          "email": email
        }
        print('checked values did not here >>>>>>>>>')
        return render(request, "worksfair/sign-in.html", context)
      else:
        existing_email = False
        try:
          email = User.objects.get(email=email)
        except (KeyError, User.DoesNotExist):
          existing_email = True

        if not existing_email:
          context = {
            "signup_error": 'A user already exists with this email',
            "firstname": firstname,
            "lastname": lastname,
            "username": username
          }
          return render(request, "worksfair/sign-in.html", context)
        else:
          user = User.objects.create_user(username, email, password)
          user.first_name = firstname
          user.last_name = lastname
          user.save()
          login(request, user)
          return redirect('/worksfair/')

    else:
      context = {
              "signup_error": 'Please confirm your password',
              "firstname": firstname,
              "lastname": lastname,
              "email": email,
              "username": username
            }
      print('did not checked values here >>>>>>>>>')
      return render(request, "worksfair/sign-in.html", context)
