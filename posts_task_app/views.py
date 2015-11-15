# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView, DetailView, CreateView
from .forms import UserCreationForm, PostForm
from .models import User, Post


class LoginRequiredMixin:

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class RegisterUser(FormView):

    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('posts_task_app:post-list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class PostList(LoginRequiredMixin, ListView):

    model = Post


class PostDetail(LoginRequiredMixin, DetailView):

    model = Post


class PostCreate(LoginRequiredMixin, CreateView):

    form_class = PostForm
    template_name = 'posts_task_app/post_create.html'
    success_url = reverse_lazy('posts_task_app:post-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
