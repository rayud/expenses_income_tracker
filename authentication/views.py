from django.shortcuts import render, redirect
from django.views import View 
import json
from django.http import JsonResponse
from django.contrib.auth.models import User 
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.contrib import auth

class RegistrationView(View) : 
    def get(self, request) : 
        return render(request, 'authentication/register.html')
    
    def post(self, request) : 
        
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'fieldValues' : request.POST
        }

        if not User.objects.filter(username=username).exists() : 
            if not User.objects.filter(email=email).exists() : 
                if len(password) < 6 : 
                    messages.warning(request, "Password is too short and It should contains min 6 characters")
                    return render(request, 'authentication/register.html', context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = True 
                user.save()
                messages.success(request, "User Created successfully")
                return render(request, 'authentication/register.html')
        return render(request, 'authentication/register.html')


class LoginView(View) : 
    def get(self, request) : 
        return render(request, 'authentication/login.html')
    
    def post(self, request) : 
        username = request.POST['username']
        password = request.POST['password']

        if username and password : 
            user = auth.authenticate(username=username, password=password)
            if user: 
                auth.login(request, user)
                messages.success(request, 'Welcome, '+user.username+' you are now logged in')
                return redirect('expenses')
            else:
                messages.error(request, 'Invalid credentials, Try again')
                return render(request, 'authentication/login.html')
        else: 
            messages.error(request, 'Enter all fields')
            return render(request, 'authentication/login.html')

class LogoutView(View) : 
    def get(self, request) : 
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('expenses')
        
class UserNameValidationView(View) : 
    def post(self, request) : 
        data = json.loads(request.body)
        username = data['username']

        if User.objects.filter(username=username).exists() : 
            return JsonResponse(
                {'username_error':"sorry username is in user, choose another one!"}, 
                status=409)
        if not str(username).isalnum() : 
            return JsonResponse(
                {'username_error': "Username shold only contain alphanumeric"}
            )
        return JsonResponse({
            'username_valid': True
        })


class EmailValidationView(View) : 
    def post(self, request): 
        data = json.loads(request.body)
        email = data['email']
        print(type(email))
        if not validate_email(email) : 
            return JsonResponse({'email_error':'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists() : 
            return JsonResponse({'email_error':'sorry email in use, choose another email'})
        return JsonResponse({'email_valid': True})