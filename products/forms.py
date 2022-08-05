from tkinter import Widget
from .models import *
from django import forms
from django.forms import ModelForm


class Comment_Form(ModelForm):

    class Meta:
        model = Comment
        fields = ['content', 'unknown_user' ]
        labels = {
            "content": ("متن"),
            "unknown_user" : ("کاربر ناشناس")
        }


class Reply_Form(ModelForm):

    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            "content": ("پاسخ شما"),
        }


    