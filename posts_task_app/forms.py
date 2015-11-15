# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post


class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username', 'email'
        ]


class PostForm(ModelForm):

    class Meta:
        model = Post

        fields = [
            'title', 'text',
        ]
