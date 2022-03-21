from .models import Custom_user, User_info
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

class Custom_userCreationForm(UserCreationForm):

    class Meta:
        model = Custom_user
        fields = ['email', 'username',]


class Profile_form(ModelForm):
    class Meta:
        model = User_info
        fields = ['first_name', 'last_name', 'address_1', 'address_2', 'state', 'city', 'post_code', 'phone_number']
