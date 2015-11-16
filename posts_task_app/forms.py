# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post


class UserCreationForm(UserCreationForm):
    """
    Form for registration of new users

    """

    class Meta:
        model = User
        fields = ['username', 'email']


class PostForm(ModelForm):
    """
    Form for creation of new posts

    """

    class Meta:
        model = Post
        fields = ['title', 'text', ]
