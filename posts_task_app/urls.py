from django.conf.urls import url
from django.contrib.auth.forms import AuthenticationForm
from . import views

urlpatterns = [

    url(r'^accounts/login/$',
        views.Login.as_view(form_class=AuthenticationForm),
        name='login'),

    url(r'^accounts/logout/$',
        views.LogoutView.as_view(),
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
