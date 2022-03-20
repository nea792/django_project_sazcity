from .models import Custom_user
from django.contrib.auth.forms import UserCreationForm

class Custom_userCreationForm(UserCreationForm):

    class Meta:
        model = Custom_user
        fields = ['email', 'username',]
