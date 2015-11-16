# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView, DetailView, CreateView

from .forms import UserCreationForm, PostForm
from .models import User, Post


class LoginRequiredMixin:
    """
    Checks auth and redirects to login

    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class RegisterUser(FormView):
    """
    Registers new users

    """

    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('posts_task_app:post-list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class PostList(LoginRequiredMixin, ListView):
    """
    Returns post list

    """

    model = Post


class PostDetail(LoginRequiredMixin, DetailView):
    """
    Returns post detail

    """

    model = Post


class PostCreate(LoginRequiredMixin, CreateView):
    """
    Creates new posts

    """

    form_class = PostForm
    template_name = 'posts_task_app/post_create.html'
    success_url = reverse_lazy('posts_task_app:post-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
