# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.views import login, logout

from . import views

urlpatterns = [

    url(r'^accounts/login/$',
        login,
        name='login'),

    url(r'^accounts/logout/$',
        logout,
        name='logout'),

    url(r'^accounts/register/$',
        views.RegisterUser.as_view(),
        name='register'),

    url(r'^post-list/$',
        views.PostList.as_view(),
        name='post-list'),

    url(r'^post-list/(?P<pk>[0-9]+)/$',
        views.PostDetail.as_view(),
        name='post-detail'),

    url(r'^post-list/post-create/$',
        views.PostCreate.as_view(),
        name='post-create'),
]
