from django.http import HttpResponse
from django.shortcuts import render
from .forms import Custom_userCreationForm, Profile_form, Update_account
from django.contrib.auth import login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages


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
        form = Profile_form(request.POST, instance=request.user.user_info)
        if form.is_valid():
            form.save()
            return HttpResponse("info is successfully saved")
    form = Profile_form(instance=request.user.user_info)
    return render(request, 'accounts/profile.html', {'form': form}) 


def edit_account(request):
    if request.method == "POST":
        user_form=Update_account(request.POST, instance=request.user)
        password_form=PasswordChangeForm(request.user, request.POST)
        if user_form.is_valid():
            user=user_form.save()
            messages.success(request, 'Your info was successfully updated!')

        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, 'Your password was successfully updated!')
            
    user_form=Update_account(instance=request.user)
    password_form=PasswordChangeForm(request.user)
    context={
        'u_form':user_form,
        'p_form':password_form
    }
    return render(request, 'accounts/edit_account.html', context)


