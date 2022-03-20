from django.http import HttpResponse
from django.shortcuts import render
from .forms import Custom_userCreationForm
from django.contrib.auth import login
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
   
