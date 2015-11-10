from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Post
from .forms import UserCreationForm, PostForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse(
                    'posts_task_app:posts-list'
                )
            )
    else:
        form = UserCreationForm()
    return render(
        request,
        "registration/register.html",
        {
            'form': form
        }
    )


@login_required()
def posts_list(request):

    posts = Post.objects.all()

    return render(
        request,
        'posts_task_app/posts_list.html',
        {
            'posts': posts,
        }
    )


@login_required()
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(
        request,
        'posts_task_app/post_detail.html',
        {'post': post, }
    )


@login_required()
def post_create(request):
    user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            user.posts.create(**form.cleaned_data)
            return HttpResponseRedirect(
                reverse(
                    'posts_task_app:posts-list'
                )
            )
    else:
        form = PostForm()
    return render(
        request,
        "posts_task_app/post_create.html",
        {
            'form': form
        }
    )
