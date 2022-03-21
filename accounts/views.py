from django.http import HttpResponse
from django.shortcuts import render
from .forms import Custom_userCreationForm, Profile_form
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm


def register_user(request):
    if request.method == "POST":
        form = Custom_userCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            return HttpResponse("register is successfully")

    form = Custom_userCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
   

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request, user)
            return HttpResponse("login is successfully")

    form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})
   

def logout_user(request):
    if request.method == "POST":
        #if request.user != "AnonymousUser":
           # print("logined")
        logout(request)
        return HttpResponse("logout is successfully")
    
    return render(request, 'accounts/logout.html')

    
def profile_user(request):
    if request.method == "POST":
        form = Profile_form(request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user = request.user
            instance.save()
            return HttpResponse("info is successfully saved")

    form = Profile_form()
    return render(request, 'accounts/profile.html', {'form': form}) 