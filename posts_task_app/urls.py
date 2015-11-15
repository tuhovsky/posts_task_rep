# -*- coding: utf-8 -*-
from django.conf.urls import url
from class_based_auth_views.views import LogoutView

from . import views

urlpatterns = [

    url(r'^accounts/login/$',
        views.Login.as_view(),
        name='login'),

    url(r'^accounts/logout/$',
        LogoutView.as_view(),
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
