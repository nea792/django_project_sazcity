from .models import Comment
from django.forms import ModelForm


class Comment_Form(ModelForm):

    class Meta:
        model = Comment
        fields = ['title', 'content', 'unknown_user' ]
        