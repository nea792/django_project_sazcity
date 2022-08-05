from urllib import request
from django.shortcuts import redirect, render
from .forms import *
from products.models import Product
from django.contrib.auth import login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.http import  Http404
from django.core.paginator import Paginator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


def main_page(request):
    products = Product.objects.all().order_by('-id')
    filter = " "
    
    if 'next' in request.GET:
         messages.error(request, 'ابتدا وارد حساب کاربری خود شوید.')

    if 'filter' in request.GET:
        filter_id = request.GET['filter']
        if filter_id == '1' :
            products = products.order_by('-id')
            filter = "جدید"

        elif filter_id == '2':
            products = sorted(products, key= lambda product : product.avg_rate(), reverse=True)
            filter = "محبوب"

        elif filter_id == '3':
            products = products.order_by('-sold')
            filter = "پر فروش"

        else:
            raise Http404()


    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products_in_page = paginator.get_page(page_number)
    context ={
        'products_in_page' : products_in_page,
        'filter' : filter
    }
    return render(request, 'accounts/main.html', context)


def register_user(request):
    if request.method == "POST":
        form = Custom_userCreationForm(request.POST)
        if form.is_valid():
            form.save()
            #login(request, user)
            messages.success(request, 'ثبت نام با موفقیت انجام شد ')
        else:
            messages.warning(request, 'اطلاعات نادرست است')

    return redirect("main-page")
   

def login_user(request):
    if request.method == "POST":
        form = Custom_authentication_form(data = request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request, user)
            messages.success(request, 'با موفقیت وارد حساب کاربری خود شدید')       
        else:
            messages.warning(request, 'اطلاعات نامعتبر است')

    return redirect("main-page")
    

@login_required(login_url='/')
def logout_user(request):
    if request.method == "POST":
        logout(request)
        messages.error(request, 'با موفقیت از حساب کاربری خود خارج شدید')

    return redirect('/')


@login_required(login_url='/')  
def profile_page(request):
    user = request.user
    user_form = Update_account(instance = user)      
    profile_form = Profile_form(instance = user.user_info)

    context={
        'u_form' : user_form,
        'p_form' : profile_form
    }
    return render(request, 'accounts/profile.html', context) 


# edit main info of user(custom_user table)
@login_required(login_url='/')  
def user_edit(request):
    if request.method == "POST":
        user_form = Update_account(request.POST, instance = request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'اطلاعات با موفقیت بروزرسانی شد')
        else:
            messages.error(request, 'اطلاعات نامعتبر است!')

    return redirect('accounts:profile')
            

# edit user_info table
@login_required(login_url='/')  
def profile_edit(request):
    if request.method == "POST":
        profile_form = Profile_form(request.POST, instance = request.user.user_info)
     
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'اطلاعات با موفقیت بروزرسانی شد')
        else:
             messages.error(request, 'اطلاعات نامعتبر است!')

    return redirect('accounts:profile')

                 
@login_required(login_url = '/')
def edit_password(request):
    if request.method == "POST":
        password_form = Custom_PasswordChangeForm(request.user, request.POST)
      
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, request.user) 
            messages.success(request, 'رمز عبور شما با موفقیت تغییر یافت')
        else:
           messages.error(request, 'رمز عبور وارد شده نامعتبر است.')
    else:
        password_form = Custom_PasswordChangeForm(request.user)

    context={
            'password_form' : password_form
        }

    return render(request, 'accounts/edit_account.html', context)


class Custom_PasswordResetView(UserPassesTestMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = "accounts/password_reset_email.html"
    success_url = reverse_lazy("accounts:password_reset_done")

    def test_func(self):
        return self.request.user.is_anonymous


class Custom_PasswordResetDone(UserPassesTestMixin, PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

    def test_func(self):
        return self.request.user.is_anonymous


class Custom_PasswordResetConfirm(UserPassesTestMixin, PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy("accounts:password_reset_complete")

    def test_func(self):
        print(self.request.session.get('_password_reset_token'))
        return self.request.user.is_anonymous


class Custom_PasswordResetCompelte(UserPassesTestMixin, PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'

    def test_func(self):
        return self.request.user.is_anonymous


def call_us(request):
    if request.method=='POST':
        call_form = Call_form(request.POST)

        if call_form.is_valid():
            subject = call_form.cleaned_data['subject']
            msg = call_form.cleaned_data['message']
            if not request.user.is_anonymous:
                new_line ='\n'
                msg += f"{new_line} this email is sent from {request.user.email}"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [settings.EMAIL_HOST_USER, ]
            send_mail( subject, msg, email_from, recipient_list )
            messages.success(request, 'پیام با موفقیت ارسال شد')
        else:
            messages.warning(request, 'اطلاعات نا معتبر است ')
        return redirect("accounts:call")

    call_form = Call_form()
    context ={
        'call_form' : call_form

    }
    return render(request, 'accounts/call.html', context)


#custom error 404 page
def error_404(request, exception):
    return render(request, 'accounts/404.html')
