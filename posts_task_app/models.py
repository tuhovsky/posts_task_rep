from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator


AbstractUser._meta.get_field('email')._unique = True
AbstractUser._meta.get_field('email').blank = False


class User(AbstractUser):

    pass


class Post(models.Model):

    user = models.ForeignKey(User, related_name='posts')
    title = models.CharField(max_length=255)
    text = models.TextField(validators=[MaxLengthValidator(3000)])
    create_at = models.DateTimeField(
        'date published', auto_now_add=True)

    def __str__(self):
        return self.title
