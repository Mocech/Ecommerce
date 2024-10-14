from django.shortcuts import render, redirect
from .forms import UserForm, UserLogin
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import auth  

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_authentication:login')
    else:
        form = UserForm()
        
    return render(request, 'app1/signup.html', {'register': form})  

def user_login(request):
    form = UserLogin(request, data=request.POST)
    context={
                'login': form,
                'show_nav':False,
                'show_footer':False,
            }
    if request.method == 'POST':
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                # Redirect to the home page after successful login
                return redirect('store:home')  # Adjust this if your home URL name is different
         

    return render(request, 'app1/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('store:home')
