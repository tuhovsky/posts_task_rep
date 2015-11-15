# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator


class Post(models.Model):

    user = models.ForeignKey(User, related_name='posts')
    title = models.CharField(max_length=255)
    text = models.TextField(validators=[MaxLengthValidator(3000)])
    create_at = models.DateTimeField(
        'date published', auto_now_add=True)

    def __str__(self):
        return self.title
