from .models import Custom_user, User_info
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django import forms
from django.utils.translation import  gettext_lazy as _


class Custom_userCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _("دو رمز عبور یکسان نیستند"),
    }
    username = forms.CharField(label=_("نام کاربری"), widget= forms.TextInput (attrs={'placeholder':'نام کاربری'}), help_text=_('Required. 30 characters or fewer. Letters, digits and ''@/./+/-/_ only.'))
    email = forms.EmailField(label=_("ایمیل"), widget= forms.TextInput (attrs={'placeholder':'ایمیل'}))
    password1 = forms.CharField(label=_("رمز عبور"), widget=forms.PasswordInput(attrs={'placeholder':'رمز عبور'}))
    password2 = forms.CharField(label=_("تکرار رمز عبور"), widget=forms.PasswordInput(attrs={'placeholder':'تکرار رمز عبور'}), help_text=_("رمز عبور قسمت بالا را تکرار کنید."))
    class Meta:
        model = Custom_user
        fields = ['username','email']
        
 
class Custom_authentication_form(AuthenticationForm):
    username = forms.CharField(label=_("نام کاربری"), max_length=254)
    password = forms.CharField(label=_("رمز عبور"), widget=forms.PasswordInput)


class Custom_PasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(label=_("رمز عبور قبلی"), widget=forms.PasswordInput)

    new_password1 = forms.CharField(label=_("رمز عبور جدید"), widget=forms.PasswordInput)

    new_password2 = forms.CharField(label=_("تکرار رمز عبور جدید"), widget=forms.PasswordInput)
   

class Profile_form(ModelForm):
    post_code = forms.CharField(max_length=10, min_length=10, label=_("کد پستی"))
    phone_number = forms.CharField(max_length=11, min_length=11, label=_("شماره همراه"))
    class Meta:
        model = User_info
        fields = ['first_name', 'last_name', 'address_1', 'address_2', 'state', 'city', 'post_code', 'phone_number']
        labels = {
            "first_name": ("نام"),
            "last_name" : ("نام خانوادگی"),
            "address_1": ("آدرس"),
            "address_2": ("آدرس"),
            "state": ("استان"),
            "city": ("شهر"),
        }
    def clean(self):
        # data from the form is fetched using super function
        super(Profile_form, self).clean()
         
        # extract the username and text field from the data
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        state = self.cleaned_data.get('state')
        city = self.cleaned_data.get('city')
 
        is_digit_in_first_name = any(char.isdigit() for char in first_name)
        is_digit_in_last_name = any(char.isdigit() for char in last_name)
        is_digit_in_state = any(char.isdigit() for char in state)
        is_digit_in_city = any(char.isdigit() for char in city)
        if is_digit_in_first_name:  
             self._errors['first_name'] = self.error_class([
                'Minimum 5 characters required'])

        if is_digit_in_last_name:  
             self._errors['last_name'] = self.error_class([
                'Minimum 5 characters required'])

        if is_digit_in_state:  
             self._errors['state'] = self.error_class([
                'Minimum 5 characters required'])

        if is_digit_in_city:  
             self._errors['city'] = self.error_class([
                'Minimum 5 characters required'])

        return self.cleaned_data


class Update_account(ModelForm):
     class Meta:
        model = Custom_user
        fields = ['email', 'username',]
        labels = {
            "email": ("ایمیل"),
            "username" : ("نام کاربری"),
         }


class Call_form(forms.Form):
    subject = forms.CharField(label=_("عنوان"), widget= forms.TextInput (attrs={'placeholder':'عنوان'}), max_length=25)
    message= forms.CharField(label=_("پیام"), widget=forms.Textarea(attrs={'placeholder':'متن پیام'}))


