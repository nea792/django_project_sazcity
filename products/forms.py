from .models import Comment
from django.forms import ModelForm


class Create_comment(ModelForm):

    class Meta:
        model = Comment
        fields = ['title', 'content', 'unknown_user' ]
        